from .serializers import VideoSerializer, SubtitleSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from .tasks import generateSRT
from .models import Subtitle
from rest_framework import filters
from server import celery_app
from django.shortcuts import redirect, HttpResponse
from django.urls import reverse


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
        task_id = generateSRT.delay(video_name, res.data['id'])

        while True:
            task = celery_app.AsyncResult(task_id)
            if task.state == 'SUCCESS':
                return redirect(reverse('pages:subtitle', kwargs={'id': res.data['id']}))
            elif task.status == 'FAILURE':
                return HttpResponse({'error': 'Something went wrong'})


def handle_upload(video):
    with open(f'media/uploads/{video.name}', 'wb+') as f:
        for chunk in video.chunks():
            f.write(chunk)
