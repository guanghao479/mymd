from actstream.managers import ActionManager, stream

class StreamManager(ActionManager):

    @stream
    def friendstrem(self, object):
        return object.actor_actions