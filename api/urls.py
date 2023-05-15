from django.urls import path
from .views import VideoView, SubtitleView

urlpatterns = [
    path('upload/', VideoView.as_view()),
    path('subtitle/<int:id>', SubtitleView.as_view())
]