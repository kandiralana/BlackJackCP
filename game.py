from deck import Deck
from players import Dealer, BotPlayer, Player
from constants import BOT_PLAYERS_LIMITS, NumberException
import time
from random import shuffle


class Game:
    max_players_count = BOT_PLAYERS_LIMITS.get('max')
    min_players_count = BOT_PLAYERS_LIMITS.get('min')

    def __init__(self):
        self.game_deck = Deck()
        self.game_dealer = Dealer()
        self.bot_players = []
        self.player = Player()
        self.all_players = []

    def clear_cards(self):
        self.player.player_cards.clear()
        for _ in range(2):
            self.player.add_card(self.game_deck.get_card())
        return self.player.player_cards

    def reset_game(self):
        self.game_deck = Deck()
        self.game_dealer = Dealer()
        self.bot_players = []
        self.player.player_cards = self.clear_cards()
        self.all_players = []

    def _generate_bot_players(self):
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
        self.all_players = [self.player, self.game_dealer]
        for bot_in_list in self.bot_players:
            self.all_players.append(bot_in_list)
        shuffle(self.all_players)  # change players places
        return self.all_players

    def open_hidden_cards(self):
        self.game_dealer.reveal_card()
        for bot in self.bot_players:
            bot.reveal_card()

    def initial_deal(self):
        print('\n🃏DEALER HANDS OUT CARDS🃏')
        for player in self.all_players:
            if not player.count_player_points():
                for _ in range(2):
                    player.add_card(self.game_deck.get_card())
        time.sleep(2)
        print('😎DONE')
        time.sleep(2)
        print('\nYou can look over your cards...\n')
        time.sleep(2)
        self.print_all_players_cards()
        self.open_hidden_cards()

    def print_all_players_cards(self):
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
        print('\n💰TIME FOR BETS💰\n')
        for player in self.all_players:
            player.make_a_bet()
            time.sleep(2)

    def asking_card(self):
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
        dealer_points = self.game_dealer.count_player_points()

        losers = [player for player in self.all_players if player.player_points > 21 and not isinstance(player, Dealer)]
        if losers:
            print('\n')
            for loser in losers:
                print(f'☠️{loser.name}, you are busted! Hit the road!')
                self.all_players.remove(loser)

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
                        return True
                else:
                    return False

    def start_game(self):
        print('👋 Hello! Nice to see you here:) Let\'s start our BLACKJACK GAME!\n'
              'Follow the tips in the game and break a leg 😎')
        time.sleep(3)

        while True:
            self._generate_bot_players()
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
                self.reset_game()  # Якщо гравець хоче грати ще раз, скидаємо гру до початкового стану
