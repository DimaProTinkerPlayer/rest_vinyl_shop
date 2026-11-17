import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from shop.models import Artist, Genre, Record


@pytest.fixture
def api_client():
    """Неавторизований HTTP-клієнт DRF."""
    return APIClient()


@pytest.fixture
def regular_user(db):
    """Звичайний зареєстрований користувач (is_staff=False)."""
    return User.objects.create_user(
        username="regular_user",
        email="user@example.com",
        password="StrongPassword123!",
        is_staff=False,
    )


@pytest.fixture
def auth_client(api_client, regular_user):
    """Клієнт, авторизований під звичайним користувачем."""
    api_client.force_authenticate(user=regular_user)
    return api_client


@pytest.fixture
def admin_user(db):
    """Адміністратор системи (is_staff=True)."""
    return User.objects.create_user(
        username="admin_user",
        email="admin@example.com",
        password="AdminPassword123!",
        is_staff=True,
    )


@pytest.fixture
def admin_client(api_client, admin_user):
    """Клієнт, авторизований під адміністратором."""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def artist(db):
    """Тестовий виконавець."""
    return Artist.objects.create(name="Pink Floyd")


@pytest.fixture
def genre(db):
    """Тестовий жанр."""
    return Genre.objects.create(name="Progressive Rock")


@pytest.fixture
def record(db, artist, genre):
    """Тестова вінілова платівка у базі даних."""
    return Record.objects.create(
        album="The Dark Side of the Moon",
        artist=artist,
        genre=genre,
        price="34.99",
        year=1973,
        cover_image="https://example.com/dsotm.jpg",
    )