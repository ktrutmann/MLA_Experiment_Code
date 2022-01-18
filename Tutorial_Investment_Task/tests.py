from otree.api import Submission
from . import *
from otree.api import Bot

import random as rd


class PlayerBot(Bot):

    def play_round(self):
        if self.player.round_number == 1:
            self.player.participant.vars['up_probs'] = [.65]
            # This is necessary, and I have no Idea why:
            print(f'@@@@@ {self.player.participant.vars}')

            yield (prolific_ID_page, {'prolific_id': 'abc123'})

        yield Submission(initializer_page, check_html=False)

        if self.round_number == 1:
            yield Submission(tutorial_page, {'transaction': 1}, check_html=False)

        if self.player.i_round_in_path == 0:
            yield condition_page

        # Trading page:
        if should_display_infos(self.player):
            yield Submission(trading_page, {'transaction': self.get_random_trade(),
                                                  'time_to_order': 2,
                                                  'unfocused_time_to_order': 0,
                                                  'changed_mind': False,
                                                  'erroneous_trade': 'none'},
                             check_html=False)

        # Belief page:
        if should_display_infos(self.player):
            yield Submission(belief_page, {'belief': rd.randint(0, 100),
                                                 'time_to_belief_report': 3,
                                                 'unfocused_time_to_belief_report': 0},
                             check_html=False)

        if should_display_infos(self.player):
            yield update_page, {'update_time_used': 2}

        if self.round_number == Constants.num_rounds:
            yield end_page

    def get_random_trade(self):
        min_transaction = min(Constants.hold_range) - self.player.hold
        max_transaction = max(Constants.hold_range) - self.player.hold
        return rd.randint(min_transaction, max_transaction)
