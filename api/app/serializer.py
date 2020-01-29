from rest_framework import serializers
from .models import Frame, Video

"""
This file contains the serializer classes that allows for simplified conversion between Python object and 
JSON defined objects
"""
class frameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = ['id', 'video', 'frame_number', 'date_time', 'count', 'timestamp', 'anomaly']

    def to_representation(self, instance):
        representation = super(frameSerializer, self).to_representation(instance)
        if representation['date_time'] is not None:
            representation['date_time'] = instance.date_time.strftime("%Y-%m-%dT%H:%M:%S")
        return representation


class videoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'url', 'isUrl', 'fileName']
