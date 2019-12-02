from rest_framework import serializers
from playlists.models import Song, Playlist

class SongSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('spotify_id', 'name')
        model = Song

class PlaylistSerializer(serializers.ModelSerializer):
    songs = SongSerializer(read_only=True,many=True)

    class Meta:
        model = Playlist
        fields = ('name', 'songs', 'user')