from abc import ABC, abstractmethod
import random

from constants import BOT_NAMES, BET_LIMITS, NumberException
from deck import player_hand_cards, dealer_hand_cards


class AbstractPlayer(ABC):
    max_bet = BET_LIMITS.get('max')
    min_bet = BET_LIMITS.get('min')

    def __init__(self, name):
        self.hidden_card = False
        self.name = name
        self.player_cards = []
        self.player_money = 100
        self.player_bet = 0
        self.player_points = self.count_player_points()

    def add_card(self, card):
        return self.player_cards.append(card)

    def count_player_points(self):
        self.player_points = sum([card.points for card in self.player_cards])
        return self.player_points

    @abstractmethod
    def make_a_bet(self):
        pass

    @abstractmethod
    def hit_or_stand(self):
        pass

    @abstractmethod
    def reveal_card(self):
        pass

    def print_cards(self):
        self.player_points = self.count_player_points()
        if isinstance(self, Dealer):
            cards_to_print = player_hand_cards(*self.player_cards) if not self.hidden_card else dealer_hand_cards(*self.player_cards)
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
    def __init__(self, name='YOU'):
        super().__init__(name)

    def make_a_bet(self):
        while True:
            try:
                player_bet_input = int(input(f'\nMake your bet ({self.min_bet}$-{self.player_money}$): '))
                if not (self.min_bet <= player_bet_input <= self.max_bet) or not (player_bet_input <= self.player_money):
                    raise NumberException
            except (TypeError, AttributeError, ValueError):
                print('Can\'t accept incorrect input. Try again!')
            except NumberException:
                print('Your input is not in the accessible range. Please, try again!')
            else:
                self.player_bet = player_bet_input
                break
        print(f'{self.name} put {self.player_bet}$')
        self.player_money -= self.player_bet
        return self.player_bet

    def hit_or_stand(self):
        while True:
            try:
                player_hit_or_stand_input = input(f'\nDo you want to take one more card? (y/n): ').lower().strip()
                if player_hit_or_stand_input not in ['y', 'n']:
                    raise ValueError
            except ValueError:
                print('Invalid input. Please enter "y" or "n".')
            else:
                break

        if player_hit_or_stand_input == 'y':
            print(f'{self.name} decided to take one more card.')
            return True
        else:
            print(f'{self.name} don\'t want to take anymore card.')
            return False

    def reveal_card(self):
        pass


class BotPlayer(AbstractPlayer):

    def __init__(self):
        super().__init__(self.get_name())
        self.hidden_card = True

    def get_name(self):
        bot_name = random.choice(BOT_NAMES)
        BOT_NAMES.remove(bot_name)
        return bot_name

    def make_a_bet(self):
        self.player_bet = random.randint(self.min_bet, self.player_money)
        print(f'{self.name} put {self.player_bet}$')
        return self.player_bet

    def hit_or_stand(self):
        if self.count_player_points() > 19:
            print(f'{self.name} don\'t want to take anymore card.')
            return False
        else:
            print(f'{self.name} takes one more card.')
            return True

    def reveal_card(self):
        self.hidden_card = False
        return self.hidden_card


class Dealer(AbstractPlayer):
    def __init__(self, name='DEALER'):
        super().__init__(name)
        self.hidden_card = True

    def reveal_card(self):
        self.hidden_card = False
        return self.hidden_card

    def make_a_bet(self):
        self.player_bet = random.randint(self.min_bet, self.player_money)
        print(f'{self.name} put {self.player_bet}$')
        return self.player_bet

    def hit_or_stand(self):
        if self.count_player_points() < 17:
            print(f'{self.name} takes one more card.')
            return True
        else:
            print(f'{self.name} don\'t want to take anymore card.')
            return False
