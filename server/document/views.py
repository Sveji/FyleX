from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import cloudinary
import cloudinary.uploader
from rest_framework import status
from .models import Document
from rest_framework.permissions import IsAuthenticated;
import requests
import cloudinary.uploader

def get_public_id(document_url):
    document_url = document_url.split("/")
    joined = f"{document_url[-2]}\\{document_url[-1]}"
    result = joined.split(".")[0]

    return result


@api_view(['POST', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def document(request):  
    if request.method == 'POST':
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

        url = 'http://127.0.0.1:7000/api/service/analysis'

        data = {
            "url": str(document_url),
        }

        headers = {
            "Content-Type": "application/json",
        }

        response = requests.post(url, json = data)

        print(response.status_code)
        if response.status_code == 200:
            response_data = response.json()
        else:
            return Response("Not the correct status code!", status=status.HTTP_400_BAD_REQUEST)

        document_object = Document.objects.create(
            document = document_url,
            analysis = response_data,
        )

        return Response({
            "id": document_object.id,
            "image_url": document_url,
            "analysis": document_object.analysis,
        }, status=status.HTTP_200_OK)
    
    if request.method == 'DELETE':
        document_id = request.query_params.get('id')

        try:
            document_object = Document.objects.get(id = document_id)

            document_id = get_public_id(document_object.document)

            cloudinary.uploader.destroy(document_id, resource_type="raw")

            document_object.delete()

            return Response("Sucsessful delete!", status=status.HTTP_200_OK)
        except:
            return Response("Error, unable to delete!", status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        document_id = request.query_params.get('id')
        
        if not document_id:
            documents = Document.objects.values('id', 'document')
            return Response(list(documents), status=status.HTTP_200_OK)
        
        else:
            document = Document.objects.get(id = document_id)
            
            return Response({
                "id": document.id,
                "document": document.document
            })
        
@api_view(['GET'])
def get_summary(request):
    if request.method == 'GET':
        
        document_id = request.query_params.get('document_id')

        if not document_id:
            return Response("Error no id given!", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            document = Document.objects.get(id = document_id)
        except Document.DoesNotExist:
            return Response("Error no object found!", status=status.HTTP_400_BAD_REQUEST)
        
        url = 'http://127.0.0.1:7000/api/service/summary'

        data = {
            "url": document.document,
        }

        response = requests.post(url, json = data)

        if response.status_code == 200:
            response_data = response.json()
            summary = response_data.get('summary_text')
        else:
            return Response("Starus code error!", status=status.HTTP_400_BAD_REQUEST)

        try:
            document.summary = summary
            document.save()
        except:
            return Response("Error with the save!", status=status.HTTP_400_BAD_REQUEST)

        return Response(response)
    
@api_view(['GET'])
def get_review(request):

    document_id = request.query_params.get("document_id")

    if not document_id:
        return Response("Error no document_id!", status=status.HTTP_404_NOT_FOUND)
    
    try:
        document = Document.objects.get(id = document_id)
    except Document.DoesNotExist:
        return Response("Error no object found!", status=status.HTTP_400_BAD_REQUEST)
    
    url = ''

    data = {
        "url": document.document,
    }
    
    response = requests.post(url, json = data)

    if response.status_code == 200:
        response_data = response.json()
        review = response_data.get('review')
    else:
        return Response("Starus code error!", status=status.HTTP_400_BAD_REQUEST)

    try:
        document.review = review
        document.save()
    except:
        return Response("Error with the save!", status=status.HTTP_400_BAD_REQUEST)

    return Response(response)