from .views import index, subtitleView, progressView
from django.urls import path

app_name = 'pages'

urlpatterns = [
    path('', index, name='index'),
    path('subtitle/<int:id>', subtitleView, name='subtitle'),
    path('progress/<str:task_id>/<int:id>', progressView, name="progress"),
]
