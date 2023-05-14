from .models import Video
from .serializers import VideoSerializer
from rest_framework.generics import CreateAPIView

class VideoView(CreateAPIView):
    serializer_class = VideoSerializer
