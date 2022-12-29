from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from sync.models import VideoState, PlaylistVideo
import json
from datetime import datetime, timezone
from django.conf import settings

def index(request):
    video_state =  VideoState.objects.all()
    if len(video_state) == 0:
        video_state = VideoState()
        video_state.save()
    else:
        video_state = video_state.values()[0]

    template = loader.get_template('sync/base.html')
    context = {"YOUTUBE_DATA_API_KEY": settings.YOUTUBE_DATA_API_KEY, "video_id": video_state['current_video_id']}
    return HttpResponse(template.render(context, request))

def set_vid_id(request):
    video_id = request.GET['video_id']
    video_state = VideoState.objects.all()[0]
    print(f"Received {video_id} from client")
    video_state.current_video_id = video_id
    video_state.save()
    return HttpResponse("Sent video to server!")

def set_vid_time(request):
    video_time = request.GET['video_time']
    video_state = VideoState.objects.all()[0]
    print(f"Received time {video_time} from client")
    video_state.current_playtime = video_time
    video_state.save()
    return HttpResponse("Sent video time to server!")

def get_vid_id(request):
    video_id = VideoState.objects.all().values()[0]['current_video_id']
    print(f"Sending {video_id} to client")
    return HttpResponse(json.dumps({'video_id': video_id}))

def get_vid_time(request):
    video_time = VideoState.objects.all().values()[0]['current_playtime']
    print(f"Sending time {video_time} to client")
    return HttpResponse(json.dumps({'video_time': video_time}))

def add_vid_to_playlist(request):
    video_id = request.GET['video_id']
    playlist_video = PlaylistVideo(video_id = video_id)
    playlist_video.save()
    return HttpResponse("Added video to playlist!")

def remove_vid_from_playlist(request):
    id = request.GET['id'];
    PlaylistVideo.objects.filter(id=id).delete();
    return HttpResponse("Deleted video from playlist!")

def get_playlist_videos(request):
    playlist_videos = PlaylistVideo.objects.all().values()
    playlist_videos = [playlist_videos[i] for i in range(len(playlist_videos))]
    print(playlist_videos)
    return HttpResponse(json.dumps(playlist_videos))

def set_next_playlist_video(request):
    video_state = VideoState.objects.all()[0]
    last_time = video_state.last_next_playlist_video_time
    current_time = datetime.now(timezone.utc);
    allowed_delta = 5
    delta = (current_time - last_time).total_seconds()
    if delta < allowed_delta:
        return HttpResponse("Refusing to run next video because of recent request!")
    next_video = PlaylistVideo.objects.all().order_by('id').first()
    video_state.last_next_playlist_video_time = current_time
    video_state.current_video_id = next_video.video_id
    video_state.current_playtime = 0
    video_state.current_playlist_id = next_video.id
    video_state.save()
    PlaylistVideo.objects.filter(id=next_video.id).delete();
    return HttpResponse("Running next video from playlist!")

