from django.shortcuts import render
from rest_framework import generics, filters
from playlists.models import Song, Playlist
from playlists.serializers import SongSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from playlists.serializers import PlaylistSerializer
from rest_framework import status
from rest_framework.response import Response
import json
import pandas as pd
from playlists.filtering import Filter
from PSSA import PSSA

# Create your views here.

class SearchSongs(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = [filters.SearchFilter]
    search_fields=['^name']

class PlayListDetail(APIView):

    def post(self, request):
        print(request.body.decode('utf-8'))
        data = json.loads(request.body.decode('utf-8'))
        username  = request.user.username
        thisUser = User.objects.get(username=username)
        newPlaylist = Playlist.objects.create(name=data['playlist_name'],
                               user=thisUser)
        for song_id in data['songs']:
            print(song_id)
            thisSong = Song.objects.filter(spotify_id=song_id).first()
            newPlaylist.songs.add(thisSong)
        print("CREATED PLAYLIST")
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        username = request.user.username
        thisUser = User.objects.get(username=username)
        playlists = Playlist.objects.filter(user=thisUser)
        serialized = PlaylistSerializer(playlists, many=True)
        return Response(serialized.data)

class Filtering(APIView):

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        #parameters:
        username = request.user.username
        thisUser = User.objects.get(username=username)
        thisPlaylist = Playlist.objects.get(user=thisUser)
        songQuerySet = thisPlaylist.songs.all()
        songsDF = pd.DataFrame(list(songQuerySet.values()))
        filter = Filter(songsDF)
        filteredDF = filter.run()

        #print(filteredDF.head())


        vsv = data['vsv']
        vse = data['vse']
        vev = data['vev']
        vee = data['vee']
        duration = data['duration']

        vector_start = (vsv, vse)
        vector_end = (vev,vee)

        pssaObj = PSSA(songsDF, filteredDF, vector_start, vector_end, duration)
        songList, artistList, genreList, VList, Elist = pssaObj.run()
        outDict = {'songList':songList,
                   'artistList':artistList,
                   'genereList':genreList,
                   'VList':VList,
                   'EList':Elist}
        serialized = json.dumps(outDict)
        return Response(outDict)










