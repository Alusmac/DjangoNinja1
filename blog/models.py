from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """Tag model
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    """Post model
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """Comment model
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
