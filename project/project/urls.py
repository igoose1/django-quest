from django.contrib import admin
from django.urls import path, include

from quest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('view/<int:depth>/', views.view),
    path('load/<int:depth>/<signature>/', views.load),
    path('', views.start),
    path('end/', views.end),
    path('summernote/', include('django_summernote.urls'))
]
