from otree.api import Submission
from . import pages
from ._builtin import Bot
import time

class PlayerBot(Bot):

    def play_round(self):
        # Wait for an while:
        time.sleep(60)
        yield Submission(pages.payoff_page, check_html=False)
