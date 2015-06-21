from django.contrib import admin
from youtuber.models import YoutubeSource


class YoutubeSourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'identifier')


admin.site.register(YoutubeSource, YoutubeSourceAdmin)
