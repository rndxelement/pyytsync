from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import loader
from sync.models import VideoState, PlaylistVideo
import json
from datetime import datetime, timezone
from django.conf import settings
from django.db.models import Min
from googleapiclient.discovery import build
import isodate

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
    video_states = VideoState.objects.all()
    if video_states:
        print(f"Received time {video_time} from client")
        video_state = video_states[0]
        video_state.current_playtime = video_time
        video_state.save()
        return HttpResponse("Sent video time to server!")
    else:
        print("No video currently set")
        return HttpResponse("No video currently set!")

def get_vid_id(request):
    video_states = VideoState.objects.all().values()
    if video_states:
        video_id = video_states[0]['current_video_id']
        print(f"Sending {video_id} to client")
        return HttpResponse(json.dumps({'video_id': video_id}))
    else:
        print("No video ID available")
        return HttpResponse(json.dumps({'video_id': None}))

def get_vid_time(request):
    video_states = VideoState.objects.all().values()
    if video_states:
        video_time = video_states[0]['current_playtime']
        print(f"Sending time {video_time} to client")
        return HttpResponse(json.dumps({'video_time': video_time}))
    else:
        print("No video time available")
        return HttpResponse(json.dumps({'video_time': None}))

def format_duration(iso_duration):
    duration = isodate.parse_duration(iso_duration)
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes:02}:{seconds:02}"

def add_vid_to_playlist(request):
    video_id = request.GET['video_id']
    video_title = request.GET['video_title']
    cnt = PlaylistVideo.objects.all().count()

    # Build a service object for interacting with the API
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_DATA_API_KEY)

    # Call the videos.list method to retrieve video details
    response = youtube.videos().list(
        part='contentDetails',
        id=video_id
    ).execute()

    # Extracting video duration
    duration = response['items'][0]['contentDetails']['duration']
    print(f"Duration: {duration}")
    video_duration = format_duration(duration)

    playlist_video = PlaylistVideo(video_id = video_id, video_title = video_title, order_num = cnt + 1, video_duration = video_duration)
    playlist_video.save()
    return HttpResponse("Added video to playlist!")

def remove_vid_from_playlist(request):
    id = request.GET['id'];
    PlaylistVideo.objects.filter(id=id).delete();
    return HttpResponse("Deleted video from playlist!")

def get_playlist_videos(request):
    playlist_videos = PlaylistVideo.objects.all().order_by('order_num').values()
    playlist_videos = [playlist_videos[i] for i in range(len(playlist_videos))]
    return HttpResponse(json.dumps(playlist_videos))

def set_next_playlist_video(request):
    video_state = VideoState.objects.all()[0]
    last_time = video_state.last_next_playlist_video_time
    current_time = datetime.now(timezone.utc);
    allowed_delta = 5
    delta = (current_time - last_time).total_seconds()
    if delta < allowed_delta:
        return HttpResponse("Refusing to run next video because of recent request!")
    next_video = PlaylistVideo.objects.all().order_by('order_num').first()
    video_state.last_next_playlist_video_time = current_time
    video_state.current_video_id = next_video.video_id
    video_state.current_playtime = 0
    video_state.current_playlist_id = next_video.id
    video_state.save()
    PlaylistVideo.objects.filter(id=next_video.id).delete();
    return HttpResponse("Running next video from playlist!")

@csrf_exempt
def set_playlist_by_titles(request):
    titles = json.loads(request.POST['titles'])
    for idx, title in enumerate(titles):
        vid = PlaylistVideo.objects.filter(video_title=title).first()
        vid.order_num = idx
        vid.save()
    return HttpResponse("Reordered videos of playlist!")

def move_vid_to_top_of_playlist(request):
    id = request.GET['id'];
    min_id = PlaylistVideo.objects.aggregate(Min('order_num'))['order_num__min']
    video = PlaylistVideo.objects.filter(id=id)[0]
    video.order_num = min_id - 1
    video.save()
    return HttpResponse("Moved video to top of playlist!")
