from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Book, Genre, Rental
from .schemas import BookIn, BookOut, GenreOut, RentalIn, RentalOut
from .auth import SimpleBearerAuth

router = Router()
auth_scheme = SimpleBearerAuth()


def book_to_out(book: Book) -> BookOut:
    """Book to out
    """
    return BookOut(
        id=book.id,
        title=book.title,
        author=book.author,
        description=book.description,
        published_date=book.published_date,
        genres=[GenreOut(id=g.id, name=g.name) for g in book.genres.all()]
    )


def rental_to_out(rental: Rental) -> RentalOut:
    """Rental to out
    """
    return RentalOut(
        id=rental.id,
        book_id=rental.book.id,
        book_title=rental.book.title,
        user=rental.user.username,
        rented_at=rental.rented_at,
        due_date=rental.due_date,
        returned=rental.returned
    )


@router.post("/genres/", response=GenreOut, auth=auth_scheme)
def create_genre(request, name: str) -> GenreOut:
    """Create new genre
    """
    genre, _ = Genre.objects.get_or_create(name=name)
    return GenreOut(id=genre.id, name=genre.name)


@router.get("/genres/", response=List[GenreOut])
def list_genres(request) -> List[GenreOut]:
    """List genres
    """
    return [GenreOut(id=g.id, name=g.name) for g in Genre.objects.all()]


@router.post("/books/", response=BookOut, auth=auth_scheme)
def create_book(request, data: BookIn) -> BookOut:
    """Create new book
    """
    book = Book.objects.create(
        title=data.title,
        author=data.author,
        description=data.description,
        published_date=data.published_date
    )
    book.genres.set(data.genre_ids)
    return book_to_out(book)


@router.get("/books/", response=List[BookOut])
def list_books(request, title: str = None, author: str = None, genre: int = None) -> List[BookOut]:
    """List books
    """
    qs = Book.objects.all()
    if title:
        qs = qs.filter(title__icontains=title)
    if author:
        qs = qs.filter(author__icontains=author)
    if genre:
        qs = qs.filter(genres__id=genre)
    return [book_to_out(b) for b in qs.distinct()]


@router.get("/books/{book_id}/", response=BookOut)
def get_book(request, book_id: int) -> BookOut:
    """Get book
    """
    book = get_object_or_404(Book, id=book_id)
    return book_to_out(book)


@router.put("/books/{book_id}/", response=BookOut, auth=auth_scheme)
def update_book(request, book_id: int, data: BookIn) -> BookOut:
    """Update book
    """
    book = get_object_or_404(Book, id=book_id)
    for attr, value in data.dict(exclude={"genre_ids"}).items():
        setattr(book, attr, value)
    book.genres.set(data.genre_ids)
    book.save()
    return book_to_out(book)


@router.delete("/books/{book_id}/", auth=auth_scheme)
def delete_book(request, book_id: int) -> BookOut:
    """Delete book
    """
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {"success": True}


@router.post("/rentals/", response=RentalOut, auth=auth_scheme)
def rent_book(request, data: RentalIn) -> RentalOut:
    """Rent book
    """

    active_rental = Rental.objects.filter(book_id=data.book_id, returned=False).first()
    if active_rental:
        return {"error": "Книга вже орендована"}
    rental = Rental.objects.create(
        book_id=data.book_id,
        user=request.user,
        due_date=data.due_date
    )
    return rental_to_out(rental)


@router.get("/rentals/", response=List[RentalOut], auth=auth_scheme)
def list_rentals(request) -> List[RentalOut]:
    """List rentals
    """
    rentals = Rental.objects.filter(user=request.user)
    return [rental_to_out(r) for r in rentals]


@router.post("/rentals/{rental_id}/return/", auth=auth_scheme)
def return_book(request, rental_id: int):
    """Return book
    """
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    rental.returned = True
    rental.save()
    return {"success": True}
