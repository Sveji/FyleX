import json
from channels.generic.websocket import AsyncWebsocketConsumer
import os
import django
import base64
import time
from urllib.parse import parse_qs
import httpx

# DECODER
def base64_url_decode(base64_url):
    """Base64 URL decode without any library"""
    padding = '=' * (4 - (len(base64_url) % 4))  # Add padding
    base64_url = base64_url.replace('-', '+').replace('_', '/')
    return base64.b64decode(base64_url + padding)

# JWT DECODE
def decode_jwt(jwt):
    """Decode JWT and return the header and payload"""
    try:
        parts = jwt.split(".")
        
        if len(parts) != 3:
            raise ValueError("Invalid JWT: must have 3 parts")

        header = base64_url_decode(parts[0]).decode("utf-8")
        payload = base64_url_decode(parts[1]).decode("utf-8")
        
        header_json = json.loads(header)
        payload_json = json.loads(payload)
        
        return header_json, payload_json
    except Exception as e:
        return {"error": str(e)}

# CHECK TOKEN VALIDITY
def check_token_validity(jwt):
    """Check if the JWT token is structurally valid"""
    header, payload = decode_jwt(jwt)
    
    if "error" in header:
        return False, header["error"]  
    
    if "exp" in payload:
        exp_time = payload["exp"]
        if exp_time < time.time():
            return False, "Token is expired"
    
    if "username" not in payload:
        return False, "Token does not contain username"

    return True, "Token is valid"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

from channels.db import database_sync_to_async
from .models import Document

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # GET TOKEN FROM QUERY
        query_string = self.scope["query_string"].decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]
        document_id_str = query_params.get("document_id", [None])[0]

        if not document_id_str:
            await self.close()

        # IS THE TOKEN VALID
        is_valid, message = check_token_validity(token)
        if is_valid == False:
            await self.close()

        # GET TOKEN DECODED AND SET SELF.USERNAME
        header, payload = decode_jwt(token)
        self.username = payload.get("username", "guest_user")

        # GET THE DOCUMENT WE ARE GOING TO BE USING AND THE GROUP NAME 
        document_id = int(document_id_str)
        document = await self.get_document(document_id)
        chat_name = await self.generate_name(document)

        await self.channel_layer.group_add(f"document_{chat_name}", self.channel_name)

        self.group_name = f"document_{chat_name}"

        self.document = document

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(f"document_{self.group_name}", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        # SEND MESSAGE RECIVER
        if action == "send_message":
            question = data.get("question")

            data_for_post = {
                "url": self.document.document,
                "question": question,
            }

            response_data = await self.send_post_request(data_for_post)

            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "send_message_notification",
                    "question": question,
                    "response_data": response_data,
                    "url": self.document.document,
                },
            )

    # GET DOCUMENT
    @database_sync_to_async
    def get_document(self, document_id):
        
        try:
            document = Document.objects.get(id = document_id)
            return document
        except Document.DoesNotExist:
            return None
        
    # GENERATE NAME
    @database_sync_to_async
    def generate_name(self, document):
        
        url = document.document

        url = url.split("/")
        joined = f"{url[-1]}"
        result = joined.split(".")[0]

        return result

    # SEND MESSAGE NOTIFICATION
    async def send_message_notification(self, event):
        await self.send(text_data=json.dumps({
            "action": "succses",
            "question": event["question"],
            "response_data": event["response_data"],
            "url": event["url"]
        }))

    # SEND POST REQUEST TO THE MICROSERVICE
    async def send_post_request(self, data):
        
        url = 'http://127.0.0.1:7000/api/service/qa'

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=data)
                return response.json()
            except httpx.HTTPStatusError as e:
                return {"error": f"HTTP error: {e.response.status_code}"}
            except httpx.RequestError as e:
                return {"error": f"Request error: {str(e)}"}