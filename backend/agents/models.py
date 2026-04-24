import uuid
from django.db import models


class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class GenerationHistory(models.Model):
    AGENT_CHOICES = [
        ("linkedin", "LinkedIn"),
        ("cv", "CV & LM"),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="history")
    agent = models.CharField(max_length=20, choices=AGENT_CHOICES)
    input_data = models.JSONField()
    output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
