from otree.api import Submission
from . import pages
from ._builtin import Bot
from .models import Constants
import random as rd


class PlayerBot(Bot):

    def play_round(self):

        yield Submission(pages.initializer_page, check_html=False)

        if self.round_number == 1:
            yield Submission(pages.tutorial_page, {'transaction': 1}, check_html=False)

        if self.player.i_round_in_path == 0:
            yield pages.condition_page

        # Trading page:
        if self.player.should_display_infos():
            yield Submission(pages.trading_page, {'transaction': self.get_random_trade(),
                                                  'time_to_order': 2,
                                                  'unfocused_time_to_order': 0,
                                                  'changed_mind': False,
                                                  'erroneous_trade': 'none'},
                             check_html=False)

        # Belief page:
        if self.player.should_display_infos():
            yield Submission(pages.belief_page, {'belief': rd.randint(0, 100),
                                                 'time_to_belief_report': 3,
                                                 'unfocused_time_to_belief_report': 0},
                             check_html=False)

        if self.player.should_display_infos():
            yield pages.update_page, {'update_time_used': 2}

        if self.round_number == Constants.num_rounds:
            yield pages.end_page

    def get_random_trade(self):
        min_transaction = min(Constants.hold_range) - self.player.hold
        max_transaction = max(Constants.hold_range) - self.player.hold
        return rd.randint(min_transaction, max_transaction)
