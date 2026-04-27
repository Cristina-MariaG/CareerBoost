import json
from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Session, GenerationHistory
from .serializers import LinkedInRequestSerializer, CvRequestSerializer, GenerationHistorySerializer
from .services.linkedin_agent import generate as linkedin_agent_generate
from .services.cv_agent import generate as cv_agent_generate, analyze as cv_agent_analyze, extract_text_from_pdf
from .services.claude_client import ClaudeError


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok'})


@api_view(['GET'])
def history(request):
    session_id = request.query_params.get('session_id')
    if not session_id:
        return Response({'error': 'session_id requis.'}, status=400)
    try:
        session = Session.objects.get(id=session_id)
    except (Session.DoesNotExist, Exception):
        return Response([], status=200)
    items = session.history.all()[:20]
    serializer = GenerationHistorySerializer(items, many=True)
    return Response(serializer.data)


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
            for chunk in linkedin_agent_generate(data['description'], data['tone']):
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


@api_view(['POST'])
def cv_generate(request):
    serializer = CvRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    data = serializer.validated_data
    session, _ = Session.objects.get_or_create(id=data['session_id'])

    try:
        cv_text = extract_text_from_pdf(data['cv'].read())
        cover_letter_text = (
            extract_text_from_pdf(data['cover_letter'].read())
            if data.get('cover_letter')
            else ""
        )
    except ClaudeError as e:
        return Response({'error': str(e)}, status=400)

    mode = data.get('mode', 'adapt')
    agent_fn = cv_agent_analyze if mode == 'analyze' else cv_agent_generate

    def event_stream():
        output_chunks = []
        try:
            for chunk in agent_fn(data['job_offer'], cv_text, cover_letter_text):
                output_chunks.append(chunk)
                yield f"data: {json.dumps({'text': chunk})}\n\n"

            full_output = "".join(output_chunks)
            GenerationHistory.objects.create(
                session=session,
                agent="cv",
                input_data={"job_offer": data['job_offer'], "mode": mode},
                output=full_output,
            )
            yield "data: [DONE]\n\n"

        except ClaudeError as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response
