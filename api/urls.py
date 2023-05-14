from django.urls import path
from .views import VideoView

urlpatterns = [
    path('upload/', VideoView.as_view()),
]