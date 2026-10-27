from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank = True, default='')
    image_url = models.URLField(blank = True, default='')

    class Meta:
        ordering = ['id']

    def __str__(self):
            return self.name

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

class Record(models.Model):
    album = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT, related_name='records')
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='records')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.PositiveIntegerField()
    cover_image = models.URLField(blank=True, default='')
    stock_quantity = models.PositiveIntegerField(default=0)
    tracklist = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.artist.name}- {self.album}"