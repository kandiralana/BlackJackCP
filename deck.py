from itertools import product
import random

from constants import SUITS, RANKS


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.points = RANKS.get(rank)


def player_hand_cards(*cards, no_hidden_card=True):
    printed_lines = [[] for _ in range(9)]

    for index, card in enumerate(cards):
        if card.rank == '10':
            rank = card.rank
            space = ''
        else:
            rank = card.rank[0]
            space = ' '

        suit = SUITS.get(card.suit)

        printed_lines[0].append('┌─────────────┐')
        printed_lines[1].append('│{}{}           │'.format(rank, space))
        printed_lines[2].append('│             │')
        printed_lines[3].append('│             │')
        printed_lines[4].append('│      {}      │'.format(suit))
        printed_lines[5].append('│             │')
        printed_lines[6].append('│             │')
        printed_lines[7].append('│           {}{}│'.format(space, rank))
        printed_lines[8].append('└─────────────┘')

    player_cards_to_print = []
    for index, line in enumerate(printed_lines):
        player_cards_to_print.append(''.join(printed_lines[index]))

    if no_hidden_card:
        return '\n'.join(player_cards_to_print)
    else:
        return player_cards_to_print


def dealer_hand_cards(*cards):
    hidden_card = [['┌─────────────┐'],
                   ['│░░░░░░░░░░░░░│'],
                   ['│░░░░░░░░░░░░░│'],
                   ['│░░░░░░░░░░░░░│'],
                   ['│░░░░░░░░░░░░░│'],
                   ['│░░░░░░░░░░░░░│'],
                   ['│░░░░░░░░░░░░░│'],
                   ['│░░░░░░░░░░░░░│'],
                   ['└─────────────┘']]

    cards_except_hidden = player_hand_cards(*cards[1:], no_hidden_card=False)
    for index, line in enumerate(cards_except_hidden):
        hidden_card[index].append(line)

    for index, line in enumerate(hidden_card):
        hidden_card[index] = ''.join(line)

    return '\n'.join(hidden_card)


class Deck:
    def __init__(self):
        self.deck = self._generate_deck()
        random.shuffle(self.deck)

    def _generate_deck(self):
        cards_pack = []
        for card_suit, card_rank in product(SUITS, RANKS):
            card = Card(suit=card_suit, rank=card_rank)
            cards_pack.append(card)
        return cards_pack

    def get_card(self):
        return self.deck.pop()

    def __len__(self):
        return len(self.deck)

