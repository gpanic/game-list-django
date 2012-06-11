from django.db import models
from django.contrib.auth.models import User
from apps.games.models import Game

RATING = (
	(10, '10'),
	(9,' 9'),
	(8,' 8'),
	(7,' 7'),
	(6,' 6'),
	(5,' 5'),
	(4,' 4'),
	(3,' 3'),
	(2,' 2'),
	(1,' 1'),
)

STATUS = (
	(1, 'Playing'),
	(2, 'Finished'),
	(3, 'Plan to play'),
	(4, 'On hold'),
	(5, 'Dropped'),
)

class List(models.Model):
	user = models.OneToOneField(User)

	def __unicode__(self):
		return self.user.username

class ListItem(models.Model):
	game_list = models.ForeignKey(List)
	game = models.ForeignKey(Game)

	status = models.PositiveSmallIntegerField(choices=STATUS, null=True, blank=True)
	rating = models.PositiveSmallIntegerField(choices=RATING, null=True, blank=True)
	date_start = models.DateField(null=True, blank=True, verbose_name=u'Start date')
	date_finish = models.DateField(null=True, blank=True, verbose_name=u'Finish date')
	times_finished = models.IntegerField(null=True, blank=True)
	time_spent = models.PositiveIntegerField(null=True, blank=True, verbose_name=u'Total time spent')
	time_playthrough = models.PositiveIntegerField(null=True, blank=True, verbose_name=u'Time spent on first playthrough')
	money_spent = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	notes = models.TextField(blank=True)

	def __unicode__(self):
		return "{} {}".format(self.game_list.user.username, self.game.title)