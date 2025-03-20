from django.urls import path
from .views import document

urlpatterns = [
    path('', document, name = "upload_document"),
    path('<int:id>/', document, name = "delete_document"),
]