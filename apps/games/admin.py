from django.contrib import admin
from apps.games.models import Genre, Platform, Publisher, Developer, Tag, Game

class GameAdmin(admin.ModelAdmin):
	list_display=('title', 'get_platforms', 'genre', 'release_date', 'publisher', 'developer',)
	filter_horizontal=('platforms', 'tags', )

admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Publisher)
admin.site.register(Developer)
admin.site.register(Tag)
admin.site.register(Game, GameAdmin)