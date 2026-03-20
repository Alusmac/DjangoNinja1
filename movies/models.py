from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    """ Genre
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    """ Movie
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_date = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    genres = models.ManyToManyField(Genre, related_name="movies")

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    """ Review
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")
