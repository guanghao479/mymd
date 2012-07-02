from django.dispatch import Signal

friends_connected = Signal(providing_args=[])
friends_requested = Signal(providing_args=[])