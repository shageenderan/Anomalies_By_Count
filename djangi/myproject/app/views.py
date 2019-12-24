from django.shortcuts import render

from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Frame
from .serializer import frameSerializer

# Create your views here.

class frameList(APIView):

    def get(self, request):
        frames = Frame.objects.all()
        serializer = frameSerializer(frames, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = frameSerializer(date = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class frameDetail(APIView):
    def get_object(self, pk):
        try:
            return Frame.objects.get(pk=pk)
        except Frame.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = frameSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk):
        frame = self.get(request, pk)
        serializer = frameSerializer(frame, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        snippet = self.get(request, pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
