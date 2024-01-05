"""
constants.py: Contains constant values used in the card game.
This module defines various constants such as bet limits, player limits, suits, ranks, bot names, and an exception class.

Constants:
-----------
- BET_LIMITS (dict): Dictionary containing minimum and maximum bet limits.
- BOT_PLAYERS_LIMITS (dict): Dictionary containing minimum and maximum number of bot players.
- SUITS (dict): Dictionary mapping suit names to corresponding symbols.
- RANKS (dict): Dictionary mapping card ranks to their corresponding values.
- BOT_NAMES (list): List of strings representing names for bot players.
- NumberException (Exception): Custom exception class for handling number input errors.
"""


BET_LIMITS = {'min': 2, 'max': 500}
BOT_PLAYERS_LIMITS = {'min': 1, 'max': 4}

SUITS = {'spades': '♠',
         'diamonds': '♦',
         'hearts': '♥',
         'clubs': '♣'
         }

RANKS = {
    'Ace': 11,
    **{face: 10 for face in ['King', 'Queen', 'Jack']},
    **{str(i): i for i in range(2, 11)}
    }

BOT_NAMES = ['Alice Johnson', 'Brian Martinez', 'Cynthia Lee', 'David Anderson', 'Emily Rodriguez',
             'Frank Mitchell', 'Grace Taylor', 'Henry Wright', 'Isabel Davis', 'Jack Turner',
             'Katherine White', 'Liam Harris', 'Megan Brown', 'Nathan Clark', 'Olivia King',
             'Noah Brown', 'Olivia Reed', 'Peyton Smith', 'Quinn Nelson', 'Riley Baker',
             'Samantha Cox', 'Tristan Walker', 'Uma Hayes', 'Violet Anderson', 'William Foster']


class NumberException(Exception):
    def __str__(self):
        return 'Your input not in the accessible range. Please, try again!\n'

