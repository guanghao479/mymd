from django.db.models import Manager

class DiaryManager(Manager):
    """Returns all diaries."""

    def published(self):
        return self.get_query_set().filter(status__gte=2, publish_date__lte=datetime.now())
