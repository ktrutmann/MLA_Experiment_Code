from otree.api import Currency as c, currency_range, Submission
from . import pages
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):

    def play_round(self):
        yield Submission(pages.payoff_page, check_html=False)
