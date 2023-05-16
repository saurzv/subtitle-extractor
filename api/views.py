from .serializers import VideoSerializer, SubtitleSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from .tasks import generateSRT
from .models import Subtitle
from rest_framework import filters
from server import celery_app
from django.shortcuts import redirect
from django.urls import reverse

class SubtitleView(ListAPIView):
    serializer_class = SubtitleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['content']

    def get_queryset(self):
        id=self.kwargs['id']
        return Subtitle.objects.filter(video_id=id)
    
class VideoView(CreateAPIView):
    serializer_class = VideoSerializer

    def post(self, request, *args, **kwargs):
        video = request.data.get('file').name
        rsp = super().post(request, *args, **kwargs)
        task_id = generateSRT.delay(video, rsp.data['id'])

        return rsp