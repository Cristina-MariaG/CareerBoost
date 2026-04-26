from rest_framework import serializers
from .models import GenerationHistory


class GenerationHistorySerializer(serializers.ModelSerializer):
    preview = serializers.SerializerMethodField()

    class Meta:
        model = GenerationHistory
        fields = ['id', 'agent', 'input_data', 'preview', 'output', 'created_at']

    def get_preview(self, obj):
        return obj.output[:200].strip()


class LinkedInRequestSerializer(serializers.Serializer):
    description = serializers.CharField(min_length=10, max_length=2000)
    tone = serializers.ChoiceField(choices=["professionnel", "storytelling", "technique"])
    session_id = serializers.UUIDField()


class CvRequestSerializer(serializers.Serializer):
    job_offer = serializers.CharField(min_length=20, max_length=5000)
    session_id = serializers.UUIDField()
    cv = serializers.FileField()
    cover_letter = serializers.FileField(required=False)

    def validate_cv(self, value):
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Le CV doit être un fichier PDF.")
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Le CV ne doit pas dépasser 5 Mo.")
        return value

    def validate_cover_letter(self, value):
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("La lettre de motivation doit être un fichier PDF.")
        if value and value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("La lettre de motivation ne doit pas dépasser 5 Mo.")
        return value
