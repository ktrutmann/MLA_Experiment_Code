from otree.api import Submission
from . import *
from otree.api import Bot
import time

class PlayerBot(Bot):

    def play_round(self):
        # Wait for an while:
        time.sleep(60)
        yield Submission(payoff_page, check_html=False)
