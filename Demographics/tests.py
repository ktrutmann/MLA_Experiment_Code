from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot


class PlayerBot(Bot):

    def play_round(self):
        yield (demographics_page, {
            'age': 22,
            'gender': 'Female',
            'ethnicity': 'White / Caucasian',
            'education': 1,
            'math_abilities_self_report': 1,
            'attention_check': 1,
            'attentiveness': 1,
            'engagement': 1,
            'household_size': 1,
            'household_children': 1,
            'income_bracket': 1,
            'games_of_chance': False,
            'traded_stocks': True,
            'investment_experience': 1,
            'investment_experience': 3,
            'purpose': 'No idea mate',
            'attention_check': 3,
            'attentiveness': 2,
            'engagement': 2})
        yield (comments_page, {
            'pattern': 'None',
            'noticed_repetitions': False,
            'dont_use_data': False,
            'dont_use_data_reason': 'None',
            'general_comments': 'None'})