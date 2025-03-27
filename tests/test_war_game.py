import unittest
import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from helper_functions import compare_cards
from war_game import play_round
from models import Player

logger = logging.getLogger()

class TestPlayRound(unittest.TestCase):

    def test_comparison_equal_one(self):
        """Player 1 wins round because Ace of Diamonds beats Jack of Spades."""
        player_1_cards = "1d"
        player_2_cards = "Js"
        comparison = compare_cards(player_1_cards, player_2_cards)
        self.assertEqual(comparison, 1)

    def test_comparison_equal_two(self):
        """Player 2 wins round because King beats Jack"""
        player_1_cards = "Jd"
        player_2_cards = "Ks"
        comparison = compare_cards(player_1_cards, player_2_cards)
        self.assertEqual(comparison, 2)

    def test_comparison_equal_zero(self):
        """Both players have the same number of cards regardless of suit, so War"""
        player_1_cards = "9c"
        player_2_cards = "9s"
        comparison = compare_cards(player_1_cards, player_2_cards)
        self.assertEqual(comparison, 0)

    def test_comparison_equal_three(self):
        """Both players have the same suit, so draw two more cards then compare"""
        player_1_cards = "10s"
        player_2_cards = "9s"
        comparison = compare_cards(player_1_cards, player_2_cards, suit_up_active=True)
        self.assertEqual(comparison, 3)

    def test_play_round_player1_wins(self):
        player1 = Player("P1", logger, ["1d"], discard = [])
        player2 = Player("P2", logger, ["Js"], discard=[])
        play_round(player1, player2, deal=1)
        self.assertEqual(player1.wins, 1)

    def test_play_round_player2_wins(self):
        player1 = Player("P1", logger, ["Js"], discard=[])
        player2 = Player("P2", logger, ["1d"], discard=[])
        play_round(player1, player2, deal=1)
        self.assertEqual(player2.wins, 1)
        self.assertEqual(player1.wins, 0)

    def test_play_round_player2_wins_war(self):
        player1 = Player("P1", logger, ['Jc', 'Qc', '5c', '3c'], discard=[])
        player1.played_cards = ["9d"]
        player2 = Player("P2", logger, ['Qs', 'Jd', '8c', '2h'], discard=[])
        player2.played_cards = ["8s"]
        play_round(player1, player2, deal=4)
        self.assertEqual(player2.wins, 1)

    def test_play_round_player1_wins_suit_up(self):
        player1 = Player("P1", logger, ['Qc', 'Qc', '5c'], discard=[])
        player1.played_cards = ["9d"]
        player2 = Player("P2", logger, ['9s', 'Jd', '8c'], discard=[])
        player2.played_cards = ["8s"]
        play_round(player1, player2, deal=2)
        self.assertEqual(player1.wins, 1)
