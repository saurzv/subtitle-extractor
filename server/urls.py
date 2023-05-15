from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('pages.urls', namespace='pages')),
    path('api/', include('api.urls', namespace='api')),
]
