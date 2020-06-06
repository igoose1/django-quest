from django.contrib import admin
from django.urls import path

from quest import views

urlpatterns = [
    path('admin/', admin.site.urls),
#    path('view/<int:depth>/', views.view),
    path('load/<int:depth>/<signature>/', views.load)
]
