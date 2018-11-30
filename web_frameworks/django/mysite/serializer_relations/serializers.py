from rest_framework import serializers

from .models import Track, Album


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('order', 'title', 'duration')


class AlbumSerializer(serializers.ModelSerializer):
    track = TrackSerializer(many=False)

    class Meta:
        model = Album
        fields = ('album_name', 'artist', 'track')

    def create(self, validated_data):
        track_data = validated_data.pop('track')
        album = Album.objects.create(**validated_data)
        # for track_data in tracks_data:
        Track.objects.create(album=album, **track_data)
        return album
