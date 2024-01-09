"""
players.py: Defines player classes for the Blackjack game.

This module includes the following classes:
- AbstractPlayer: Abstract base class for all player types.
- Player: Represents the human player in the game.
- BotPlayer: Represents a computer-controlled bot player in the game.
- Dealer: Represents the dealer in the game.
"""

from abc import ABC, abstractmethod
import random

from constants import BOT_NAMES, BET_LIMITS, NumberException
from deck import player_hand_cards, dealer_hand_cards


class AbstractPlayer(ABC):
    """
    Abstract base class for all player types in the Blackjack game.

    Attributes:
    -----------
    - max_bet (int): Maximum allowed bet amount.
    - min_bet (int): Minimum allowed bet amount.

    Methods:
    --------
    - __init__: Initializes a new player with default attributes.
    - add_card: Adds a card to the player's hand.
    - count_player_points: Calculates and returns the total points of the player's hand.
    - make_a_bet: Abstract method for making a bet.
    - hit_or_stand: Abstract method for deciding whether to hit or stand.
    - reveal_card: Abstract method for revealing a card.
    - print_cards: Prints the player's hand cards.
    """
    max_bet = BET_LIMITS.get('max')
    min_bet = BET_LIMITS.get('min')

    def __init__(self, name):
        """
        Initializes a new player with default attributes.

        Parameters:
        -----------
        - name (str): The name of the player.
        """
        self.hidden_card = False
        self.name = name
        self.player_cards = []
        self.player_money = 100
        self.player_bet = 0
        self.player_points = self.count_player_points()

    def add_card(self, card):
        """
        Adds a card to the player's hand.

        Parameters:
        -----------
        - card: The card object to be added to the player's hand.
        """
        return self.player_cards.append(card)

    def count_player_points(self):
        """
        Calculates and returns the total points of the player's hand.

        Returns:
        --------
        int: The total points of the player's hand.
        """
        self.player_points = sum([card.points for card in self.player_cards])
        return self.player_points

    @abstractmethod
    def make_a_bet(self):
        """
        Abstract method for making a bet.
        """
        pass

    @abstractmethod
    def hit_or_stand(self):
        """
        Abstract method for deciding whether to hit or stand.

        Returns:
        --------
        bool: True if the player decides to hit, False if the player decides to stand.
        """
        pass

    @abstractmethod
    def reveal_card(self, status):
        """
        Abstract method for revealing a card.
        """
        pass

    def clear_cards(self):
        """
        Clears player's hand cards.

        Returns:
        --------
        list: empty list.
        """
        return self.player_cards.clear()

    def deal_cards(self, deck_cards):
        for _ in range(2):
            self.add_card(deck_cards.get_card())
        return self.player_cards

    def print_cards(self):
        """
        Prints the player's hand cards.

        Returns:
        --------
        str: Formatted string representation of the player's hand cards.
        """
        self.player_points = self.count_player_points()
        if isinstance(self, Dealer):
            cards_to_print = player_hand_cards(*self.player_cards) if not self.hidden_card else dealer_hand_cards(
                *self.player_cards)
            return cards_to_print
        elif isinstance(self, Player):
            cards_to_print = player_hand_cards(*self.player_cards)
            return cards_to_print
        elif isinstance(self, BotPlayer):
            if not self.hidden_card:
                cards_to_print = player_hand_cards(*self.player_cards)
                return cards_to_print
            else:
                return False


