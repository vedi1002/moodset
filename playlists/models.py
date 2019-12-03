from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Song(models.Model):
    name = models.CharField(max_length=500)
    tag_name = models.CharField(max_length=250)
    playcount = models.IntegerField()
    listeners = models.IntegerField()
    artist_name = models.CharField(max_length=500)
    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.IntegerField()
    loudness = models.FloatField()
    mode = models.IntegerField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    spotify_id = models.CharField(max_length=250)
    duration_ms = models.IntegerField()
    time_signature = models.IntegerField()

    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=250)
    songs = models.ManyToManyField(Song)
    user = models.ForeignKey(User, on_delete=models.CASCADE)






