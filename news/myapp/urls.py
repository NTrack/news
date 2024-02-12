from django.urls import path
from . import views

urlpatterns = [
    path('getArticles/',views.ArticlesView.as_view()),
    path('token/', views.TokenView.as_view()),
    path('comment/', views.CommentView.as_view())
]