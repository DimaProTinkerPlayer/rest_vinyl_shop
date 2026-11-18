import logging

from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Artist, Genre, Record
from shop.permissions import IsAdminOrReadOnly, IsAuthenticatedOrReadOnlyCustom
from shop.serializers import (
    ArtistSerializer,
    GenreSerializer,
    RecordDetailSerializer,
    RecordListSerializer,
)

logger = logging.getLogger(__name__)


# ARTISTS


class ArtistListCreateAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        tags=["Artists"],
        summary="Отримати список виконавців",
        responses={200: ArtistSerializer(many=True)},
    )
    def get(self, request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Artists"],
        summary="Створити нового виконавця (лише Admin)",
        request=ArtistSerializer,
        responses={
            201: ArtistSerializer,
            400: OpenApiExample(
                "Помилка валідації",
                value={"error": {"name": ["This field is required."]}},
                response_only=True,
                status_codes=["400"],
            ),
            403: OpenApiExample(
                "Недостатньо прав",
                value={"detail": "Доступ заборонено. Ця дія дозволена лише адміністраторам."},
                response_only=True,
                status_codes=["403"],
            ),
        },
    )
    def post(self, request):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            artist = serializer.save()
            logger.info(
                'Адміністратор "%s" створив виконавця ID=%d ("%s")',
                request.user.username,
                artist.id,
                artist.name,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(
            'Помилка валідації при створенні виконавця: %s',
            serializer.errors,
        )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class ArtistDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            logger.warning("Виконавця з ID=%s не знайдено", pk)
            return None

    @extend_schema(
        tags=["Artists"],
        summary="Отримати деталі виконавця",
        responses={200: ArtistSerializer},
    )
    def get(self, request, pk):
        artist = self.get_object(pk)
        if not artist:
            return Response(
                {"error": f"Виконавця з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Artists"],
        summary="Оновити виконавця (лише Admin)",
        request=ArtistSerializer,
        responses={200: ArtistSerializer},
    )
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
            logger.info(
                'Адміністратор "%s" оновив виконавця ID=%d',
                request.user.username,
                pk,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        tags=["Artists"],
        summary="Видалити виконавця (лише Admin)",
        responses={204: None},
    )
    def delete(self, request, pk):
        artist = self.get_object(pk)
        if not artist:
            return Response(
                {"error": f"Виконавця з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        records_count = artist.records.count()
        if records_count > 0:
            logger.warning(
                'Спроба видалити виконавця ID=%d ("%s"), за яким закріплено %d платівок',
                pk,
                artist.name,
                records_count,
            )
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
        logger.info(
            'Адміністратор "%s" видалив виконавця ID=%d',
            request.user.username,
            pk,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


# GENRES


class GenreListCreateAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        tags=["Genres"],
        summary="Отримати список жанрів",
        responses={200: GenreSerializer(many=True)},
    )
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Genres"],
        summary="Створити новий жанр (лише Admin)",
        request=GenreSerializer,
        responses={201: GenreSerializer},
    )
    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            genre = serializer.save()
            logger.info(
                'Адміністратор "%s" створив жанр ID=%d ("%s")',
                request.user.username,
                genre.id,
                genre.name,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(
            "Помилка валідації при створенні жанру: %s",
            serializer.errors,
        )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class GenreDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Genre.objects.get(pk=pk)
        except Genre.DoesNotExist:
            logger.warning("Жанр з ID=%s не знайдено", pk)
            return None

    @extend_schema(
        tags=["Genres"],
        summary="Отримати деталі жанру",
        responses={200: GenreSerializer},
    )
    def get(self, request, pk):
        genre = self.get_object(pk)
        if not genre:
            return Response(
                {"error": f"Жанр з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Genres"],
        summary="Оновити жанр (лише Admin)",
        request=GenreSerializer,
        responses={200: GenreSerializer},
    )
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
            logger.info(
                'Адміністратор "%s" оновив жанр ID=%d',
                request.user.username,
                pk,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        tags=["Genres"],
        summary="Видалити жанр (лише Admin)",
        responses={204: None},
    )
    def delete(self, request, pk):
        genre = self.get_object(pk)
        if not genre:
            return Response(
                {"error": f"Жанр з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        records_count = genre.records.count()
        if records_count > 0:
            logger.warning(
                'Спроба видалити жанр ID=%d ("%s"), до якого прив\'язано %d платівок',
                pk,
                genre.name,
                records_count,
            )
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
        logger.info(
            'Адміністратор "%s" видалив жанр ID=%d',
            request.user.username,
            pk,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


# RECORDS


class RecordListCreateAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        tags=["Records"],
        summary="Отримати список платівок",
        description=(
            "Повертає перелік вінілових платівок із підтримкою пошуку, "
            "фільтрації за виконавцем/жанром, сортування та пагінації. Доступно всім."
        ),
        parameters=[
            OpenApiParameter(name="search", description="Пошук за назвою альбому", required=False, type=str),
            OpenApiParameter(name="artist_id", description="Фільтр за ID виконавця", required=False, type=int),
            OpenApiParameter(name="genre_id", description="Фільтр за ID жанру", required=False, type=int),
            OpenApiParameter(
                name="sort",
                description="Сортування (price, -price, year, -year, price_asc, price_desc, year_desc)",
                required=False,
                type=str,
            ),
            OpenApiParameter(name="page", description="Номер сторінки для пагінації", required=False, type=int),
            OpenApiParameter(name="limit", description="Кількість записів на сторінку", required=False, type=int),
        ],
        responses={200: RecordListSerializer(many=True)},
    )
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
                logger.warning(
                    "Некоректні параметри пагінації: page=%s, limit=%s",
                    page_param,
                    limit_param,
                )

        logger.debug("Запит списку платівок (query_params=%s)", dict(request.query_params))
        serializer = RecordListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Records"],
        summary="Створити нову платівку",
        description="Додає нову платівку до каталогу. Вимагає JWT-автентифікації та прав адміністратора.",
        request=RecordDetailSerializer,
        responses={
            201: RecordDetailSerializer,
            400: OpenApiExample(
                "Помилка валідації",
                value={"error": {"price": ["A valid number is required."]}},
                response_only=True,
                status_codes=["400"],
            ),
            401: OpenApiExample(
                "Неавторизований запит",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            403: OpenApiExample(
                "Недостатньо прав",
                value={"detail": "Доступ заборонено. Ця дія дозволена лише адміністраторам."},
                response_only=True,
                status_codes=["403"],
            ),
        },
        examples=[
            OpenApiExample(
                "Приклад створення платівки",
                value={
                    "album": "The Dark Side of the Moon",
                    "artist_id": 1,
                    "genre_id": 1,
                    "price": "34.99",
                    "year": 1973,
                    "cover_image": "https://example.com/dsotm.jpg",
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request):
        serializer = RecordDetailSerializer(data=request.data)
        if serializer.is_valid():
            record = serializer.save()
            logger.info(
                'Користувач "%s" створив платівку ID=%d ("%s")',
                request.user.username,
                record.id,
                record.album,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(
            'Помилка валідації при створенні платівки користувачем "%s": %s',
            request.user.username,
            serializer.errors,
        )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class RecordDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Record.objects.select_related("artist", "genre").get(pk=pk)
        except Record.DoesNotExist:
            logger.warning("Платівку з ID=%s не знайдено", pk)
            return None

    @extend_schema(
        tags=["Records"],
        summary="Отримати деталі платівки",
        description="Повертає повну інформацію про конкретну платівку за її ID. Доступно всім.",
        responses={
            200: RecordDetailSerializer,
            404: OpenApiExample(
                "Платівку не знайдено",
                value={"error": "Платівку з ID 999 не знайдено."},
                response_only=True,
                status_codes=["404"],
            ),
        },
    )
    def get(self, request, pk):
        record = self.get_object(pk)
        if not record:
            return Response(
                {"error": f"Платівку з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = RecordDetailSerializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Records"],
        summary="Оновити платівку",
        description="Повністю оновлює дані платівки за ID. Вимагає прав адміністратора.",
        request=RecordDetailSerializer,
        responses={
            200: RecordDetailSerializer,
            400: OpenApiExample(
                "Помилка валідації",
                value={"error": {"year": ["Ensure this value is greater than or equal to 1900."]}},
                response_only=True,
                status_codes=["400"],
            ),
            401: OpenApiExample(
                "Неавторизований запит",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            403: OpenApiExample(
                "Недостатньо прав",
                value={"detail": "Доступ заборонено. Ця дія дозволена лише адміністраторам."},
                response_only=True,
                status_codes=["403"],
            ),
            404: OpenApiExample(
                "Платівку не знайдено",
                value={"error": "Платівку з ID 999 не знайдено."},
                response_only=True,
                status_codes=["404"],
            ),
        },
    )
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
            logger.info(
                'Користувач "%s" оновив платівку ID=%d',
                request.user.username,
                pk,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(
            'Помилка валідації при оновленні платівки ID=%d: %s',
            pk,
            serializer.errors,
        )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        tags=["Records"],
        summary="Видалити платівку",
        description="Видаляє платівку за ID. Вимагає прав адміністратора.",
        responses={
            204: None,
            401: OpenApiExample(
                "Неавторизований запит",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            403: OpenApiExample(
                "Недостатньо прав",
                value={"detail": "Доступ заборонено. Ця дія дозволена лише адміністраторам."},
                response_only=True,
                status_codes=["403"],
            ),
            404: OpenApiExample(
                "Платівку не знайдено",
                value={"error": "Платівку з ID 999 не знайдено."},
                response_only=True,
                status_codes=["404"],
            ),
        },
    )
    def delete(self, request, pk):
        record = self.get_object(pk)
        if not record:
            return Response(
                {"error": f"Платівку з ID {pk} не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )
        record_album = record.album
        record.delete()
        logger.info(
            'Користувач "%s" видалив платівку ID=%d ("%s")',
            request.user.username,
            pk,
            record_album,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)