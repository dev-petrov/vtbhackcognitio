from rest_framework import serializers
from .models import Document, Comment, User

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['title', 'text', 'end_date']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class CommentSerializer(serializers.Serializer):
    user = UserSerializer()
    text = serializers.CharField()
    date = serializers.DateTimeField()