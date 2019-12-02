from django.core.management.base import BaseCommand
from playlists.models import Song
import pandas as pd

class Command(BaseCommand):
    args = '<csv filename>'
    help = 'Populate database with csv file.'

    def _create_song(self,row):
        song = Song(name=row['name'],
                    tag_name=row['tag_name'],
                    playcount=row['playcount'],
                    listeners=row['listeners'],
                    artist_name=row['artist_name'],
                    danceability=row['danceability'],
                    energy=row['energy'],
                    key=row['key'],
                    loudness=row['loudness'],
                    mode = row['mode'],
                    speechiness = row['speechiness'],
                    acousticness = row['acousticness'],
                    instrumentalness = row['instrumentalness'],
                    liveness = row['liveness'],
                    valence = row['valence'],
                    tempo = row['tempo'],
                    spotify_id = row['id'],
                    duration_ms = row['duration_ms'],
                    time_signature = row['time_signature'])
        song.save()

    def handle(self, *args, **options):


        df = pd.read_csv("playlists/tracks_features_89338.csv")

        for index, row in df.iterrows():
            self._create_song(row)

