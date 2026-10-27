from django.urls import path

from .views import (
    ArtistDetailAPIView,
    ArtistListCreateAPIView,
    GenreDetailAPIView,
    GenreListCreateAPIView,
    RecordDetailAPIView,
    RecordListCreateAPIView,
)

urlpatterns = [

    path("records", RecordListCreateAPIView.as_view(), name="record-list-create"),
    path("records/<int:pk>", RecordDetailAPIView.as_view(), name="record-detail"),

    path("artists", ArtistListCreateAPIView.as_view(), name="artist-list-create"),
    path("artists/<int:pk>", ArtistDetailAPIView.as_view(), name="artist-detail"),

    path("genres", GenreListCreateAPIView.as_view(), name="genre-list-create"),
    path("genres/<int:pk>", GenreDetailAPIView.as_view(), name="genre-detail"),
]