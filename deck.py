"""
deck.py: Defines classes related to the deck of cards for a card game.

This module includes the following classes and functions:
- Card: Represents a playing card with suit, rank, and point value.
- player_hand_cards: Function to format and print player's hand cards.
- dealer_hand_cards: Function to format and print dealer's hand cards with a hidden card.
- Deck: Represents a deck of playing cards.
"""

from itertools import product
import random

from constants import SUITS, RANKS


class Card:
    """
        Represents a playing card with suit, rank, and point value.

        Attributes:
        -----------
        - suit (str): The suit of the card.
        - rank (str): The rank of the card.
        - points (int): The point value of the card based on the game rules.
    """

    def __init__(self, suit, rank):
        """
            Initializes a new card.
        """
        self.suit = suit
        self.rank = rank
        self.points = RANKS.get(rank)


def player_hand_cards(*cards, no_hidden_card=True):
    """
        Format and print the player's hand cards.

        Parameters:
        -----------
        *cards: Variable number of Card objects representing the player's hand.
        no_hidden_card (bool): Flag indicating whether to show a hidden card for the dealer. Default is True.

        Returns:
        --------
        str: Formatted string representation of the player's hand cards.
    """

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
    """
        Format and print the dealer's hand cards with a hidden card.

        Parameters:
        -----------
        *cards: Variable number of Card objects representing the dealer's hand.

        Returns:
        --------
        str: Formatted string representation of the dealer's hand cards with a hidden card.
    """

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
    """
        Represents a deck of playing cards.

        Attributes:
        -----------
        - deck (list): List containing Card objects representing the deck of cards.

        Methods:
        --------
        - __init__: Initializes a new deck by generating and shuffling the cards.
        - _generate_deck: Generates a deck of cards using product of suits and ranks.
        - get_card: Retrieves and removes the top card from the deck.
        - __len__: Returns the number of cards remaining in the deck.
    """

    def __init__(self):
        """
            Initializes a new deck by generating and shuffling the cards.
        """
        self.deck = self._generate_deck()
        random.shuffle(self.deck)

    def _generate_deck(self):
        """
        Generates a deck of cards using the product of suits and ranks.

        Returns:
        --------
        list: List containing Card objects representing the deck of cards.
        """
        cards_pack = []
        for card_suit, card_rank in product(SUITS, RANKS):
            card = Card(suit=card_suit, rank=card_rank)
            cards_pack.append(card)
        return cards_pack

    def get_card(self):
        """
        Retrieves and removes the top card from the deck.

        Returns:
        --------
        Card: The top card from the deck.
        """
        return self.deck.pop()

    def __len__(self):
        """
        Returns the number of cards remaining in the deck.

        Returns:
        --------
        int: Number of cards remaining in the deck.
        """
        return len(self.deck)
