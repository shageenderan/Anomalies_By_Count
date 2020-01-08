from app.models import Frame

def create_frame(videoId, datetime, timestamp, count):
    f = Frame(video=videoId, date_time=datetime, timestamp=timestamp, count=count)
    f.save()