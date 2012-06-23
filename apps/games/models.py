from django.db import models
from django.contrib.auth.models import User

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

class Genre(models.Model):
	name = models.CharField(max_length=200, unique=True)
	description = models.TextField(blank=True)

	def __unicode__(self):
		return self.name

class Platform(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return self.name

class Company(models.Model):
	name = models.CharField(max_length=200, unique=True)
	website = models.URLField(max_length=100, blank=True)

	def __unicode__(self):
		return self.name

	def games_released(self):
		games = list(self.game_developer_set.all())
		games.extend(list(self.game_publisher_set.all()))
		games = list(set(games))
		return len(games)

	class Meta:
		verbose_name_plural = 'Companies'

class Tag(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return self.name

class Game(models.Model):
	title = models.CharField(max_length=200)
	summary = models.TextField(blank=True)
	release_date = models.DateField()
	genre = models.ForeignKey(Genre)
	publisher = models.ForeignKey(Company, related_name='game_publisher_set')
	developer = models.ForeignKey(Company, related_name='game_developer_set')
	platforms = models.ManyToManyField(Platform)
	tags = models.ManyToManyField(Tag)

	def __unicode__(self):
		return self.title

	def get_platforms(self):
		return ', '.join(p.name for p in self.platforms.all())

	def get_tags(self):
		return ', '.join(t.name for t in self.tags.all())