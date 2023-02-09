from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="user_posts")
    content = models.CharField(max_length=140, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user}'s post({self.id}) at {self.created}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
    content = models.CharField(max_length=140, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def get_comments(self):
        return self.post.post_comments.order_by('-created').all()

    def __str__(self) -> str:
        return f"{self.user}'s comment on post \"{self.post_id}\" at {self.created}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes", null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment_likes", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user} likes {self.post}"

class Follow(models.Model):
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def get_user_followed_posts(self):
        return self.user_followed.user_posts.order_by("-created").all()

    def __str__(self) -> str:
        return f"{self.user_following} follows {self.user_followed}"