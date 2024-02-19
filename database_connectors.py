import mysql.connector
from player import Player
from matchday import PlayerInMatch
from club import Club
import sys


def read_player_by_id(player_id):
	cnx = mysql.connector.connect(user='root', password='MyNewPass',
                              host='127.0.0.1',
                              database='football_data')
							  
	cursor = cnx.cursor()
	
	statement = "Select player_id, player_name_id, player_name_pretty from players where player_id = %i"%(player_id)
	
	cursor.execute(statement)
	result = cursor.fetchall()
	
	player = Player()
	
	player.player_id = result[0][0]
	player.player_name_id = result[0][1]
	player.player_name_pretty = result[0][2]
	
	cursor.close()
	cnx.close()
	
	return player
	
def read_player_by_clubid(club_id):
	cnx = mysql.connector.connect(user='root', password='MyNewPass',
                              host='127.0.0.1',
                              database='football_data')
							  
	cursor = cnx.cursor()
	
	statement = "Select player_id from player_in_club where club_id = %i"%(club_id)
	
	cursor.execute(statement)
	result_ids = cursor.fetchall()
	
	result_list = []
	
	for row in result_ids:
		player = Player()
		
		statement = "Select player_id, player_name_id, player_name_pretty from players where player_id = %i"%(row[0])
		
		print(statement)
		
		cursor.execute(statement)
		result_player = cursor.fetchall()
		
		player.player_id = result_player[0][0]
		player.player_name_id = result_player[0][1]
		player.player_name_pretty = result_player[0][2]
		
		result_list.append(player)
	
	cursor.close()
	cnx.close()
	
	return result_list

	
def read_club_by_id(club_id):
	cnx = mysql.connector.connect(user='root', password='MyNewPass',
                              host='127.0.0.1',
                              database='football_data')
							  
	cursor = cnx.cursor()
	
	statement = "Select club_id, club_name_id, club_name_pretty from clubs where club_id = %i"%(club_id)
	
	cursor.execute(statement)
	result = cursor.fetchall()
	
	club = Club()
	
	club.club_id = result[0][0]
	club.club_name_id = result[0][1]
	club.club_name_pretty = result[0][2]
	
	cursor.close()
	cnx.close()
	
	return club
	
def read_player_in_match_by_id(player_in_match_id):
	cnx = mysql.connector.connect(user='root', password='MyNewPass',
                              host='127.0.0.1',
                              database='football_data')
							  
	cursor = cnx.cursor()
	
	statement = "Select (player_id, club_id, match_id, player_status, match_date, player_position) from player_in_match where player_in_match_id = %i"%(player_in_match_id)
	
	cursor.execute(statement)
	result = cursor.fetchall()
	
	player_in_match = PlayerInMatch(player_in_match_id=player_in_match_id)
	
	player_in_match.player_id = result[0][0]
	player_in_match.club_id = result[0][1]
	player_in_match.match_id = result[0][2]
	player_in_match.player_status = result[0][3]
	player_in_match.match_date = result[0][4]
	player_in_match.player_position = result[0][5]
	
	
	return player_in_match
	
def write_player_in_match(player_in_match):
	cnx = mysql.connector.connect(user='root', password='MyNewPass',
                              host='127.0.0.1',
                              database='football_data')
							  
	cursor = cnx.cursor()
	
	statement = "Select player_id from player_in_match where player_id = {player_id} AND match_date = \"{match_date}\";" \
			.format(player_id=str(player_in_match.player_id), \
			match_date=str(player_in_match.match_date))
			
	
	
	statement = "INSERT INTO player_in_match (player_id, match_id, player_status, match_date, player_position, club_id) "\
			"VALUES ({player_id}, {match_id}, \"{player_status}\", \"{match_date}\", \"{player_position}\", {club_id})"\
			.format(\
			player_id=str(player_in_match.player_id),\
			match_id=str(player_in_match.match_id),\
			player_status=player_in_match.player_status,\
			match_date=player_in_match.match_date,\
			player_position=player_in_match.player_position,\
			club_id=str(player_in_match.club_id))
	
	cursor.execute(statement)

	cnx.commit()
	cursor.close()
	cnx.close()
	
def write_player(player):
	cnx = mysql.connector.connect(user='root', password='MyNewPass',
                              host='127.0.0.1',
                              database='football_data')
							  
	cursor = cnx.cursor()
	
	statement = "INSERT INTO players (player_id, player_name_id, player_name_pretty) "\
			"VALUES ({player_id}, \"{player_name_id}\", \"{player_name_pretty}\")"\
			.format(\
			player_id=str(player.player_id),\
			player_name_id=player.player_name_id,\
			player_name_pretty=player.player_name_pretty)
			
	#print(statement)
	
	try:
		cursor.execute(statement)
	except: 
		print("mysql error:", sys.exc_info()[0])
		
	cnx.commit()
	cursor.close()
	cnx.close()
	
def add_players_to_club(club):
	cnx = mysql.connector.connect(user='root', password='MyNewPass',
                              host='127.0.0.1',
                              database='football_data')
							  
	cursor = cnx.cursor()
	
	for player in club.player_list:
		statement = "Select club_id, player_id from player_in_club where player_id = {player_id}".format(player_id=str(player.player_id))
		cursor.execute(statement)
		result = cursor.fetchall()
		relation_exists = False
		for row in result:
			if row[0]==str(club.club_id):
				relation_exists = True
				
		if relation_exists == False:
			statement = "INSERT INTO player_in_club (player_id, club_id) \
			VALUES ({player_id}, {club_id})"\
			.format(player_id=str(player.player_id), club_id=str(club.club_id))
			cursor.execute(statement)
		
	cnx.commit()
	cursor.close()
	cnx.close()	