from django.urls import path
from . import views

urlpatterns = [
    path('get_comments/<int:document_id>', views.get_comments)
]