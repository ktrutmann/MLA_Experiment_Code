from otree.api import Submission
from . import *
from otree.api import Bot
import time

class PlayerBot(Bot):

    def play_round(self):
        yield Submission(payoff_page, check_html=False)
        # Wait for an while:
        time.sleep(600)
