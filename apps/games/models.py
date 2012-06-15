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
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)

	def __unicode__(self):
		return self.name

class Platform(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Publisher(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class Developer(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Game(models.Model):
	title = models.CharField(max_length=200)
	summary = models.TextField(blank=True)
	release_date = models.DateField()
	genre = models.ForeignKey(Genre)
	platform = models.ForeignKey(Platform)
	publisher = models.ForeignKey(Publisher)
	developer = models.ForeignKey(Developer)
	tags = models.ManyToManyField(Tag)

	def __unicode__(self):
		return self.title

class Review(models.Model):
	author = models.ForeignKey(User)
	game = models.ForeignKey(Game)

	date_created = models.DateField(auto_now_add=True, verbose_name=u'Created')
	rating = models.PositiveSmallIntegerField(choices=RATING)

	class Meta:
		unique_together = ('author', 'game')