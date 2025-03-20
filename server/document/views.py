from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import cloudinary
import cloudinary.uploader
from rest_framework import status
from .models import Document

@api_view(['POST'])
def upload_document(request):
    document = request.FILES.get('document')

    if not document:
        return Response("Error there is no document!", status=status.HTTP_404_NOT_FOUND)

    try:
        upload_result = cloudinary.uploader.upload(
            document,
            folder = 'hackTues11',
            resource_type = 'raw',
        )
    except:
        return Response("Error object not created!", status=status.HTTP_400_BAD_REQUEST)
    
    document_url = upload_result['secure_url']

    document_object = Document.objects.create(
        document = document_url
    )

    return Response({
        "id": document_object.id,
        "image_url": document_url
    }, status=status.HTTP_200_OK)