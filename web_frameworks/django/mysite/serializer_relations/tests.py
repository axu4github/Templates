from django.test import TestCase

from .serializers import AlbumSerializer


class NestedRelationshipsTest(TestCase):

    def test_create_album(self):
        data = {
            'album_name': 'The Grey Album',
            'artist': 'Danger Mouse',
            'track': {'order': 1, 'title': 'Public Service', 'duration': 245},
        }

        serializer = AlbumSerializer(data=data)
        serializer.is_valid()
        album = serializer.save()

        self.assertEqual(album.track.order, data["track"]["order"])
