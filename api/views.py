from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from server import celery_app
from .serializers import VideoSerializer, SubtitleSerializer
from .tasks import generateSRT
from .models import Subtitle


def statusView(request, task_id):
    task = celery_app.AsyncResult(task_id)

    return JsonResponse({'status': task.state})


# Not used in production, used in testing
class SubtitleView(ListAPIView):
    serializer_class = SubtitleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['content']

    def get_queryset(self):
        id = self.kwargs['id']
        return Subtitle.objects.filter(video_id=id)


class VideoView(CreateAPIView):
    serializer_class = VideoSerializer

    def post(self, request, *args, **kwargs):
        video = request.data.get('file')
        handle_upload(video)
        video_name = video.name
        res = super().post(request, *args, **kwargs)
        task = generateSRT.delay(video_name, res.data['id'])

        return redirect(reverse('pages:progress', kwargs={'task_id': task.task_id, 'id': res.data['id']}))


def handle_upload(video):
    with open(f'media/uploads/{video.name}', 'wb+') as f:
        for chunk in video.chunks():
            f.write(chunk)
