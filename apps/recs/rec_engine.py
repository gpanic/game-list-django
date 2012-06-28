from django.contrib.auth.models import User
from django.db import connection, transaction
import math
import operator
import re

from apps.games.models import Game

DB_TABLE = 'recs_user_rating_matrix'
NUM_SIMILAR_ITEMS = 5

class SimilarityException(Exception):
	pass

class RatingException(Exception):
	pass

def create_matrix():
	games = Game.objects.all()
	ids = [g.id for g in games]

	query = 'CREATE TABLE ' + DB_TABLE + ' (user_id INTEGER NOT NULL PRIMARY KEY UNIQUE, ' + 'game_{} INTEGER, ' * (len(games)-1) + 'game_{} INTEGER)'
	query = query.format(*ids)

	cursor = connection.cursor()
	cursor.execute(query)
	transaction.commit_unless_managed()

def populate_matrix():
	cursor = connection.cursor()
	users = User.objects.filter(is_active=True)
	for user in users:
		games = Game.objects.all().count()
		query = 'INSERT INTO ' + DB_TABLE + ' VALUES (' + str(user.id) + ', ' + '0, '*(games-1) + '0)'
		cursor.execute(query)
		transaction.commit_unless_managed()

		list_items = user.list.listitem_set.all()

		query = 'UPDATE ' + DB_TABLE + ' SET '
		s = []
		for i, item in enumerate(list_items):
			if item.rating:
				s.append('game_'+ str(item.game.id) + '=' + str(item.rating))
		query += ', '.join(s) + ' WHERE user_id=' + str(user.id)
		cursor.execute(query)
		transaction.commit_unless_managed()

def drop_matrix():
	query = 'DROP TABLE ' + DB_TABLE

	cursor = connection.cursor()
	cursor.execute(query)
	transaction.commit_unless_managed()

def get_rating(user_id, item_id):
	query = 'SELECT game_' + str(item_id) + ' FROM ' + str(DB_TABLE) + ' WHERE user_id=' + str(user_id)
	cursor = connection.cursor()
	cursor.execute(query)
	return int(cursor.fetchone()[0])

def get_user_average_rating(user_id):
	query = 'SELECT * FROM ' + str(DB_TABLE) + ' WHERE user_id=' + str(user_id)
	cursor = connection.cursor()
	cursor.execute(query)
	user_row = cursor.fetchone()
	user_row = filter(lambda a: a != 0, user_row)
	return float(sum(user_row[1:])) / float(len(user_row[1:]))

def get_all_item_ids():
	query = 'PRAGMA TABLE_INFO (' + DB_TABLE + ')'
	cursor = connection.cursor()
	table_info = list(cursor.execute(query))
	table_info = table_info[1:]
	item_ids = [int(re.split('(\d+)', c[1])[1]) for c in table_info]
	return item_ids

def get_unrated_ids(user_id):
	item_ids = get_all_item_ids()
	unrated_ids = []
	for i in item_ids:
		if get_rating(user_id, i) == 0:
			unrated_ids.append(i)
	return unrated_ids

def similarity(item1_id, item2_id):
	query = 'SELECT user_id, game_1 FROM ' + DB_TABLE + ' WHERE game_' + str(item1_id) + '<>0 AND game_' + str(item2_id) + '<> 0'
	cursor = connection.cursor()
	rows = list(cursor.execute(query))
	user_ids = [r[0] for r in rows]

	sim1 = 0
	sim2 = 0
	sim3 = 0
	if user_ids:
		for i in user_ids:
			user_average_rating = get_user_average_rating(i)
			rating1 = get_rating(i, item1_id)
			rating2 = get_rating(i, item2_id)
			
			sim1 += (rating1 - user_average_rating) * (rating2 - user_average_rating)
			sim2 += (rating1 - user_average_rating)**2
			sim3 += (rating2 - user_average_rating)**2
		sim2 = math.sqrt(sim2)
		sim3 = math.sqrt(sim3)

		sim = float(sim1) / (float(sim2) * float(sim3))
		return sim
	else:
		raise SimilarityException('No user pair has rated this item.')


def get_rated_similar_items(user_id, item_id, number):
	item_ids = get_all_item_ids()
	item_ids.remove(item_id)
	item_rating_sim_list = []
	for i in item_ids:
		rating = get_rating(user_id, i)
		if rating != 0:
			try:
				sim = similarity(item_id, i)
				if sim >= 0:
					item_rating_sim_list.append([i, rating, sim])
			except SimilarityException:
				pass
	item_rating_sim_list.sort(key=operator.itemgetter(2), reverse=True)
	return item_rating_sim_list[:5]



def weighted_sum(user_id, item_id):
	items = get_rated_similar_items(user_id, item_id, NUM_SIMILAR_ITEMS)
	sum1 = 0
	sum2 = 0
	for item in items:
		sum1 += item[1] * item[2]
		sum2 += math.fabs(item[2])
	return sum1 / sum2

def get_recommendations(user_id, number):
	item_ids = get_unrated_ids(user_id)
	item_weighted_sums = [weighted_sum(user_id, i) for i in item_ids]
	recs = zip(item_ids, item_weighted_sums)
	recs.sort(key=operator.itemgetter(1), reverse=True)
	return recs[:number]