from datetime import datetime
from rest_framework import serializers

from .models import Artist, Genre, Record

class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ('id', 'name',"bio", "image_url")

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name')

class RecordListSerializer(serializers.ModelSerializer):

    artist = serializers.CharField(source='artist.name', read_only=True)
    genre = serializers.CharField(source='genre.name', read_only=True)

    class Meta:
        model = Record
        fields = ['id','album', 'artist', 'genre', 'price', 'year', 'cover_image']

class RecordDetailSerializer(serializers.ModelSerializer):
    artist_id = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all(), source='artist')
    genre_id = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), source='genre')

    artist = serializers.CharField(source='artist.name', read_only=True)
    genre = serializers.CharField(source='genre.name', read_only=True)

    class Meta:
        model = Record
        fields = ['id', 'album', 'artist_id','artist','genre_id', 'genre', 'price', 'year', 'cover_image','stock_quantity',"tracklist"]

    def validate_year(self, value):
        current_year = datetime.now().year
        if value < 1800 or value > current_year + 1:
            raise serializers.ValidationError(f"Рік має бути в межах від 1800 до {current_year + 1}.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Ціна не можу бути від'ємною.")
        return value

    def validate_tracklist(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Трекліст має бути списком рядків.")
        return value