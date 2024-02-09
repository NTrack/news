from django.urls import path
from . import views

urlpatterns = [
    path('', views.test),
    path('index/',views.test),
    path('getjson/',views.index),
]
