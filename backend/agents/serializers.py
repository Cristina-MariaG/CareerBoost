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
    mode = serializers.ChoiceField(choices=["adapt", "analyze"], default="adapt")

    def _validate_pdf(self, value, label):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(f"{label} ne doit pas dépasser 5 Mo.")
        header = value.read(4)
        value.seek(0)
        if header != b'%PDF':
            raise serializers.ValidationError(f"{label} doit être un fichier PDF valide.")
        return value

    def validate_cv(self, value):
        return self._validate_pdf(value, "Le CV")

    def validate_cover_letter(self, value):
        if value:
            return self._validate_pdf(value, "La lettre de motivation")
        return value
