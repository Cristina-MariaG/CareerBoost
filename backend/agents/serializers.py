from rest_framework import serializers


class LinkedInRequestSerializer(serializers.Serializer):
    description = serializers.CharField(min_length=10, max_length=2000)
    tone = serializers.ChoiceField(choices=["professionnel", "storytelling", "technique"])
    session_id = serializers.UUIDField()
