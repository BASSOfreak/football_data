import unittest
from club import Club
from player import Player

class TestClub(unittest.TestCase):
	def test_AddPlayer(self):
		club = Club("AS Roma")
		player = Player("Francesco Totti")
		club.add_player(player)
		player = Player("Daniele DeRossi")
		club.add_player(player)
		club.add_player(player)
		self.assertEqual(club.player_number,2,"should be 2")
	
	def test_RemovePlayer(self):
		club = Club("AS Roma")
		player = Player("Francesco Totti")
		club.add_player(player)
		player = Player("Daniele DeRossi")
		club.remove_player("Daniele DeRossi")
		self.assertEqual(club.player_number,1,"should be 1")
		
	def test_RemoveNonexistantPlayer(self):
		club = Club("AS Roma")
		player = Player("Francesco Totti")
		club.add_player(player)
		player = Player("Daniele DeRossi")
		club.remove_player("Daniele DeRossi")
		self.assertEqual(club.remove_player("Daniele DeRossi"),-1,"should be -1")

if __name__ == '__main__':
    unittest.main()
