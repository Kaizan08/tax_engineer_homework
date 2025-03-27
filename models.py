"""Different models as the game is altered"""

class Player:
    def __init__(self, name, logger, hand, discard = [],):
        self.hand = hand
        self.discard = discard
        self.played_cards = []
        self.wins = 0
        self.name = name
        self.logger = logger

    def update_wins(self, played_cards):
        self.wins += 1
        self.discard = self.played_cards + played_cards

    def get_wins(self):
        return self.wins

    def update_played_cards(self, played_cards):
        self.played_cards.append(played_cards)

    def output(self, win=False):
        self.logger.info(
            f"{self.name}: H:{str(len(self.hand)).ljust(2)} | D:{str(len(self.discard)).ljust(2)} | {self.played_cards}{'*' if win else ' '}")