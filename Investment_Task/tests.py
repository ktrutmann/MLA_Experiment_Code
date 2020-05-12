from . import pages
from ._builtin import Bot
from otree.api import Submission
from .models import Constants
import random as rd


class PlayerBot(Bot):

    def __init__(self):
        print('Using Bot in "{}" mode.'.format(Constants.bot_type))

    def play_round(self):
        yield Submission(pages.initializer_page, check_html=False)

        if self.player.i_round_in_path == 0:
            yield pages.condition_page

        # Trading page:
        if self.player.should_display_infos():
            if Constants.bot_type == 'custom':
                transaction = self.get_wishful_trade()
            else:
                min_transaction = min(Constants.hold_range) - self.player.hold
                max_transaction = max(Constants.hold_range) - self.player.hold
                transaction = rd.randint(min_transaction, max_transaction + 1)

            yield Submission(pages.trading_page, {'transaction': transaction,
                                                  'time_to_order': 2,
                                                  'unfocused_time_to_order': 0,
                                                  'changed_mind': False,
                                                  'erroneous_trade': 'none'},
                             check_html=False)

        # Belief page:
        if self.player.should_display_infos():
            if Constants.bot_type == 'custom':
                belief = self.get_wishful_belief()
            else:
                belief = rd.randint(0, 100)
            yield Submission(pages.belief_page, {'belief': belief,
                                                 'time_to_belief_report': 3,
                                                 'unfocused_time_to_belief_report': 0},
                             check_html=False)

        if self.player.should_display_infos():
            yield pages.update_page, {'update_time_used': 2}

        if self.round_number == Constants.num_rounds:
            yield pages.end_page

    def get_wishful_trade(self):
        return 0  # TODO: Implement! Should return trades that make the desired effect extremely clear!

    def get_wishful_belief(self):
        return 0  # TODO: Implement! Should return beliefs that make the desired effect extremely clear!
