from actstream.managers import ActionManager, stream
from django.contrib.contenttypes.models import ContentTypes
from actstream.models import user_stream

class StreamManager(ActionManager):

    @stream
    def stream_mine(self, object, verb, time):
        return object.actor_actions