from club import Club
from player import Player
import requests
from bs4 import BeautifulSoup
import mysql.connector
from matchday import PlayerInMatch
from database_connectors import read_club_by_id
from database_connectors import read_player_by_clubid
from database_connectors import write_player
from database_connectors import read_player_by_id
from database_connectors import write_player_in_match
from database_connectors import add_players_to_club
from transfermarket_scraper import parse_player_matches
from transfermarket_scraper import parse_club_squad

club = read_club_by_id(5)
club_squad = parse_club_squad(club, "2020")

for res in club_squad:
	club.add_player(res)

add_players_to_club(club)

matchres_list = []
for player in club.player_list:
	write_player(player)
	
	temp_matchlist = parse_player_matches(player, club.club_id)
	for match in temp_matchlist:
		write_player_in_match(match)