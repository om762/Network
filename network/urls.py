
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("posts/", views.posts, name="posts"),
    path("new-post/", views.new_post, name="new_post"),
    path("like-post/", views.like_post, name="like_post"),
    path('comments/<int:post_id>/', views.view_comments, name="view_comments"),
    path("comment/", views.comment, name="comment"),
    path("toggle_follow/", views.toggle_follow, name="toggle_follow")
]
