from django.db import models
from datetime import datetime, timezone

class VideoState(models.Model):

    current_video_id = models.CharField(max_length=50, null=True)
    current_playtime = models.FloatField(null=True)
    current_playlist_id = models.IntegerField(null=True)
    last_next_playlist_video_time = models.DateTimeField(default=datetime.now(timezone.utc))

class PlaylistVideo(models.Model):

    video_id = models.CharField(max_length=50)
    video_title = models.CharField(max_length=500, null=True)
    order_num = models.IntegerField(null=True)
