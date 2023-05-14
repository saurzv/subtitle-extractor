from django.urls import include,path
from rest_framework import routers
from .views import VideoView

urlpatterns = [
    path('upload/', VideoView.as_view()),
]