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
	publisher = models.ForeignKey(Publisher)
	developer = models.ForeignKey(Developer)
	platforms = models.ManyToManyField(Platform)
	tags = models.ManyToManyField(Tag)

	def __unicode__(self):
		return self.title

	def get_platforms(self):
		return ', '.join(p.name for p in self.platforms.all())

	def get_tags(self):
		return ', '.join(t.name for t in self.tags.all())