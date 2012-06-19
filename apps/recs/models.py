from django.db import models
from django.contrib.auth.models import User

from apps.games.models import Game

class UserRec(models.Model):
	author = models.ForeignKey(User)
	game1 = models.ForeignKey(Game, related_name='userrec_game1', verbose_name=u'Game 1')
	game2 = models.ForeignKey(Game, related_name='userrec_game2', verbose_name=u'Game 2')

	content = models.TextField()
	date_created = models.DateField(auto_now_add=True, verbose_name=u'Created')

	def __unicode__(self):
		return 'UserRec {} {} {}'.format(self.author, self.game1.title, self.game2.title)