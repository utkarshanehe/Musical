from django.db import models
from django.urls import reverse


class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.artist + "  -  " + self.album_title


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_file = models.FileField()
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.album.pk})


