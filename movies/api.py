from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Movie, Genre, Review
from .schemas import MovieIn, MovieOut, GenreOut, ReviewIn, ReviewOut
from .auth import SimpleBearerAuth

router = Router()
auth_scheme = SimpleBearerAuth()


def movie_to_out(movie: Movie) -> MovieOut:
    """ Movie to output
    """
    return MovieOut(
        id=movie.id,
        title=movie.title,
        description=movie.description,
        release_date=movie.release_date,
        rating=float(movie.rating),
        genres=[GenreOut(id=g.id, name=g.name) for g in movie.genres.all()]
    )


def review_to_out(review: Review) -> ReviewOut:
    """ Review to output
    """
    return ReviewOut(
        id=review.id,
        user=review.user.username,
        text=review.text,
        rating=review.rating,
        created_at=review.created_at.isoformat()
    )


@router.post("/genres/", response=GenreOut, auth=auth_scheme)
def create_genre(request, name: str) -> GenreOut:  #
    """ Create new genre
    """
    genre, _ = Genre.objects.get_or_create(name=name)
    return GenreOut(id=genre.id, name=genre.name)


@router.get("/genres/", response=List[GenreOut])
def list_genres(request) -> List[GenreOut]:
    """ List all genres
    """
    return [GenreOut(id=g.id, name=g.name) for g in Genre.objects.all()]


@router.post("/movies/", response=MovieOut, auth=auth_scheme)
def create_movie(request, data: MovieIn) -> MovieOut:
    """ Create new movie
    """
    movie = Movie.objects.create(
        title=data.title,
        description=data.description,
        release_date=data.release_date,
        rating=data.rating
    )
    movie.genres.set(data.genre_ids)
    return movie_to_out(movie)


@router.get("/movies/", response=List[MovieOut])
def list_movies(
        request,
        title: str = None,
        genre: int = None,
        min_rating: float = None,
        max_rating: float = None,
        start_date: str = None,
        end_date: str = None,
) -> List[MovieOut]:
    """ List all movies
    """
    qs = Movie.objects.all()
    if title:
        qs = qs.filter(title__icontains=title)
    if genre:
        qs = qs.filter(genres__id=genre)
    if min_rating is not None:
        qs = qs.filter(rating__gte=min_rating)
    if max_rating is not None:
        qs = qs.filter(rating__lte=max_rating)
    if start_date:
        qs = qs.filter(release_date__gte=start_date)
    if end_date:
        qs = qs.filter(release_date__lte=end_date)
    return [movie_to_out(m) for m in qs.distinct()]


@router.get("/movies/{movie_id}/", response=MovieOut)
def get_movie(request, movie_id: int) -> MovieOut:
    """ Get movie by id
    """
    movie = get_object_or_404(Movie, id=movie_id)
    return movie_to_out(movie)


@router.put("/movies/{movie_id}/", response=MovieOut, auth=auth_scheme)
def update_movie(request, movie_id: int, data: MovieIn) -> MovieOut:
    """ Update movie by id
    """
    movie = get_object_or_404(Movie, id=movie_id)
    for attr, value in data.dict(exclude={"genre_ids"}).items():
        setattr(movie, attr, value)
    movie.genres.set(data.genre_ids)
    movie.save()
    return movie_to_out(movie)


@router.delete("/movies/{movie_id}/", auth=auth_scheme)
def delete_movie(request, movie_id: int):
    """ Delete movie by id
    """
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return {"success": True}


@router.post("/reviews/", response=ReviewOut, auth=auth_scheme)
def add_review(request, data: ReviewIn) -> ReviewOut:
    """ Add review
    """
    review, _ = Review.objects.update_or_create(
        user=request.user,
        movie_id=data.movie_id,
        defaults={"text": data.text, "rating": data.rating}
    )
    return review_to_out(review)


@router.get("/movies/{movie_id}/reviews/", response=List[ReviewOut])
def list_reviews(request, movie_id: int) -> List[ReviewOut]:
    """ List reviews
    """
    reviews = Review.objects.filter(movie_id=movie_id)
    return [review_to_out(r) for r in reviews]
