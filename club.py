from player import Player

class Club:
	player_number = 0
	
	def __init__(self, club_id=None, club_name_id=None,club_name_pretty=None):
		self.club_id = club_id
		self.club_name_id = club_name_id
		self.club_name_pretty = club_name_pretty
		self.player_list = []
		
	def add_player(self, player):
		#check if a player with that name already exists
		for existing_player in self.player_list:
			if existing_player.player_id == player.player_id:
				return False
		
		#if not, add that player
		self.player_list.append(player)
		self.player_number = self.player_number + 1
		return True
		
	def list_players(self):
		#list all players
		for player in self.player_list:
			print(player.player_name_pretty)
			
	def remove_player(self, player_id):
		#remove player with a given name; deletes the last player with that name
		player_position = -1
		#find the position of the player with the given name
		for pos, value in enumerate(self.player_list):
			if value.player_id == player_id:
				player_position = pos
		
		#if a player of that name was found, delete that player
		if player_position != -1:
			del self.player_list[player_position]
			
		return player_position
		