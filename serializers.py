from rest_framework import serializers
from .models import Document, User

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id_document', 'title', 'description', 'document_type', 'summary', 'created_at', 'user']
        read_only_fields = ['id_document', 'created_at', 'user']

    def validate_summary(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Summary must be a valid string.")
        return value
