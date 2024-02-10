from django.urls import path
from . import views

urlpatterns = [
    path('', views.test),
    path('index/',views.test),
    path('getjson/',views.index),
    path('comment/', views.CommentView.as_view())
]
