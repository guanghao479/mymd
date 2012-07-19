from django.db.models import Manager

class ExperiencePublishManager(Manager):
    """Returns the all posts."""

    def published(self):
        return self.get_query_set().filter(status__gte=2, publish_date__lte=datetime.now())
