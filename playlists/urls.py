from django.urls import path
from playlists.views import SearchSongs, PlayListDetail



urlpatterns = [
    path('songs/', SearchSongs.as_view() ,name='search_results'),
    path('playlists/', PlayListDetail.as_view(), name='playlist_details')
]