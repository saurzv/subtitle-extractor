from django.urls import path
from .views import VideoView, SubtitleView, statusView

app_name = 'api'

urlpatterns = [
    path('upload/', VideoView.as_view()),
    path('subtitle/<int:id>/', SubtitleView.as_view()),
    path('status/<str:task_id>/', statusView, name="status"),
]
