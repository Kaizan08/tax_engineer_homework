import random
from models import Player

def get_shuffled_deck():
    '''
    Generate Standard 52 card deck, 1-10 / J / Q / K, with 4 different suits
    '''
    SUITS = ('c', 'd', 'h', 's')
    CARDS = tuple(map(str, range(1, 11))) + ('J', 'Q', 'K')
    deck = [card+suit for suit in SUITS for card in CARDS]
    random.shuffle(deck)
    return deck

def split_deck(deck, logger):
    '''Give half a deck to each player
    player 2 get's larger pile if there are an odd number of cards
    '''
    player1 = Player('P1', logger, deck[:len(deck)//2], [])
    player2 = Player('P2', logger, deck[len(deck) - len(player1.hand):], [])
    return player1, player2

def map_card_to_numeric(card):
    '''Turn String values of cards into numeric representations for comparison'''
    if card == 'Joker': return None
    suitless = card[:-1]
    if suitless == 'J': return 11
    elif suitless == 'Q': return 12
    elif suitless == 'K': return 13
    else: return int(suitless) if int(suitless) != 1 else 14  # aces high

def compare_cards(card_1, card_2, suit_up_active=False, with_advantage=False):
    '''
    return
        0 if they're the same
        1 if card_1 is greater than card_2
        2 if card_1 is less than card_2
        3 if cards are the same suit, and playing 'suit_up'
    '''
    numeric_1 = map_card_to_numeric(card_1)
    numeric_2 = map_card_to_numeric(card_2)
    if numeric_1 == numeric_2: return 0
    elif suit_up_active and (card_1[-1] == card_2[-1]): return 3
    elif with_advantage and (card_1[0] == 'K' and card_2[0] == 'Q'): return 8  # Player1 would be K refactor if time
    elif with_advantage and (card_1[0] == 'Q' and card_2[0] == 'K'): return 9  # Player2 would be K refactor if time
    elif numeric_1 > numeric_2: return 1
    elif numeric_1 < numeric_2: return 2
    raise Exception(f"Comparison detected something unexpected: {card_1} vs. {card_2}")

def compare_cards_with_advantage(card_1, card_2, with_advantage=False):
    """Refactor out the suit_up and this function to more appropriate and more DRY"""
    numeric_1 = map_card_to_numeric(card_1)
    numeric_2 = map_card_to_numeric(card_2)
    if numeric_1 == numeric_2: return 0
    elif with_advantage and (card_1[0] == 'K' and card_2[0] == 'Q'): return 8  # Player1 would be K refactor if time
    elif with_advantage and (card_1[0] == 'Q' and card_2[0] == 'K'): return 9
    elif numeric_1 > numeric_2: return 1
    elif numeric_1 < numeric_2: return 2
    raise Exception(f"Comparison detected something unexpected: {card_1} vs. {card_2}")

def check_and_refill_hand(hand, discard):
    '''
    If hand is empty, move discard pile to hand
    return True if the player loses
    '''
    if not any(hand):  # need to refill hand or see if the game ends
        if not any(discard):  # out of cards, we know player 2 has cards so player 1 loses
            return True
        else:  # pick up discard pile
            discard.reverse()
            while any(discard):
                hand.append(discard.pop())
    return False