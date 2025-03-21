from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import cloudinary
import cloudinary.uploader
from rest_framework import status
from .models import Document
from rest_framework.permissions import IsAuthenticated
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
        user = request.user
        name = request.data.get('name')

        if not name:
            return Response("Error, there is no name!", status=status.HTTP_404_NOT_FOUND)

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

        if response.status_code == 200:
            response_data = response.json()
        else:
            return Response("Not the correct status code!", status=status.HTTP_400_BAD_REQUEST)

        document_object = Document.objects.create(
            document = document_url,
            analysis = response_data,
            user = user,
            name = name,
        )

        return Response({
            "id": document_object.id,
            "document_url": document_url,
            "analysis": document_object.analysis,
            "name": document_object.name,
        }, status=status.HTTP_200_OK)
    
    if request.method == 'DELETE':
        document_id = request.query_params.get('id')

        try:
            document_object = Document.objects.get(id = document_id)

            user = request.user
            if document_object.user.id != user.id:
                return Response("The id is not for the user!", status=status.HTTP_400_BAD_REQUEST)

            document_id = get_public_id(document_object.document)

            cloudinary.uploader.destroy(document_id, resource_type="raw")

            document_object.delete()

            return Response("Sucsessful delete!", status=status.HTTP_200_OK)
        except:
            return Response("Error, unable to delete!", status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        document_id = request.query_params.get('id')
        user = request.user

        if not document_id:
            documents = Document.objects.values('id', 'document', 'analysis', 'summary', 'review', "user_id", "name").filter(user = user.id)
            return Response(list(documents), status=status.HTTP_200_OK)
        
        else:
            try:
                document = Document.objects.get(id = document_id)
            except:
                return Response("Error, incorrect given id!", status=status.HTTP_400_BAD_REQUEST)
            
            if document.user.id != user.id:
                return Response("The id is not for the user!", status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "id": document.id,
                "document": document.document,
                "analysis": document.analysis,
                "summary": document.summary,
                "review": document.review,
                "user_id": user.id,
                "name": document.name,
            })
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request):
    if request.method == 'GET':
        
        user = request.user

        document_id = request.query_params.get('document_id')

        if not document_id:
            return Response("Error no id given!", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            document = Document.objects.get(id = document_id)
            if document.user.id != user.id:
                return Response("The id is not for the user!", status=status.HTTP_400_BAD_REQUEST)
        except Document.DoesNotExist:
            return Response("Error no object found!", status=status.HTTP_400_BAD_REQUEST)
        
        url = 'http://127.0.0.1:7000/api/service/summary'

        data = {
            "url": document.document,
        }

        try:
            response = requests.post(url, json=data, timeout=10)  
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to reach the summary service: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

        try:
            response_data = response.json()
        except ValueError:
            return Response({"error": "Invalid response format from summary service!"}, status=status.HTTP_502_BAD_GATEWAY)

        summary = response_data.get("summary_text")
        if not summary:
            return Response({"error": "Summary text missing in response!"}, status=status.HTTP_502_BAD_GATEWAY)

        try:
            document.summary = summary
            document.save()
        except Exception as e:
            return Response({"error": f"Failed to save summary: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Summary retrieved successfully!", "summary": summary}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def get_review(request):

    user = request.user

    document_id = request.query_params.get("document_id")

    if not document_id:
        return Response("Error no document_id!", status=status.HTTP_404_NOT_FOUND)
    
    try:
        document = Document.objects.get(id = document_id)
        if document.user.id != user.id:
            return Response("The id is not for the user!", status=status.HTTP_400_BAD_REQUEST)
    except Document.DoesNotExist:
        return Response("Error no object found!", status=status.HTTP_400_BAD_REQUEST)
    
    url = 'http://127.0.0.1:7000/api/service/review'

    data = {
        "url": document.document,
        "analysis": document.analysis,
    }
    
    response = requests.post(url, json = data)

    if response.status_code == 200:
        response_data = response.json()
    else:
        return Response("Starus code error!", status=status.HTTP_400_BAD_REQUEST)

    try:
        document.review = response_data
        document.save()
    except:
        return Response("Error with the save!", status=status.HTTP_400_BAD_REQUEST)

    return Response(response)