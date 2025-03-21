import os.path
import base64
import time
import re
import email
import pickle
import json
import uuid
import socket
import threading
from email import policy
from email.parser import BytesParser
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# We need these scopes for push notifications and reading emails
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.metadata"
]

# File to store processed message IDs
PROCESSED_IDS_FILE = "processed_emails.pkl"

# Your domain for push notifications - update this to your actual domain or IP
# For local testing, you can use ngrok to expose your local server
DOMAIN = "194.141.252.114"  # or use your public IP or ngrok URL
PORT = 8080
NOTIFICATION_TOPIC = f"projects/gmail-notifications-{uuid.uuid4()}"


class NotificationHandler(BaseHTTPRequestHandler):
    """Handler for Gmail push notifications."""

    def do_POST(self):
        """Handle POST requests from Gmail push notifications."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            # Parse the notification data
            notification = json.loads(post_data)

            # Respond with 200 OK to acknowledge receipt
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')

            # Process the notification in a separate thread
            threading.Thread(target=self.process_notification, args=(notification,)).start()

        except Exception as e:
            print(f"Error handling notification: {e}")
            self.send_response(500)
            self.end_headers()

    def process_notification(self, notification):
        """Process the Gmail notification data."""
        try:
            # Extract message data if available
            data = notification.get('message', {}).get('data', '')
            if data:
                # Data is base64-encoded
                decoded_data = base64.b64decode(data).decode('utf-8')
                data_json = json.loads(decoded_data)

                # Check if it's an email notification
                if 'emailAddress' in data_json:
                    # Get the historyId from the notification
                    history_id = data_json.get('historyId')
                    if history_id:
                        print(f"Received notification with historyId: {history_id}")
                        # Retrieve the new messages
                        check_for_new_emails(history_id)
        except Exception as e:
            print(f"Error processing notification data: {e}")


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


def load_processed_ids():
    """Load the set of already processed message IDs from disk."""
    if os.path.exists(PROCESSED_IDS_FILE):
        try:
            with open(PROCESSED_IDS_FILE, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading processed IDs: {e}")
    return set()


def save_processed_ids(processed_ids):
    """Save the set of processed message IDs to disk."""
    try:
        with open(PROCESSED_IDS_FILE, "wb") as f:
            pickle.dump(processed_ids, f)
    except Exception as e:
        print(f"Error saving processed IDs: {e}")


def setup_push_notifications(service, user_id="me"):
    """Set up Gmail API push notifications."""
    try:
        # Define a new push notification
        body = {
            'labelIds': ['INBOX'],
            'topicName': NOTIFICATION_TOPIC,
            'labelFilterAction': 'include'
        }

        # Register the watch on the user's inbox
        result = service.users().watch(userId=user_id, body=body).execute()

        # Check the result
        historyId = result.get('historyId')
        expiration = result.get('expiration')

        print(f"Push notifications set up successfully!")
        print(f"History ID: {historyId}")
        print(f"Expiration: {datetime.fromtimestamp(int(expiration) / 1000)}")

        return historyId

    except HttpError as error:
        print(f"An error occurred setting up push notifications: {error}")
        return None


def fetch_history(service, start_history_id, user_id="me"):
    """Fetch history of changes since the start_history_id."""
    try:
        history_list = service.users().history().list(
            userId=user_id,
            startHistoryId=start_history_id,
            historyTypes=['messageAdded']
        ).execute()

        # Extract added message IDs
        messages = []
        if 'history' in history_list:
            for history in history_list['history']:
                if 'messagesAdded' in history:
                    for message in history['messagesAdded']:
                        # Get the message ID
                        msg_id = message['message']['id']
                        messages.append(msg_id)

        return messages

    except HttpError as error:
        print(f"An error occurred fetching history: {error}")
        return []


def check_for_new_emails(history_id=None):
    """Check for new emails using the Gmail API."""
    try:
        # Get credentials and build service
        creds = get_credentials()
        service = build("gmail", "v1", credentials=creds)

        # Load processed message IDs
        processed_ids = load_processed_ids()

        # If no history_id provided, get the latest messages directly
        if not history_id:
            # Get list of messages
            results = service.users().messages().list(
                userId="me",
                q="in:inbox",
                maxResults=10
            ).execute()

            messages = results.get("messages", [])
            msg_ids = [msg['id'] for msg in messages]
        else:
            # Use history to get new message IDs
            msg_ids = fetch_history(service, history_id)

        # Filter out already processed messages
        new_msg_ids = [msg_id for msg_id in msg_ids if msg_id not in processed_ids]

        if not new_msg_ids:
            return

        # Fetch and process new emails
        new_emails = []
        for msg_id in new_msg_ids:
            email_content = get_email_content(service, msg_id)
            if email_content:
                new_emails.append(email_content)
                # Mark as processed
                processed_ids.add(msg_id)

        # Display new emails
        if new_emails:
            print(f"Found {len(new_emails)} new email(s)!")
            for email in new_emails:
                display_email(email)

            # Save updated processed IDs
            save_processed_ids(processed_ids)

    except Exception as e:
        print(f"Error checking for new emails: {e}")


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


def run_notification_server():
    """Run the HTTP server to receive push notifications."""
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, NotificationHandler)
    print(f"Starting notification server on port {PORT}...")
    httpd.serve_forever()


def main():
    """Main function to set up Gmail push notifications and listen for updates."""
    try:
        # Get credentials and build service
        creds = get_credentials()
        service = build("gmail", "v1", credentials=creds)

        # Load processed message IDs
        processed_ids = load_processed_ids()
        print(f"Loaded {len(processed_ids)} previously processed email IDs")

        # Start notification server in a separate thread
        server_thread = threading.Thread(target=run_notification_server, daemon=True)
        server_thread.start()

        # Set up push notifications
        history_id = setup_push_notifications(service)
        if not history_id:
            print("Failed to set up push notifications. Falling back to periodic checking.")

        # Initial check for new emails
        print("Checking for new emails...")
        check_for_new_emails()

        print("Gmail Listener is now running. Press Ctrl+C to exit.")

        # Keep the main thread alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting Gmail Listener...")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()