from django.urls import path
from .views import document, get_summary

urlpatterns = [
    path('', document, name = "upload_document"),
    path('<int:id>/', document, name = "delete_document"),
    path('summary/', get_summary, name = "get_summary"),
]