from django.shortcuts import render
from rest_framework import generics, filters
from playlists.models import Song, Playlist
from playlists.serializers import SongSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from playlists.serializers import PlaylistSerializer
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

class SearchSongs(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = [filters.SearchFilter]
    search_fields=['^name']

class PlayListDetail(APIView):

    def post(self, request):
        username  = request.user.username
        thisUser = User.objects.filter(username=username)
        newPlaylist = Playlist(name=request.data.playlist_name, user=thisUser)
        for song_id in request.data.songs:
            thisSong = Song.objects.filter(spotify_id=song_id)
            newPlaylist.add(thisSong)
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        username = request.user.username
        thisUser = User.objects.filter(username=username)
        playlists = Playlist.objects.filter(user=thisUser)
        serialized = PlaylistSerializer(playlists, many=True)
        return Response(serialized.data)










