from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('main.urls')),
    path('users/', include('users.urls')),
    path('', include('project.urls')),
]

