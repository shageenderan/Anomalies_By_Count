from rest_framework import serializers
from .models import Frame

class frameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = ['title', 'datetime', 'count']