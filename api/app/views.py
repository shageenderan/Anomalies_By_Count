from django.shortcuts import render

from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Frame, Video
from .serializer import frameSerializer, videoSerializer
import datetime
import pytz
import requests
from mask.script.objectdetection import check_video_exists, object_detection_url, object_detection_file
from background_task import background

# Create your views here.
utcTimezone = pytz.utc

fileExtensions = {
    "x-flv": ".flv",
    "mp4": ".mp4",
    "quicktime": ".mov",
    "x-msvideo": ".avi",
    "x-ms-wmv": ".wmv"
}

class frameList(APIView):

    def get(self, request):
        frames = Frame.objects.all()
        serializer = frameSerializer(frames, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = frameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class frameDate(APIView):
    def get(self, request):
        date = request.GET.get('date', None)
        dateObject = datetime.datetime.strptime(date, '%Y%m%d')
        dateObject = utcTimezone.localize(dateObject)
        frames = Frame.objects.filter(date_time__date=dateObject.date())
        serializer = frameSerializer(frames, many=True)
        return Response(serializer.data)


class frameDateRange(APIView):
    def get(self, request):
        start = request.GET.get('from', None)
        end = request.GET.get('to', None)
        if start is None:
            startObject = datetime.datetime(1970, 1, 1)
        else:
            startObject = datetime.datetime.strptime(start, '%Y%m%d%H%M%S')
        if end is None:
            endObject = datetime.datetime.now()
        else:
            endObject = datetime.datetime.strptime(end, '%Y%m%d%H%M%S')
        startObject = utcTimezone.localize(startObject)
        endObject = utcTimezone.localize(endObject)
        frames = Frame.objects.filter(date_time__range=[startObject, endObject])
        serializer = frameSerializer(frames, many=True)
        return Response(serializer.data)


class frameTimestampRange(APIView):
    def get(self, request):
        start = request.GET.get('from', None)
        end = request.GET.get('to', None)
        if start is None:
            startObject = -1
        else:
            startObject = float(start)
        if end is None:
            frames = Frame.objects.filter(timestamp__gte=startObject)
        else:
            endObject = float(end)
            frames = Frame.objects.filter(timestamp__range=[startObject, endObject])
        serializer = frameSerializer(frames, many=True)
        return Response(serializer.data)


class frameDetail(APIView):
    def get_object(self, pk):
        try:
            return Frame.objects.get(pk=pk)
        except Frame.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        frame = self.get_object(pk)
        serializer = frameSerializer(frame)
        return Response(serializer.data)

    def post(self, request):
        serializer = frameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        frame = self.get(request, pk)
        serializer = frameSerializer(frame, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        frame = self.get(request, pk)
        frame.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class videoList(APIView):
    def get(self, request):
        video = Video.objects.all()
        serializer = videoSerializer(video, many=True)
        return Response(serializer.data)


class videoDetail(APIView):
    def get_object(self, pk):
        try:
            return Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        video = self.get_object(pk)
        serializer = videoSerializer(video)
        return Response(serializer.data)

    def post(self, request):
        serializer = videoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        video = self.get(request, pk)
        serializer = videoFrameDetail(video, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        video = self.get(request, pk)
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class videoFrameDetail(APIView):
    def get(self, request, videoPK):
        try:
            frames = Frame.objects.filter(video=videoPK)
            start = request.GET.get('from', None)
            end = request.GET.get('to', None)
            if start is None:
                startObject = -1
            else:
                startObject = float(start)
            if end is None:
                frames = frames.filter(timestamp__gte=startObject)
            else:
                endObject = float(end)
                frames = frames.filter(timestamp__range=[startObject, endObject])
            serializer = frameSerializer(frames, many=True)
            return Response(serializer.data)
        except Frame.DoesNotExist:
            raise HttpResponse(status=202)


class detectSubmit(APIView):

    def post(self, request):
        serializer = videoSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data.get('isUrl'):
                req = requests.head(serializer.validated_data.get('url'))
                if req.ok:
                    serializer.save()
                    detection_queue_url(serializer.data['url'], serializer.data['id'])
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(data="{'error':'URL invalid'}", status=status.HTTP_400_BAD_REQUEST)
            else:
                if check_video_exists(serializer.validated_data.get('fileName')):
                    serializer.save()
                    detection_queue_file(serializer.data['fileName'], serializer.data['id'])
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(data="{'error':'File does not exist'}", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@background(schedule=0)
def detection_queue_url(url, idVal):
    print("URL:{}".format(url), datetime.datetime.now())
    object_detection_url(url, idVal)


@background(schedule=0)
def detection_queue_file(filename, idVal):
    print("File:{}".format(filename), datetime.datetime.now())
    object_detection_file(filename, idVal)
