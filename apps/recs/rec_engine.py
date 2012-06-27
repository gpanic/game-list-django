from django.contrib.auth.models import User
from django.db import connection, transaction
import math
import re
import operator

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
	query = 'PRAGMA TABLE_INFO (' + DB_TABLE + ')'
	cursor = connection.cursor()
	table_info = list(cursor.execute(query))
	table_info = table_info[1:]
	item_ids = [int(re.split('(\d+)', c[1])[1]) for c in table_info]
	item_ids.remove(item_id)
	item_rating_sim_list = []
	for i in item_ids:
		rating = get_rating(user_id, i)
		if rating != 0:
			try:
				sim = similarity(item_id, i)
				item_rating_sim_list.append([i, rating, sim])
			except SimilarityException:
				pass
	item_rating_sim_list.sort(key=operator.itemgetter(2), reverse=True)
	if len(item_rating_sim_list) >=5:
		return item_rating_sim_list[:5]
	else:
		raise RatingException('User needs more ratings.')



def weighted_sum(user_id, item_id):
	items = get_rated_similar_items(user_id, item_id, NUM_SIMILAR_ITEMS)
	sum1 = 0
	sum2 = 0
	for item in items:
		sum1 += item[1] * item[2]
		sum2 += math.fabs(item[2])
	return sum1 / sum2


