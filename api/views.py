from .serializers import VideoSerializer
from rest_framework.generics import CreateAPIView
from .tasks import generateSRT
from django.conf import settings

class VideoView(CreateAPIView):
    serializer_class = VideoSerializer

    def post(self, request, *args, **kwargs):
        video = request.data.get('file')
        rsp = super().post(request, *args, **kwargs)
        generateSRT.delay(settings.MEDIA_ROOT+'uploads/{}'.format(video.name))
        return rsp