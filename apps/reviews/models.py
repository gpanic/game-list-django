from django.db import models
from django.contrib.auth.models import User

from apps.games.models import Game
from apps.games.models import RATING

class Review(models.Model):
	author = models.ForeignKey(User)
	game = models.ForeignKey(Game)

	date_created = models.DateField(auto_now_add=True, verbose_name=u'Created')
	rating = models.PositiveSmallIntegerField(choices=RATING)
	content = models.TextField()

	def __unicode__(self):
		return "Review {} {}".format(self.author.username, self.game.title)

	class Meta:
		unique_together = ('author', 'game')