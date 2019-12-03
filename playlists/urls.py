from django.urls import path
from playlists.views import SearchSongs, PlayListDetail, Filtering



urlpatterns = [
    path('songs/', SearchSongs.as_view() ,name='search_results'),
    path('playlists/', PlayListDetail.as_view(), name='playlist_details'),
    path('generate/', Filtering.as_view(), name='playlist_generator')
]