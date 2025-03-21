import os.path
import base64
import time
import re
import email
from email import policy
from email.parser import BytesParser
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# Using a more permissive scope to access message content and attachments
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_credentials():
    """Gets valid user credentials from storage or initiates the auth flow."""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists("token.json"):
        try:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        except ValueError as e:
            print(f"Error loading token.json: {e}")
            print("Will create a new token file...")
            # Delete the invalid token file
            os.remove("token.json")
            creds = None

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("Refreshed expired token.")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            # Force approval prompt to get refresh token
            flow.run_local_server(
                port=3000,
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'
            )
            creds = flow.credentials

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Verify we have a refresh token
    if not creds.refresh_token:
        print("WARNING: No refresh token in credentials. Token will expire.")

    return creds


def extract_email_address(sender_string):
    """Extracts email address from a string like 'Name <email@example.com>'."""
    email_match = re.search(r'<(.+?)>', sender_string)
    if email_match:
        return email_match.group(1)
    else:
        # If no angle brackets, the string might be just the email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', sender_string)
        if email_match:
            return email_match.group(0)
    return None


def get_email_content(service, msg_id):
    """Gets the full content of a specific email using Python's email parser."""
    try:
        # Get the raw message
        message = service.users().messages().get(
            userId="me",
            id=msg_id,
            format="raw"
        ).execute()

        # Decode the raw message
        raw_msg = base64.urlsafe_b64decode(message['raw'])

        # Parse the message using Python's email module
        mime_msg = BytesParser(policy=policy.default).parsebytes(raw_msg)

        # Extract headers
        subject = mime_msg['Subject'] or ""
        sender = mime_msg['From'] or ""
        sender_email = extract_email_address(sender)
        date = mime_msg['Date'] or ""

        # Extract body content
        body = ""
        attachments = []

        # Walk through all parts of the email
        for part in mime_msg.walk():
            # Get content type
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", "")).lower()

            try:
                # If this part is an attachment
                if "attachment" in content_disposition or "inline" in content_disposition and part.get_filename():
                    # Extract attachment info
                    filename = part.get_filename()
                    if filename:
                        # Get attachment data
                        attachment_data = part.get_payload(decode=True)
                        attachment = {
                            "filename": filename,
                            "mimeType": content_type,
                            "size": len(attachment_data),
                            "data": attachment_data
                        }
                        attachments.append(attachment)
                # If the part is text and not an attachment, it's part of the body
                elif content_type in ["text/plain", "text/html"]:
                    charset = part.get_content_charset() or 'utf-8'
                    try:
                        part_body = part.get_payload(decode=True).decode(charset)
                        # Prefer plain text for readability, add HTML only if we don't have plain text
                        if content_type == "text/plain" or not body:
                            body += part_body
                    except UnicodeDecodeError:
                        try:
                            part_body = part.get_payload(decode=True).decode('latin-1')
                            if content_type == "text/plain" or not body:
                                body += part_body
                        except:
                            pass
            except Exception as e:
                print(f"Error processing email part: {e}")

        # Get the message raw data as backup if we failed to extract the body
        if not body and 'raw' in message:
            try:
                # This is a fallback to ensure we get something
                body = "[Email body extraction incomplete - showing raw content]\n"
                body += base64.urlsafe_b64decode(message['raw']).decode('utf-8')
            except:
                body = "[Could not decode email body]"

        # Debug information
        if not body and attachments:
            print(f"DEBUG: Email with subject '{subject}' has attachments but no body text.")

        return {
            "id": msg_id,
            "subject": subject,
            "sender": sender,
            "sender_email": sender_email,
            "date": date,
            "body": body,
            "attachments": attachments
        }

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
    except Exception as e:
        print(f"Unexpected error in get_email_content: {e}")
        return None


def save_attachment(file_data, filename):
    """Saves attachment data to a file."""
    if not os.path.exists("attachments"):
        os.makedirs("attachments")

    filepath = os.path.join("attachments", filename)
    with open(filepath, "wb") as f:
        f.write(file_data)
    return filepath


def get_inbox_messages(service, max_results=10, query="in:inbox", last_history_id=None):
    """Gets messages from the inbox with optional filtering by historyId."""
    try:
        # Get list of messages
        results = service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get("messages", [])

        if not messages:
            return [], last_history_id

        # Filter by historyId if provided
        if last_history_id:
            # Get only messages with a higher historyId
            new_messages = []
            for message in messages:
                msg_data = service.users().messages().get(
                    userId="me",
                    id=message["id"],
                    format="minimal"
                ).execute()

                if int(msg_data["historyId"]) > last_history_id:
                    new_messages.append(message)

            messages = new_messages

        # Get full details for each message
        email_data = []
        new_history_id = last_history_id

        for message in messages:
            msg_id = message["id"]
            email_content = get_email_content(service, msg_id)

            if email_content:
                email_data.append(email_content)

                # Update history ID to track the latest message
                msg_data = service.users().messages().get(
                    userId="me",
                    id=msg_id,
                    format="minimal"
                ).execute()

                current_history_id = int(msg_data["historyId"])
                if not new_history_id or current_history_id > new_history_id:
                    new_history_id = current_history_id

        return email_data, new_history_id

    except HttpError as error:
        print(f"An error occurred: {error}")
        return [], last_history_id


def display_email(email):
    """Displays the complete information about an email."""
    print("\n" + "=" * 80)
    print(f"NEW EMAIL RECEIVED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print(f"From: {email['sender']}")
    print(f"Email: {email['sender_email']}")
    print(f"Subject: {email['subject']}")
    print(f"Date: {email['date']}")
    print(f"\nBody:\n{'-' * 80}")
    print(email['body'] if email['body'] else "[No body content]")
    print(f"{'-' * 80}")

    # Process attachments
    if email['attachments']:
        print(f"\nAttachments ({len(email['attachments'])}):")
        for attachment in email['attachments']:
            print(f"  - {attachment['filename']} ({attachment['mimeType']}, {attachment['size']} bytes)")

            # Optionally save the attachment
            if "data" in attachment:
                filepath = save_attachment(attachment["data"], attachment["filename"])
                print(f"    Saved to: {filepath}")
    else:
        print("\nNo attachments")
    print("=" * 80)


def main():
    """Main function to continuously monitor Gmail for new emails."""
    last_history_id = None
    check_interval = 60  # Check every minute (60 seconds)

    print("Starting Gmail Monitor...")
    print("Waiting for new emails...")

    while True:
        try:
            # Get credentials (will refresh if needed)
            creds = get_credentials()

            # Build the Gmail service
            service = build("gmail", "v1", credentials=creds)

            # Get profile info to get the initial historyId if needed
            if last_history_id is None:
                profile = service.users().getProfile(userId="me").execute()
                last_history_id = int(profile["historyId"])
                print(f"Initial history ID: {last_history_id}")

            # Get new messages from inbox
            emails, new_history_id = get_inbox_messages(
                service,
                max_results=10,
                last_history_id=last_history_id
            )

            # Process new emails
            if emails:
                print(f"Found {len(emails)} new email(s)!")
                for email in emails:
                    display_email(email)

            # Update last history ID
            if new_history_id and new_history_id != last_history_id:
                last_history_id = new_history_id

            # Wait before checking again
            time.sleep(check_interval)

        except HttpError as error:
            print(f"An error occurred: {error}")
            time.sleep(60)  # Wait a bit before retrying on error
        except KeyboardInterrupt:
            print("Exiting Gmail Monitor...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            print("Waiting before retry...")
            time.sleep(60)


if __name__ == "__main__":
    main()