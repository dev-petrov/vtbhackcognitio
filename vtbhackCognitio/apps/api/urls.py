from django.urls import path
from . import views

urlpatterns = [
    path('edit_document/<int:document_id>', views.edit_document),
    path('add_comment/<int:document_id>', views.add_comment),
]