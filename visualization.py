import mysql.connector
import altair as alt
from vega_datasets import data
import pandas as pd

from player import Player
from club import Club
from matchday import PlayerInMatch
from database_connectors import read_club_by_id
from database_connectors import read_player_by_clubid
from transfermarket_scraper import parse_player_matches
from database_connectors import read_player_by_id

def test_vis(club_id=5, date = "2020-08-30"):
	# status name definitions
	in_match = "Played"
	on_bench = "on the bench "
	healthy = ["not in squad", "Red card suspension", "Indirect card suspension", "Yellow card suspension", "No eligibility", "Suspension through sports court", "Fitness"]
	
	cnx = mysql.connector.connect(user='root', password='MyNewPass',
                              host='127.0.0.1',
                              database='football_data')
							  
	cursor = cnx.cursor()
	
	#set up empty arrays for results
	date_array = []
	status_array = []
	player_number_array = []
	
	# get list of matchdays in given season with given club_id
	statement = "select distinct match_date from player_in_match where (club_id = \"{club_id}\" and match_date > \"{match_date}\")"\
			.format(club_id=str(club_id), match_date=str(date))
	 
	cursor.execute(statement)
	date_list = cursor.fetchall()
	
	# loop through matchdays
	for match_date in date_list:
		# get info for all players that could have played on this match day
		statement = "select player_status from player_in_match where (match_date = \"{match_date}\" and club_id = {club_id});"\
				.format(match_date=str(match_date[0]), club_id=str(club_id))
		
		cursor.execute(statement)
		status_list = cursor.fetchall()		
				
		# set up counters for stati
		status_counter_played = 0
		status_counter_bench = 0
		status_counter_healthy = 0
		status_counter_injured = 0
		
		# get status and add to corresponding counter
		for entry in status_list:
			entry_string = entry[0]
			if entry_string == in_match:
				status_counter_played += 1
			elif entry_string == on_bench:
				status_counter_bench += 1
			elif entry_string in healthy:
				status_counter_healthy += 1
			else: 
				status_counter_injured += 1
		
		# fill arrays for given matchday
		date_array.extend([match_date, match_date, match_date, match_date])
		status_array.extend(["Played", "On the bench", "Healthy", "Injured"])
		player_number_array.extend([status_counter_played, status_counter_bench, status_counter_healthy, status_counter_injured])
	
	source = pd.DataFrame({'date': date_array, 
			'number_players': player_number_array,
			'status': status_array})

	chart = alt.Chart(source).mark_bar().encode(
		x='date',
		y='sum(number_players)',
		color='status'
	)
	chart.save("chart_milan.html")

	
if __name__ == "__main__":
	test_vis()