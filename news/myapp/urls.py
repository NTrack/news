from django.urls import path
from . import views
from . import login

urlpatterns = [
    path('getArticles/', views.ArticlesView.as_view()),
    path('comment/', views.CommentView.as_view()),
    path('like/', views.LikeView.as_view()),
    path('login/', login.user_login_func)
]
