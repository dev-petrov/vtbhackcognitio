from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('auth/', views.auth),
    path('login/', views.login),
    path('logout/', views.logout),
    path('docs/', views.docs),
    path('docs/<int:document_id>', views.document),
    path('create-doc/', views.create_doc),
    path('edit-doc/<int:document_id>', views.edit_doc),
]