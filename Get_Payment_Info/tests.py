from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):

    def play_round(self):
        yield pages.payment_info_page, {'participant_name': 'Mr. Derp', 'booth_nr': 13}
