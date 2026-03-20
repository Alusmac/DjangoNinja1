from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    """Class Genre
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    """Class Book
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    published_date = models.DateField(default=date(2000, 1, 1))
    genres = models.ManyToManyField(Genre, related_name="books")

    def __str__(self) -> str:
        return self.title


class Rental(models.Model):
    """Class Rental
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="rentals")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rentals")
    rented_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned = models.BooleanField(default=False)

    class Meta:
        unique_together = ("book", "user", "returned")
