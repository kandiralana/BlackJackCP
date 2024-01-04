from deck import Deck
from players import Dealer, BotPlayer, Player
from constants import BOT_PLAYERS_LIMITS, NumberException
import time


class Game:
    max_players_count = BOT_PLAYERS_LIMITS.get('max')
    min_players_count = BOT_PLAYERS_LIMITS.get('min')

    def __init__(self):
        self.game_deck = Deck()
        self.game_dealer = Dealer()
        self.bot_players = []
        self.player = Player()
        self.all_players = []

    def _generate_bot_players(self):
        while True:
            try:
                players_count = int(input(
                    f'Enter the number of computer players ({self.min_players_count}-{self.max_players_count}) '
                    f'you wanna play with: '))
                if not (self.min_players_count <= players_count <= self.max_players_count):
                    raise NumberException
            except (ValueError, TypeError, AttributeError):
                print('Can\'t accept incorrect input. Try again!\n')
            except NumberException:
                print('Your number of players is not in the accessible range. Please, try again!\n')
            else:
                break

        for bot_player in range(players_count):
            bot_player = BotPlayer()
            self.bot_players.append(bot_player)
        print('You will play with {}'.format(', '.join([bot.name for bot in self.bot_players])))
        self.all_players = self.list_of_players()
        time.sleep(2)
        return self.bot_players

    def list_of_players(self):
        self.all_players = [self.player, self.game_dealer]
        for bot_in_list in self.bot_players:
            self.all_players.append(bot_in_list)
        return self.all_players

    def open_hidden_cards(self):
        self.game_dealer.reveal_card()
        for bot in self.bot_players:
            bot.reveal_card()

    def initial_deal(self):
        for player in self.all_players:
            for _ in range(2):
                player.add_card(self.game_deck.get_card())
        self.print_all_players_cards()
        self.open_hidden_cards()

    def print_all_players_cards(self):
        for player in self.all_players:
            cards = player.print_cards()
            if not cards:
                print(f'{player.name} looked over the playing cards')
            else:
                print(f'{player.name} cards:\n{cards}')
            if not player.hidden_card:
                print(f'Points: {player.player_points}\n')
            time.sleep(1)

    def making_a_bets(self):
        for player in self.all_players:
            player.make_a_bet()
            time.sleep(2)

    def asking_card(self):
        for player in self.all_players:
            if player.hit_or_stand():
                player.add_card(self.game_deck.get_card())
            time.sleep(2)

    def check_winner(self):
        dealer_points = self.game_dealer.count_player_points()

        if dealer_points > 21:
            print('All players in the game are winners!')
            return True  # гравці виграли

        winners = [player for player in self.all_players if player.player_points == 21]
        if winners:
            for player in winners:
                print(f'{player.name}, you are a winner with 21 points!')
            return winners  # є переможець

        losers = [player for player in self.all_players if player.player_points > 21]
        if losers:
            for loser in losers:
                print(f'{loser.name}, you are busted! Hit the road!')
                self.all_players.remove(loser)

        if len(self.all_players) == 1 and self.all_players[0].player_points <= 21:
            print(f'{self.all_players[0].name}, you are the only winner!')
            winners.append(self.all_players[0])
            return winners

        return False  # гра триває

    def game_round(self):
        while True:
            winners_list = self.check_winner()
            if winners_list:
                self.distribute_prizes(winners_list)
                break
            else:
                self.asking_card()
            self.print_all_players_cards()

    def win21(self, winners):
        winners21 = []
        for player in winners:
            if player.player_points == 21:
                winners21.append(player)

        for winner21 in winners21:
            prize = (1.5 * winner21.player_bet).__round__(2)
            winner21.player_money += prize  # виграш з бету + сам бет
            print(f'{winner21.name}, your prize is {prize}! Take your money!')

    def distribute_prizes(self, winners):
        if self.win21(winners):
            return True
        else:
            for player in self.all_players:
                if 21 > player.player_points > self.game_dealer.player_points:
                    prize = 2 * player.player_bet
                    player.player_money += prize  # виграш з бету + сам бет
                    print(f'{player.name}, your prize is {prize}! Take your money!')
                elif player.player_points == self.game_dealer.player_points and not isinstance(player, Dealer):
                    print(f'OMG! It\'s a hit! {player.name} and {self.game_dealer.name}, you have the same points!\n'
                          f'Take your bet back.')

    def start_game(self):
        print('Hello! Nice to see you here:) Let\'s start our BLACKJACK GAME!')
        self._generate_bot_players()
        self.making_a_bets()
        self.initial_deal()
        time.sleep(2)
        print('\nLet\'s open our cards!\n')
        time.sleep(1)
        self.print_all_players_cards()
        self.game_round()  # Викликаємо метод game_round()
