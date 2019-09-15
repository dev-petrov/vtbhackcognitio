from django.urls import path
from . import views

urlpatterns = [
    path('edit_document/<int:document_id>', views.edit_document)
]