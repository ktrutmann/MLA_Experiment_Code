from . import pages
from ._builtin import Bot
from otree.api import Submission
from .models import Constants
import random as rd


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            print('@@@@@@ Using Bot in "{}" mode.'.format(Constants.bot_type))

        yield Submission(pages.initializer_page, check_html=False)

        if self.player.i_round_in_path == 0:
            yield pages.condition_page

        # Trading page:
        if self.player.should_display_infos():
            if Constants.bot_type == 'custom':
                transaction = self.get_wishful_trade()
            else:
                transaction = self.get_random_trade()

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
        # Only simulate the effect in the "last decision". Otherwise trade randomly.
        if self.player.i_round_in_path == Constants.n_periods_per_phase * 2:
            if self.player.condition_name == 'full_control':
                # Invest somewhere around 0 shares:
                return rd.randint(-1, 1) - self.player.hold
            elif self.player.condition_name == 'blocked_full_info':
                # Invest more shares or short more, depending on the drift:
                goal = rd.randint(min(Constants.hold_range), 0) if self.player.drift > .5 \
                       else rd.randint(0, max(Constants.hold_range))
                return goal - self.player.hold
            else:
                # Invest or short around the maximum:
                return max(Constants.hold_range) - rd.randint(0, 2) if self.player.drift > .5 \
                    else min(Constants.hold_range) + rd.randint(0, 2)
        else:
            return self.get_random_trade()

    def get_wishful_belief(self):
        if self.player.i_round_in_path == 0:
            return 50
        else:
            # I don't think this is the "correct" updating mechanism, but it does the job.
            previous_self = self.player.in_round(self.round_number - 1)

            if self.player.condition_name == 'full_control':
                # Be very conservative:
                alpha = .5
            elif self.player.condition_name == 'blocked_full_info':
                # Be less conservative:
                alpha = .75
            elif self.player.condition_name == 'blocked_blocked_info':
                # If we're jumping rounds use last reported belief and price as a reference:
                i = 2
                while previous_self.belief is None:
                    previous_self = self.player.in_round(self.round_number - i)
                    i += 1

                # Be least conservative:
                alpha = .9
            else:
                # Do whatever:
                alpha = 1

            if self.player.price > previous_self.price:
                return int(previous_self.belief + alpha * (100 - previous_self.belief) /
                           (self.player.i_round_in_path + 1))
            else:
                return int(previous_self.belief + alpha * (0 - previous_self.belief) /
                           (self.player.i_round_in_path + 1))

    def get_random_trade(self):
        min_transaction = min(Constants.hold_range) - self.player.hold
        max_transaction = max(Constants.hold_range) - self.player.hold
        return rd.randint(min_transaction, max_transaction)
