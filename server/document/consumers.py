import json
from channels.generic.websocket import AsyncWebsocketConsumer
import os
import django
import base64
import time
from urllib.parse import parse_qs

def base64_url_decode(base64_url):
    """Base64 URL decode without any library"""
    padding = '=' * (4 - (len(base64_url) % 4))  # Add padding
    base64_url = base64_url.replace('-', '+').replace('_', '/')
    return base64.b64decode(base64_url + padding)

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

        document_id = int(document_id_str)
        document = await self.get_document(document_id)
        chat_name = await self.generate_name(document)

        await self.channel_layer.group_add(f"document_{chat_name}", self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        for group_name in self.groups_joined:
            await self.channel_layer.group_discard(group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    @database_sync_to_async
    def get_document(self, document_id):
        
        try:
            document = Document.objects.get(id = document_id)
            return document
        except Document.DoesNotExist:
            return None
        
    @database_sync_to_async
    def generate_name(self, document):
        
        url = document.document

        url = url.split("/")
        joined = f"{url[-1]}"
        result = joined.split(".")[0]

        return result

