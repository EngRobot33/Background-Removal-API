from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    picture_id = serializers.IntegerField()
    picture = serializers.CharField()
