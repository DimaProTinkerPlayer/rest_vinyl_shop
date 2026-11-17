import pytest
from rest_framework import status

from shop.models import Record


@pytest.mark.django_db
class TestRecordEndpoints:
    list_url = "/records"

    def detail_url(self, pk):
        return f"/records/{pk}"


    def test_get_records_list_public(self, api_client, record):
        response = api_client.get(self.list_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["album"] == record.album

    def test_get_records_search_and_filter(self, api_client, record, artist, genre):
        response_found = api_client.get(self.list_url, {"search": "Dark Side", "genre_id": genre.id})
        assert response_found.status_code == status.HTTP_200_OK
        assert len(response_found.data) == 1

        response_empty = api_client.get(self.list_url, {"search": "NonExistentAlbum"})
        assert response_empty.status_code == status.HTTP_200_OK
        assert len(response_empty.data) == 0

    def test_get_record_detail_public(self, api_client, record):
        response = api_client.get(self.detail_url(record.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == record.id
        assert response.data["album"] == "The Dark Side of the Moon"


    def test_create_record_as_admin(self, admin_client, artist, genre):
        payload = {
            "album": "Wish You Were Here",
            "artist_id": artist.id,
            "genre_id": genre.id,
            "price": "39.99",
            "year": 1975,
            "cover_image": "https://example.com/wywh.jpg",
        }
        response = admin_client.post(self.list_url, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Record.objects.count() == 1
        assert response.data["album"] == "Wish You Were Here"

    def test_update_record_as_admin(self, admin_client, record, artist, genre):
        payload = {
            "album": "The Dark Side of the Moon (Remastered)",
            "artist_id": artist.id,
            "genre_id": genre.id,
            "price": "44.99",
            "year": 1973,
            "cover_image": "https://example.com/dsotm-remaster.jpg",
        }
        response = admin_client.put(self.detail_url(record.id), payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        record.refresh_from_db()
        assert record.album == "The Dark Side of the Moon (Remastered)"
        assert str(record.price) == "44.99"

    def test_delete_record_as_admin(self, admin_client, record):
        response = admin_client.delete(self.detail_url(record.id))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Record.objects.count() == 0


    def test_create_record_unauthenticated_returns_401(self, api_client, artist, genre):
        payload = {
            "album": "Animals",
            "artist_id": artist.id,
            "genre_id": genre.id,
            "price": "29.99",
            "year": 1977,
        }
        response = api_client.post(self.list_url, payload, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Record.objects.count() == 0

    def test_create_record_as_regular_user_returns_403(self, auth_client, artist, genre):
        payload = {
            "album": "Animals",
            "artist_id": artist.id,
            "genre_id": genre.id,
            "price": "29.99",
            "year": 1977,
        }
        response = auth_client.post(self.list_url, payload, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Record.objects.count() == 0

    def test_delete_record_as_regular_user_returns_403(self, auth_client, record):
        response = auth_client.delete(self.detail_url(record.id))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Record.objects.count() == 1

    def test_create_record_invalid_data_returns_400(self, admin_client, artist, genre):
        payload = {
            "album": "",
            "artist_id": artist.id,
            "genre_id": genre.id,
            "price": "-15.00",
            "year": 1975,
        }
        response = admin_client.post(self.list_url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_get_nonexistent_record_returns_404(self, api_client):
        response = api_client.get(self.detail_url(99999))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_nonexistent_record_returns_404(self, admin_client, artist, genre):
        payload = {
            "album": "Ghost Album",
            "artist_id": artist.id,
            "genre_id": genre.id,
            "price": "20.00",
            "year": 2000,
        }
        response = admin_client.put(self.detail_url(99999), payload, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_record_returns_404(self, admin_client):
        response = admin_client.delete(self.detail_url(99999))

        assert response.status_code == status.HTTP_404_NOT_FOUND