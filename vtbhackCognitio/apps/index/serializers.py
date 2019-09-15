from rest_framework import serializers
from .models import Document, Comment, User, Result

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['title', 'text', 'end_date']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class CommentSerializer(serializers.Serializer):
    user = UserSerializer()
    text = serializers.CharField()
    date = serializers.DateTimeField()


class ResultSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Result
        fields = '__all__'
