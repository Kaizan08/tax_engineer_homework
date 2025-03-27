import logging
import argparse
from helper_functions import (
    check_and_refill_hand,
    compare_cards,
    get_shuffled_deck,
    split_deck,
)


logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[],
)
logger = logging.getLogger()

parser = argparse.ArgumentParser()
parser.add_argument('--auto', action='store_true', help='Prevent request for user action, move game along automatically')
parser.add_argument('--output', nargs='?', const='gameplay.log', default=False, help='Auto play game and output the game results to a log file')
parser.add_argument('--suit-up', action='store_true', help='run game with "suit up" house rule')
args = parser.parse_args()


def game_comparison(function, info="", **kwargs):
    logger.info(info)
    return function(**kwargs)


def play_round(player1, player2, deal=1, reversed=False):
    '''
    Single round of gameplay, wars are considered part of the same round, and are recursively called
    '''
    if (not args.auto) and not(args.output): input('Press Enter to play')

    handle_shifting_cards_scenarios(player1, player2, deal, reversed)
    comparison = compare_cards(player1.played_cards[-1], player2.played_cards[-1], suit_up_active=(args.suit_up and deal != 4))  # check if deal is 4, if it is it's a regular war and you can't enter suit-up

    # Clean up outputs to model class
    player1.output(True if comparison == 1 else False)
    player2.output(True if comparison == 2 else False)

    # Simplified this, but could do more
    if comparison == 1:
        player1.update_wins(player2.played_cards)
    elif comparison == 2:
        player2.update_wins(player1.played_cards)
    elif comparison in [0, 3]:
        return game_comparison(play_round, player1=player1, player2=player2, deal=deal, reversed=reversed)

    return None  # no winner yet


def handle_shifting_cards_scenarios(player1, player2, deal, reversed):
    """This is to pull out logic for more getting card scenarios for all game types"""
    for _ in range(0, deal):
        if not any([any(player1.hand), any(player1.discard), any(player2.hand), any(player2.discard)]):
            # Players have played all cards in one long series of wars, just compare on the last card or draw
            # assume suit_up can't activate on this last hand
            return compare_cards(player1.played_cards[-1], player2.played_cards[-1], suit_up_active=False)

        if check_and_refill_hand(player1.hand, player1.discard): return 2
        player1.update_played_cards(player1.hand.pop(0 if reversed else -1))

        if check_and_refill_hand(player2.hand, player2.discard): return 1
        player2.update_played_cards(player2.hand.pop(0 if reversed else -1))


def play_war():
    '''
    Play game
    '''

    #setup deck and player data objects
    deck = get_shuffled_deck()
    player1, player2 = split_deck(deck, logger=logger)
    round = 1

    while(True):
        #game play loop
        assert round < 10000, "infinite loop suspected"  # if player's don't grab their own deck first when picking up cards, the game can enter infinite loops
        player1.played_cards, player2.played_cards = [], []
        logger.info(f'---- Round {round} ----')
        winner = play_round(player1, player2, deal=1)
        if winner:
            logger.info(f'Player {winner} Wins in {round} rounds!')
            break
        elif winner == 0:  # for rare case
            logger.info("Draw!")
            break

        # move cards from discard to hand if hand is empty
        if check_and_refill_hand(player1.hand, player1.discard):
            logger.info(f'Player 2 Wins in {round} rounds!')
            break

        if check_and_refill_hand(player2.hand, player2.discard):
            logger.info(f'Player 1 Wins in {round} rounds!')
            break

        round += 1


if __name__ == '__main__':
    if args.output:
        logger.addHandler(logging.FileHandler(mode='w', filename=(args.output.replace('.log', '')+'.log')))
    else:
        logger.addHandler(logging.StreamHandler())
    play_war()
