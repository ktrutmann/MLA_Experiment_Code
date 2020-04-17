from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from otree.api import Submission
from .models import Constants
import random as rd


class PlayerBot(Bot):
    def play_round(self):
        yield Submission(pages.initializer_page, check_html=False)

        if self.player.participant.vars['i_in_block'] == 0:
            yield (pages.condition_page)

        if not self.player.participant.vars['skipper']:
            yield Submission(pages.trading_page, {'transaction': 0,
                                                  'time_to_order': 2,
                                                  'unfocused_time_to_order': 0},
                             check_html=False)

        if self.player.participant.vars['belief_elicitation'] and not self.player.participant.vars['skipper']:
            yield Submission(pages.belief_page, {'belief': rd.randint(0, 100),
                                                 'time_to_belief_report': 3,
                                                 'unfocused_time_to_belief_report': 0},
                             check_html=False)

        if not self.player.participant.vars['skipper']:
            yield (pages.update_page, {'update_time_used': 2})

        if self.round_number == Constants.num_rounds:
            yield (pages.end_page)
