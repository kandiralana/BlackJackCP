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
        return 'Your number of players not in the accessible range. Please, try again!\n'

# BOT_NAMES = ['Alice Johnson', 'Brian Martinez', 'Cynthia Lee', 'David Anderson', 'Emily Rodriguez',
#              'Frank Mitchell', 'Grace Taylor', 'Henry Wright', 'Isabel Davis', 'Jack Turner',
#              'Katherine White', 'Liam Harris', 'Megan Brown', 'Nathan Clark', 'Olivia King',
#              'Patrick Moore', 'Quinn Foster', 'Rachel Reed', 'Samuel Carter', 'Taylor Adams',
#              'Victor Lopez', 'Wendy Walker', 'Xavier Smith', 'Yvonne Hall', 'Zachary Evans',
#              'Adriana Rivera', 'Brandon Cooper', 'Chloe Morgan', 'Derek Baker', 'Ella Bennett',
#              'Felix Ross', 'Gabriella Hayes', 'Harrison Nelson', 'Ivy Perry', 'Justin Kim',
#              'Kylie Turner', 'Lucas Fisher', 'Mia Roberts', 'Nolan Johnson', 'Olivia Cox',
#              'Preston Reed', 'Quinn Taylor', 'Rebecca Hall', 'Seth Turner', 'Tracy Martinez',
#              'Ursula Davis', 'Vincent White', 'Willa Foster', 'Xander Mitchell', 'Yasmine Lee',
#              'Zane Anderson', 'Avery Wright', 'Blake Harris', 'Caroline Carter', 'Daniel Adams',
#              'Emma King', 'Finn Brown', 'Giselle Taylor', 'Hudson Clark', 'Isla Moore',
#              'Jaden Foster', 'Kelly Rodriguez', 'Landon Smith', 'Morgan Bennett', 'Natalie Kim',
#              'Oscar Hayes', 'Piper Nelson', 'Quincy Turner', 'Riley Cooper', 'Sophie Baker',
#              'Tyler Reed', 'Ulysses Walker', 'Vivian Evans', 'Wyatt Hall', 'Ximena Perry',
#              'Yara Mitchell', 'Zackary Cox', 'Amelia Foster', 'Benjamin Davis', 'Charlotte White',
#              'Dylan Harris', 'Eva Roberts', 'Finnley Turner', 'Grace Carter', 'Henry Adams',
#              'Isabella King', 'Jacob Moore', 'Kaitlyn Hall', 'Liam Martinez', 'Mia Taylor',
#              'Noah Brown', 'Olivia Reed', 'Peyton Smith', 'Quinn Nelson', 'Riley Baker',
#              'Samantha Cox', 'Tristan Walker', 'Uma Hayes', 'Violet Anderson', 'William Foster']
