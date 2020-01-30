# Django imports
from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from background_task import background

# Local file imports
from .models import Frame, Video
from .serializer import frameSerializer, videoSerializer
from mask.script.objectdetection import check_video_exists, object_detection_url, object_detection_file

# External library imports
import datetime
import pytz
import requests

# This file contains the functions necessary to create Django views used by the URL for parsing API requests made.

utcTimezone = pytz.utc


# API logic for URL /frames/
class frameList(APIView):

    # GET - Returns list of all frames in DB
    def get(self, request):
        frames = Frame.objects.all()
        serializer = frameSerializer(frames, many=True)
        return Response(serializer.data)

    # POST - Create a new frame and add it to DB
    def post(self, request):
        serializer = frameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API logic for URL /frame/filter(?date=YYYYmmdd(20200127). No date given will return all frames on any date
class frameDate(APIView):

    # GET - returns list of frames which occurs on the date given
    def get(self, request):
        date = request.GET.get('date', None)
        dateObject = datetime.datetime.strptime(date, '%Y%m%d')
        dateObject = utcTimezone.localize(dateObject)
        frames = Frame.objects.filter(date_time__date=dateObject.date())
        serializer = frameSerializer(frames, many=True)
        return Response(serializer.data)


# API logic for URL /frame/date(?to=YYYYmmddHHMMSS(20200127000000)&from=YYYYmmddHHMMSS(20190127235959)). Can use both,
# either, or no query arguments.
class frameDateRange(APIView):

    # GET - returns the list of frames falling within the dates given in the query arguments
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
        frames = Frame.objects.filter(date_time__range=[startObject, endObject])
        serializer = frameSerializer(frames, many=True)
        return Response(serializer.data)


# API logic for URL /frame/timestamp(?from=number(int or float)&to=number(int or float). Can use both,
# either, or no query arguments.
class frameTimestampRange(APIView):

    # GET - returns the list of frames falling within the timestamp attribute of the frame.
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


# API logic for URL /frame/{id:number}/. Provides basic CRUD operations for singular Frame objects.
class frameDetail(APIView):

    # GET - returns the frame object with the given id
    def get(self, request, pk):
        try:
            frame = Frame.objects.get(pk=pk)
            serializer = frameSerializer(frame)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Frame.DoesNotExist:
            raise Http404

    # PUT - updates the object with the given id with values given in the API request body
    def put(self, request, pk):
        try:
            frame = Frame.objects.get(pk=pk)
            serializer = frameSerializer(frame, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Frame.DoesNotExist:
            raise Http404

    # DELETE - deletes the object with the given id from the DB
    def delete(self, request, pk):
        try:
            frame = Frame.objects.get(pk=pk)
            frame.delete()
            return Response(status=status.HTTP_200_OK)
        except Frame.DoesNotExist:
            raise Http404


# API logic for URL /video/
class videoList(APIView):

    # GET - returns list of all videos in the DB
    def get(self, request):
        video = Video.objects.all()
        serializer = videoSerializer(video, many=True)
        return Response(serializer.data)


# API logic for URL /video/{id:number}/. Provides basic CRUD operations for singular Video objects.
class videoDetail(APIView):

    # GET - returns the Video object with the given id
    def get(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
            serializer = videoSerializer(video)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Video.DoesNotExist:
            raise Http404

    # PUT - updates the Video with the given id wth the values provided in the API request
    def put(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
            serializer = videoSerializer(video, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Video.DoesNotExist:
            raise Http404

    # DELETE - deletes the Video object with the given id from the DB.
    def delete(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
            video.delete()
            return Response(status=status.HTTP_200_OK)
        except Video.DoesNotExist:
            raise Http404


# API logic for the URL /video/{id:number}/frame(?to=number&from=number). Can use both, either, or no query arguments.
class videoFrameDetail(APIView):

    # GET - return a list of frames from the video with the given video id.
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Frame.DoesNotExist:
            raise HttpResponse(status=200)


# API logic for url /video/submit/
class detectSubmit(APIView):

    # POST - creates a new queue task to run object detection using video provided by the link. Returns the video id of
    # the object created for future API requests
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


# Django background task placed on the queue to be called when scheduled
@background(schedule=0)
def detection_queue_url(url, idVal):
    print("URL:{}".format(url), datetime.datetime.now())
    object_detection_url(url, idVal)


# Django background task placed on the queue to be called when scheduled
@background(schedule=0)
def detection_queue_file(filename, idVal):
    print("File:{}".format(filename), datetime.datetime.now())
    object_detection_file(filename, idVal)