class Player(AbstractPlayer):
    """
    Represents the human player in the Blackjack game.

    Methods:
    --------
    - __init__: Initializes a new human player.
    - make_a_bet: Takes user input to determine the bet amount.
    - hit_or_stand: Takes user input to decide whether to hit or stand.
    - reveal_card: Not implemented for the human player.
    """

    def __init__(self, name='YOU'):
        """
        Initializes a new human player.

        Parameters:
        -----------
        - name (str): The name of the human player.
        """
        super().__init__(name)

    def make_a_bet(self):
        """
        Takes user input to determine the bet amount.

        Returns:
        --------
        int: The bet amount chosen by the human player.
        """
        while True:
            try:
                player_bet_input = int(input(f'➡️ Make your bet ({self.min_bet}$-{self.player_money}$): '))
                if not (self.min_bet <= player_bet_input <= self.max_bet) or not (
                        player_bet_input <= self.player_money):
                    raise NumberException
            except (TypeError, AttributeError, ValueError):
                print('‼️Can\'t accept incorrect input. Try again!')
            except NumberException:
                print('‼️Your input is not in the accessible range. Please, try again!')
            else:
                self.player_bet = player_bet_input
                break
        print(f'{self.name} put {self.player_bet}$')
        self.player_money -= self.player_bet
        return self.player_bet

    def hit_or_stand(self):
        """
        Takes user input to decide whether to hit or stand.

        Returns:
        --------
        bool: True if the human player decides to hit, False if the human player decides to stand.
        """
        while True:
            try:
                player_hit_or_stand_input = input(f'➡️ Your have {self.player_points} points.'
                                                  f'\nDo you want to take one more card? (y/n): ').lower().strip()
                if player_hit_or_stand_input not in ['y', 'n']:
                    raise ValueError
            except ValueError:
                print('‼️Invalid input. Please enter "y" or "n".')
            else:
                break

        if player_hit_or_stand_input == 'y':
            print(f'{self.name} decided to take one more card.')
            return True
        else:
            print(f'{self.name} don\'t want to take anymore card.')
            return False

    def reveal_card(self, status):
        """
        Not implemented for the human player.
        """
        pass


class BotPlayer(AbstractPlayer):
    """
    Represents a computer-controlled bot player in the Blackjack game.

    Methods:
    --------
    - __init__: Initializes a new bot player.
    - get_name: Randomly selects and returns a bot name.
    - make_a_bet: Randomly determines the bet amount for the bot player.
    - hit_or_stand: Decides whether to hit or stand based on the bot's strategy.
    - reveal_card: Reveals the hidden card for the bot player.
    """

    def __init__(self):
        """
        Initializes a new bot player.
        """
        super().__init__(self.get_name())
        self.hidden_card = True

    def get_name(self):
        """
        Randomly selects and returns a bot name.

        Returns:
        --------
        str: A randomly selected bot name.
        """
        bot_name = random.choice(BOT_NAMES)
        BOT_NAMES.remove(bot_name)
        return bot_name

    def make_a_bet(self):
        """
        Randomly determines the bet amount for the bot player.

        Returns:
        --------
        int: The randomly determined bet amount for the bot player.
        """
        self.player_bet = random.randint(self.min_bet, self.player_money)
        self.player_money -= self.player_bet
        print(f'{self.name} put {self.player_bet}$')
        return self.player_bet

    def hit_or_stand(self):
        """
        Decides whether to hit or stand based on the bot's strategy.

        Returns:
        --------
        bool: True if the bot player decides to hit, False if the bot player decides to stand.
        """
        if self.count_player_points() > 19:
            print(f'{self.name} don\'t want to take anymore card.')
            return False
        else:
            print(f'{self.name} takes one more card.')
            return True

    def reveal_card(self, status):
        """
        Reveals the hidden card for the bot player.

        Returns:
        --------
        bool: True after revealing the hidden card.
        """
        self.hidden_card = status
        return self.hidden_card


class Dealer(AbstractPlayer):
    """
    Represents the dealer in the Blackjack game.

    Methods:
    --------
    - __init__: Initializes a new dealer.
    - reveal_card: Reveals the hidden card for the dealer.
    - make_a_bet: Randomly determines the bet amount for the dealer.
    - hit_or_stand: Decides whether to hit or stand based on the dealer's strategy.
    """

    def __init__(self, name='DEALER'):
        """
        Initializes a new dealer.

        Parameters:
        -----------
        - name (str): The name of the dealer.
        """
        super().__init__(name)
        self.hidden_card = True

    def reveal_card(self, status):
        """
        Reveals the hidden card for the dealer.

        Returns:
        --------
        bool: True after revealing the hidden card.
        """
        self.hidden_card = status
        return self.hidden_card

    def make_a_bet(self):
        """
        Randomly determines the bet amount for the dealer.

        Returns:
        --------
        int: The randomly determined bet amount for the dealer.
        """
        self.player_bet = random.randint(self.min_bet, self.player_money)
        self.player_money -= self.player_bet
        print(f'{self.name} put {self.player_bet}$')
        return self.player_bet

    def hit_or_stand(self):
        """
        Decides whether to hit or stand based on the dealer's strategy.

        Returns:
        --------
        bool: True if the dealer decides to hit, False if the dealer decides to stand.
        """
        if self.count_player_points() < 17:
            print(f'{self.name} takes one more card.')
            return True
        else:
            print(f'{self.name} don\'t want to take anymore card.')
            return False
