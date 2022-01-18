from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot


class PlayerBot(Bot):

    def play_round(self):
        yield (demographics_page, {'age': 22, 'gender': 'Female', 'is_student': 'No',
                                         'investment_experience': 3, 'purpose': 'aaa',
                                         'attention_check': 3, 'attentiveness': 2, 'engagement': 2})
        yield (comments_page, {'general_comments': 'Nope!'})
