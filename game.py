"""
game.py: Defines classes and functions for the main Blackjack game.

This module includes the following classes and functions:
- Game: Represents the main game controller.
"""

from deck import Deck
from players import Dealer, BotPlayer, Player
from constants import BOT_PLAYERS_LIMITS, NumberException
import time
from random import shuffle


class Game:
    """
        Represents the main game controller for Blackjack.

        Attributes:
        -----------
        - max_players_count (int): Maximum number of bot players allowed in the game.
        - min_players_count (int): Minimum number of bot players allowed in the game.

        Methods:
        --------
        - __init__: Initializes a new game by creating a deck, dealer, and player instances.
        - clear_cards: Clears player's hand cards and deals two new cards.
        - reset_game: Resets the game state to the initial state.
        - _generate_bot_players: Generates a specified number of bot players based on user input.
        - list_of_players: Creates a list of all players in the game.
        - open_hidden_cards: Reveals the dealer's and bot players' hidden cards.
        - initial_deal: Deals two cards to each player at the beginning of the game.
        - print_all_players_cards: Prints the hand cards of all players.
        - making_a_bets: Prompts all players to make their bets.
        - asking_card: Asks each player whether they want to hit or stand and adds cards accordingly.
        - check_winner: Checks for winners and losers based on game conditions.
        - game_round: Executes a round of the game, including player turns and checking for winners.
        - distribute_prizes: Distributes prizes to the winners based on game outcomes.
        - play_again_prompt: Prompts the player to play the game again or exit.
        - start_game: Starts the main loop of the Blackjack game.
        """
    max_players_count = BOT_PLAYERS_LIMITS.get('max')
    min_players_count = BOT_PLAYERS_LIMITS.get('min')

    def __init__(self):
        """
        Initializes a new game by creating a deck, dealer, and player instances.
        """
        self.game_deck = Deck()
        self.game_dealer = Dealer()
        self.bot_players = []
        self.player = Player()
        self.all_players = []

    def clear_and_deal_cards(self):
        """
        Clears player's hand cards and deals two new cards.

        Returns:
        --------
        list: List of two new cards for the player.
        """
        self.player.clear_cards()
        self.player.deal_cards(self.game_deck)
        return self.player.player_cards

    def reset_game(self):
        """
        Resets the game state to the initial state.
        """
        self.game_deck = Deck()
        self.game_dealer = Dealer()
        self.bot_players = []
        self.player.player_cards = self.clear_and_deal_cards()
        self.all_players = []

        time.sleep(2)
        print('*' * 100)
        print('\nGlad to see you again! You are thr lucky one if you still have some money😎')
        time.sleep(3)

    def reset_room(self):
        """
        Resets the game state to the initial state.
        """
        self.game_deck = Deck()
        for player in self.all_players:
            player.clear_cards()
            player.deal_cards(self.game_deck)
            player.reveal_card(status=True)

        time.sleep(2)
        print('*' * 100)
        print('\nSeems you\'re fall in love with the dealer!'
              '\nHow else to explain that you are still here?! OK, another game 😎')
        time.sleep(3)

    def _generate_bot_players(self):
        """
        Generates a specified number of bot players based on user input.

        Returns:
        --------
        list: List of bot players.
        """
        while True:
            try:
                players_count = int(input(
                    f'\n➡️ Enter the number of computer players ({self.min_players_count}-{self.max_players_count}) '
                    f'you wanna play with: '))
                if not (self.min_players_count <= players_count <= self.max_players_count):
                    raise NumberException
            except (ValueError, TypeError, AttributeError):
                print('‼️Can\'t accept incorrect input. Try again!\n')
            except NumberException:
                print('‼️Your number of players is not in the accessible range. Please, try again!\n')
            else:
                break

        for bot_player in range(players_count):
            bot_player = BotPlayer()
            self.bot_players.append(bot_player)

        time.sleep(1)
        print('🔎Looking for your opponents...')
        time.sleep(2)
        print('👥 You will play with {}'.format(', '.join([bot.name for bot in self.bot_players])))
        self.all_players = self.list_of_players()
        time.sleep(2)
        return self.bot_players

    def list_of_players(self):
        """
        Creates a list of all players in the game.

        Returns:
        --------
        list: List of all players in the game.
        """
        self.all_players = [self.player, self.game_dealer]
        for bot_in_list in self.bot_players:
            self.all_players.append(bot_in_list)
        shuffle(self.all_players)  # change players places
        return self.all_players

    def open_hidden_cards(self):
        """
        Reveals the dealer's and bot players' hidden cards.
        """
        self.game_dealer.reveal_card(status=False)
        for bot in self.bot_players:
            bot.reveal_card(status=False)

    def initial_deal(self):
        """
        Deals two cards to each player at the beginning of the game.
        """
        print('\n🃏DEALER HANDS OUT CARDS🃏')
        for player in self.all_players:
            if not player.count_player_points():
                player.deal_cards(self.game_deck)

        time.sleep(2)
        print('😎DONE')
        time.sleep(2)
        print('\nYou can look over your cards...\n')
        time.sleep(2)
        self.print_all_players_cards()
        self.open_hidden_cards()

    def print_all_players_cards(self):
        """
        Prints the hand cards of all players.
        """
        for player in self.all_players:
            cards = player.print_cards()
            if not cards:
                print(f'👀{player.name} looked over the playing cards')
            else:
                print(f'😎{player.name} has cards:\n{cards}')
            if not player.hidden_card:
                print(f'⚪️Points: {player.player_points}\n')
            time.sleep(2)

    def making_a_bets(self):
        """
        Prompts all players to make their bets.
        """
        print('\n💰TIME FOR BETS💰\n')
        for player in self.all_players:
            player.make_a_bet()
            time.sleep(2)

    def asking_card(self):
        """
        Asks each player whether they want to hit or stand and adds cards accordingly.

        Returns:
        --------
        list: List of True/False values indicating whether each player chose to hit.
        """
        answers = []
        for player in self.all_players:
            if player.hit_or_stand():
                player.add_card(self.game_deck.get_card())
                answers.append(True)
            else:
                answers.append(False)
            time.sleep(2)
        return answers

    def check_winner(self):
        """
        Checks for winners and losers based on game conditions.

        Returns:
        --------
        bool: True if the game has winners, False otherwise.
        """
        dealer_points = self.game_dealer.count_player_points()

        losers = [player for player in self.all_players if player.player_points > 21 and not isinstance(player, Dealer)]
        if losers:
            print('\n')
            for loser in losers:
                print(f'☠️{loser.name}, you are busted! Hit the road!')
                self.all_players.remove(loser)
                time.sleep(1)

        if dealer_points > 21:
            print('\n🤑The DEALER is busted! All players in the game are winners!')
            self.all_players.remove(self.game_dealer)
            for player in self.all_players:
                prize = (1.5 * player.player_bet).__round__(0)
                print(f'{player.name}, congrats! Take your prize {prize}$')
                player.player_money += prize
                time.sleep(1)
            return True  # гравці виграли

        winners21 = [player for player in self.all_players if player.player_points == 21]
        if winners21:
            for winner21 in winners21:
                print(f'\n🎉{winner21.name}, you are a winner with 21 points!')

                prize = (2 * winner21.player_bet).__round__(0)
                winner21.player_money += prize  # виграш з бету + сам бет

                print(f'{winner21.name}, your prize is {prize}! Take your money!')

            return True  # є переможець

        if len(self.all_players) == 1 and self.all_players[0].player_points < 21:
            prize = (1.5 * self.all_players[0].player_bet).__round__(0)
            print(f'\n🎉{self.all_players[0].name}, you are the only winner! '
                  f'Your prize is {prize}! Take your money!')
            self.all_players[0].player_money += prize
            return True

        return False  # гра триває

    def game_round(self):
        """
        Executes a round of the game, including player turns and checking for winners.
        """
        while True:
            print('\nSo, what do we have?..')
            time.sleep(2)

            winners_list = self.check_winner()
            if winners_list:
                break
            else:
                print('\n😎Anyone want to take one more card?\n')
                time.sleep(2)
                answers = self.asking_card()

                if not any(answers):  # Якщо всі елементи списку False
                    print('\n🏁Let\'s finish our game\n')
                    time.sleep(2)
                    self.distribute_prizes()
                    break
                else:
                    time.sleep(2)
                    print('\nLet\'s look over our cards!\n')
                    time.sleep(2)
                    self.print_all_players_cards()

    def distribute_prizes(self):
        """
        Distributes prizes to the winners based on game outcomes.
        """
        for player in self.all_players:
            if 21 > player.player_points > self.game_dealer.player_points:
                prize = (1.5 * player.player_bet).__round__(0)
                player.player_money += prize  # виграш з бету + сам бет
                print(f'🏆{player.name}, you beat the DEALER\n'
                      f'{player.name}, your prize is {prize}! Congrats and take your money!')
            elif player.player_points == self.game_dealer.player_points and not isinstance(player, Dealer):
                player.player_money += player.player_bet
                print(
                    f'🤜🤛 OMG! It\'s a hit! {player.name} and {self.game_dealer.name}, you have the same points ({player.player_points})!\n'
                    f'{player.name}, take your bet {player.player_bet}$ only back. Good luck next time!')
                time.sleep(1)

    def play_again_prompt(self):
        """
        Prompts the player to play the game again or exit.

        Returns:
        --------
        bool: True if the player wants to play again, False otherwise.
        """
        while True:
            try:
                play_again_input = input('\n➡️ Do you want to play again? (y/n): ').lower().strip()
                if play_again_input not in ['y', 'n']:
                    raise ValueError
            except ValueError:
                print('‼️Invalid input. Please enter "y" or "n".')
            else:
                if play_again_input == 'y':
                    if self.player.player_money < self.player.min_bet:
                        print("☠️ Sorry, you don't have enough money for the minimum bet. Game over.")
                        return False
                    else:
                        if self.game_dealer not in self.all_players:
                            self.all_players.append(self.game_dealer)
                        return True
                else:
                    return False

    def room_promt(self):
        """
        Prompts the player to play the game again in the same room or exit.

        Returns:
        --------
        bool: True if the player wants to play again, False otherwise.
        """
        if len(self.all_players) > 2 and self.player in self.all_players:
            while True:
                try:
                    room_input = input('\n➡️ Stay in this room? (y/n): ').lower().strip()
                    if room_input not in ['y', 'n']:
                        raise ValueError
                except ValueError:
                    print('‼️Invalid input. Please enter "y" or "n".')
                else:
                    if room_input == 'y':
                        self.reset_room()
                        return True
                    else:
                        return False
        else:
            return False

    def start_game(self):
        """
        Starts the main loop of the Blackjack game.
        """
        print('👋 Hello! Nice to see you here:) Let\'s start our BLACKJACK GAME!\n'
              'Follow the tips in the game and break a leg 😎')
        time.sleep(3)
        self._generate_bot_players()

        while True:
            self.making_a_bets()
            self.initial_deal()
            time.sleep(3)
            print('\nOK, guys, open your cards!\n')
            time.sleep(3)
            self.print_all_players_cards()
            self.game_round()

            print(f"\n💰Your current balance: ${self.player.player_money}")

            if not self.play_again_prompt():
                print('👋 Thank you for playing! Have a great day!')
                break
            else:
                if not self.room_promt():
                    self.reset_game()
                    self._generate_bot_players()
