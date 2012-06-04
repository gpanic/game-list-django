from django.db import models

class Genre(models.Model):
	name=models.CharField(max_length=200)
	description=models.TextField(blank=True)

	def __unicode__(self):
		return self.name

class Platform(models.Model):
	name=models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Publisher(models.Model):
	name=models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class Developer(models.Model):
	name=models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class Tag(models.Model):
	name=models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Game(models.Model):
	title=models.CharField(max_length=200)
	summary=models.TextField(blank=True)
	release_date=models.DateField()
	genre=models.ForeignKey(Genre)
	platform=models.ForeignKey(Platform)
	publisher=models.ForeignKey(Publisher)
	developer=models.ForeignKey(Developer)
	tags=models.ManyToManyField(Tag)

	def __unicode__(self):
		return self.title