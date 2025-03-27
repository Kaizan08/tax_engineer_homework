import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helper_functions import compare_cards


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