from club import Club
from player import Player
import requests
from bs4 import BeautifulSoup
import mysql.connector
from matchday import PlayerInMatch

def class_empty(in_class):
	return (in_class == "") or (in_class == "bg_rot_20") or  (in_class == "bg_gelb_20")

def parse_player_matches(player, club_id):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
	URL = "https://www.transfermarkt.us/"+str(player.player_name_id)+"/leistungsdatendetails/spieler/"+str(player.player_id)+"/saison//verein/" + str(club_id) + "/liga/0/wettbewerb//pos/0/trainer_id/0"
	
	request = requests.get(URL, headers = headers)
	
	parsed_content = BeautifulSoup(request.content, 'html.parser')
	
	result_list = []
	
	for tr in parsed_content.find_all('tr',class_=class_empty):
		match = PlayerInMatch()
		match.player_id = player.player_id
		#print("----new match----")
		current = tr.td
		temp = current.a["href"]
		comp = temp[1:temp[1:].find('/')+1]
		#competition
		#print("competition: "+comp)
		current = current.find_next('td')
		#date
		#print("date: "+str(current.string))
		pre_string_date = current.string
		year = "20" + pre_string_date[pre_string_date.rfind("/")+1:]
		month = pre_string_date[:pre_string_date.find("/")]
		if len(month) == 1:
			month = "0" + month
			
		day = pre_string_date[pre_string_date.find("/")+1:pre_string_date.rfind("/")]
		if len(day) == 1:
			day = "0" + day
			
		correct_date = year + "-" + month + "-" + day
		match.match_date = str(correct_date)
		current = current.find_next('td')
		#Location
		#print("location: "+str(current.string))
		current = current.find_next('td')
		#own team
		temp = current.a["href"]
		cut_off_front = temp[temp.find("verein/")+7:]
		own_team = cut_off_front[:cut_off_front.find("/")]
		match.club_id = own_team
		#print("own team: " + own_team)
		current = current.find_next('td', class_="zentriert no-border-rechts")
		#opponent team
		temp = current.a["href"]
		opponent_team = temp[1:temp[1:].find('/')+1]
		#print("opponent team: " + opponent_team)
		current = current.find_next('td')
		current = current.find_next('td')
		#print("match id: " + current.a["id"])
		match.match_id = current.a["id"]
		current = current.find_next('span')
		#result
		#print("result: " + str(current.string))
		current = current.find_next('td')
		if "colspan" in current.attrs.keys():
			#status 
			if current.span:
				#print("status: " + str(current.span["title"]))
				match.player_status = str(current.span["title"])
			else:
				#print("status: " + str(current.string))
				match.player_status = str(current.string)
		else:
			#position
			match.player_status = "Played"
			#print("position: " + str(current.a.string))
			match.player_position = str(current.a.string)
			
		result_list.append(match)

	return result_list

def parse_club_squad(club,season):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
	URL = "https://www.transfermarkt.us/"+club.club_name_id+"/kader/verein/"+str(club.club_id)+"/plus/0/galerie/0?saison_id="+season
	output = requests.get(URL, headers = headers)
	url_content = output.content
	parsed_content = BeautifulSoup(url_content, 'html.parser')
	
	result_list = []
	
	for bit in parsed_content.find_all("a",attrs={"class": "spielprofil_tooltip"}):
		href_value = bit.get("href")
		player_name_id = href_value[1:href_value[1:].find("/")+1]
		temp_player = Player(bit.get("id"), player_name_id, bit.get("title"))
		result_list.append(temp_player)
		
	return result_list
		
		

def transfermarket_scraper():
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
	URL = 'https://www.transfermarkt.us/as-roma/kader/verein/12/plus/0/galerie/0?saison_id=2020'
	output = requests.get(URL, headers = headers)
	url_content = output.content
	parsed_content = BeautifulSoup(url_content, 'html.parser')
	
	club = Club("AS Roma")
	
	cnx = mysql.connector.connect(user='root', password='MyNewPass',
                              host='127.0.0.1',
                              database='football_data')
	cursor = cnx.cursor()
	
	for bit in parsed_content.find_all("a",attrs={"class": "spielprofil_tooltip"}):
		href_value = bit.get("href")
		player_name_id = self.name_id = href_value[1:href_value[1:].find("/")+1]
		temp_player = Player(bit.get("title"), player_name_id, bit.get("id"))
		temp_player.update_href_matchRes()
		temp_player.club_id = 12
		club.add_player(temp_player)
		
	for temp_player in club.player_list:
		
		mysql_statement_1 = ("INSERT INTO players "
			"(player_id, player_name, player_href, tm_href_matchresults) "
			"VALUES (%(player_id)s, %(player_name)s, %(player_href)s, %(tm_href_matchresults)s)")
		data_1 = {
			'player_id': temp_player.player_id,
			'player_name': temp_player.name,
			'player_href': temp_player.href,
			'tm_href_matchresults': temp_player.tm_href_matchresults,
		}
		cursor.execute(mysql_statement_1, data_1)
		
		mysql_statement_2 = ("INSERT INTO player_in_club "
				"(player_id, club_id) "
				"VALUES (%(player_id)s, %(club_id)s)")
			  
		data_2 = {
			'player_id': temp_player.player_id,
			'club_id': 12
		}
		
		cursor.execute(mysql_statement_2, data_2)
		
		
	cnx.commit()
	cnx.close()
	

	
if __name__ == "__main__":
	transfermarket_scraper()