from .views import index, subtitleView
from django.urls import path

app_name = 'pages'

urlpatterns = [
    path('', index, name='index'),
    path('subtitle/<int:id>', subtitleView, name='subtitle'),
]