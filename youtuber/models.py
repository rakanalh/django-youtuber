from django.db import models
from django.utils.translation import ugettext as _


class YoutubeSource(models.Model):
    TYPE_CHANNEL = 1
    TYPE_PLAYLIST = 2

    TYPES_CHOICES = (
        (TYPE_CHANNEL, _('Channel')),
        (TYPE_PLAYLIST, _('Playlist'))
    )

    name = models.CharField(max_length=250)
    type = models.SmallIntegerField(choices=TYPES_CHOICES)
    identifier = models.CharField(max_length=250)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name