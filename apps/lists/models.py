from django.db import models
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from django.db.models.signals import post_save

from apps.games.models import Game
from apps.games.models import RATING

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

	def get_games(self):
		games = []
		for listitem in self.listitem_set.all():
			games.append(listitem.game)
		return games

	def get_time_spent(self):
		list_items = self.listitem_set.all()
		time = 0
		for item in list_items:
			if item.time_spent:
				time += item.time_spent
		return time

	def get_money_spent(self):
		list_items = self.listitem_set.all()
		money = 0
		for item in list_items:
			if item.money_spent:
				money += item.money_spent
		return money

	def get_average_rating(self):
		list_items = self.listitem_set.all()
		ratings = []
		for item in list_items:
			if item.rating:
				ratings.append(item.rating)
		if ratings:
			return float(sum(ratings)) / float(len(ratings))
		else:
			return 0

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
		return "ListItem {} {}".format(self.game_list.user.username, self.game.title)

	class Meta:
		unique_together = ('game_list', 'game')

def create_list(sender, instance, created, **kwargs):
	if created:
		List.objects.create(user=instance)

post_save.connect(create_list, sender=User)