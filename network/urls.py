from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post", views.add_post, name="add_post"),
    path("edit_post/<post_id>", views.edit_post, name="edit_post"),
    path("delete_post/<post_id>", views.delete_post, name="delete_post"),
    path("comment/<post_id>", views.comment, name="comment"),
    path("like/<post_id>", views.like, name="like"),
    path("profile/<int:user_pk>", views.profile, name="profile"),
    path("follow_unfollow/<int:user_pk>", views.follow_unfollow, name="follow_unfollow"),
    path("following", views.following, name="following"),
]