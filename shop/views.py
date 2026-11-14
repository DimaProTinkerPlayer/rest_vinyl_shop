from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Artist, Genre, Record
from .serializers import (
    ArtistSerializer,
    GenreSerializer,
    RecordDetailSerializer,
    RecordListSerializer,
)


# ARTISTS

class ArtistListCreateAPIView(APIView):
    def get(self, request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ArtistDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            return None

    def get(self, request, pk):
        artist = self.get_object(pk)
        if not artist:
            return Response(
                {"error": f"Виконавця з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        artist = self.get_object(pk)
        if not artist:
            return Response(
                {"error": f"Виконавця з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ArtistSerializer(artist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        artist = self.get_object(pk)
        if not artist:
            return Response(
                {"error": f"Виконавця з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        records_count = artist.records.count()
        if records_count > 0:
            return Response(
                {
                    "error": (
                        f"Не можна видалити виконавця '{artist.name}', "
                        f"оскільки за ним закріплено {records_count} платівок."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        artist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# GENRES

class GenreListCreateAPIView(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GenreDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Genre.objects.get(pk=pk)
        except Genre.DoesNotExist:
            return None

    def get(self, request, pk):
        genre = self.get_object(pk)
        if not genre:
            return Response(
                {"error": f"Жанр з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        genre = self.get_object(pk)
        if not genre:
            return Response(
                {"error": f"Жанр з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        genre = self.get_object(pk)
        if not genre:
            return Response(
                {"error": f"Жанр з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        records_count = genre.records.count()
        if records_count > 0:
            return Response(
                {
                    "error": (
                        f"Неможливо видалити жанр '{genre.name}', "
                        f"оскільки до нього прив'язано {records_count} платівок."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# RECORDS

class RecordListCreateAPIView(APIView):
    def get(self, request):
        queryset = Record.objects.select_related("artist", "genre").all()

        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(album__icontains=search)

        artist_id = request.query_params.get("artist_id")
        if artist_id:
            queryset = queryset.filter(artist_id=artist_id)

        genre_id = request.query_params.get("genre_id")
        if genre_id:
            queryset = queryset.filter(genre_id=genre_id)

        sort = request.query_params.get("sort")
        if sort:
            valid_sort_fields = {
                "price": "price",
                "-price": "-price",
                "year": "year",
                "-year": "-year",
                "price_asc": "price",
                "price_desc": "-price",
                "year_desc": "-year",
            }
            if sort in valid_sort_fields:
                queryset = queryset.order_by(valid_sort_fields[sort])

        page_param = request.query_params.get("page")
        limit_param = request.query_params.get("limit")

        if limit_param:
            try:
                limit = int(limit_param)
                page = int(page_param) if page_param else 1
                if limit > 0 and page > 0:
                    start = (page - 1) * limit
                    end = start + limit
                    queryset = queryset[start:end]
            except ValueError:
                pass

        serializer = RecordListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RecordDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RecordDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Record.objects.select_related("artist", "genre").get(pk=pk)
        except Record.DoesNotExist:
            return None

    def get(self, request, pk):
        record = self.get_object(pk)
        if not record:
            return Response(
                {"error": f"Платівку з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = RecordDetailSerializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        record = self.get_object(pk)
        if not record:
            return Response(
                {"error": f"Платівку з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = RecordDetailSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        record = self.get_object(pk)
        if not record:
            return Response(
                {"error": f"Платівку з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)