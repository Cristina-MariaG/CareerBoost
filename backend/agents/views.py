import json
from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Session, GenerationHistory
from .serializers import LinkedInRequestSerializer
from .services.linkedin_agent import generate
from .services.claude_client import ClaudeError


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok'})


@api_view(['POST'])
def linkedin_generate(request):
    serializer = LinkedInRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    data = serializer.validated_data
    session, _ = Session.objects.get_or_create(id=data['session_id'])

    def event_stream():
        output_chunks = []
        try:
            for chunk in generate(data['description'], data['tone']):
                output_chunks.append(chunk)
                yield f"data: {json.dumps({'text': chunk})}\n\n"

            full_output = "".join(output_chunks)
            GenerationHistory.objects.create(
                session=session,
                agent="linkedin",
                input_data={"description": data['description'], "tone": data['tone']},
                output=full_output,
            )
            yield "data: [DONE]\n\n"

        except ClaudeError as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response
