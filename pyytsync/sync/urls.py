from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('set-vid-id', views.set_vid_id, name='set-vid-id'),
        path('set-vid-time', views.set_vid_time, name='set-vid-time'),
        path('get-vid-id', views.get_vid_id, name='get-vid-id'),
        path('get-vid-time', views.get_vid_time, name='get-vid-time'),
        path('add-vid-to-playlist', views.add_vid_to_playlist, name='add-vid-to-playlist'),
        path('remove-vid-from-playlist', views.remove_vid_from_playlist, name='remove-vid-from-playlist'),
        path('get-playlist-videos', views.get_playlist_videos, name='get-playlist-videos'),
        path('set-next-playlist-video', views.set_next_playlist_video, name='set-next-playlist-video'),
        path('set-playlist-by-titles', views.set_playlist_by_titles, name='set-playlist-by-titles'),
] 
