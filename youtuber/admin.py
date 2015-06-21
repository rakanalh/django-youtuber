from django.contrib import admin
from youtuber.models import YoutubeSource


class YoutubeSourceAdmin(admin.ModelAdmin):
    pass


admin.site.register(YoutubeSource, YoutubeSourceAdmin)
