from . import pages
from ._builtin import Bot
from otree.api import Submission
from .models import Constants
import random as rd
import numpy as np


class PlayerBot(Bot):

    rational_belief_up_asset = .5
    cases = ['custom', 'model', 'optimal']  # Can be 'custom', 'model', 'optimal', or 'random'. See `Readme.md`.

    def play_round(self):

        yield Submission(pages.initializer_page, check_html=False)

        if self.round_number == 1:
            print('@@@@@@ Using Bot in "{}" mode.'.format(self.case))
        else:
            self.update_optimal_belief()

        if self.player.i_round_in_path == 0:
            yield pages.condition_page

        # Trading page:
        if self.player.should_display_infos():
            if self.case == 'custom':
                transaction = self.get_wishful_trade()
            elif self.case == 'model':
                transaction = self.get_model_trade()
            elif self.case == 'optimal':
                goal = max(Constants.hold_range) if self.get_optimal_belief() > .5 else min(Constants.hold_range)
                transaction = goal - self.player.hold
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
            if self.case == 'custom':
                belief = self.get_wishful_belief()
            elif self.case == 'model':
                belief = self.get_model_belief()
            elif self.case == 'optimal':
                belief = int(self.get_optimal_belief() * 100)
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

    def update_optimal_belief(self):
        if self.player.i_round_in_path == 0:
            self.rational_belief_up_asset = .5
        else:
            previous_self = self.player.in_round(self.round_number - 1)
            price_up = self.player.price > previous_self.price
            move_prob = max(Constants.up_probs) if price_up else min(Constants.up_probs)  # Note: This assumes symmetry!

            # This will introduce rounding errors but oh well...
            self.rational_belief_up_asset = self.rational_belief_up_asset * move_prob / \
                                                (self.rational_belief_up_asset * max(Constants.up_probs) +
                                                    (1 - self.rational_belief_up_asset) * min(Constants.up_probs))

    def get_optimal_belief(self):
        return (self.rational_belief_up_asset * max(Constants.up_probs) +
                (1 - self.rational_belief_up_asset) * min(Constants.up_probs))

    def get_model_trade(self):
        """
        This implements a simple expected utility power function as well as a soft-max choice rule with a given
        sensitivity parameter. This parameter (theta) can be understood as a "randomness" parameter,
        as an extremely high value will lead to the most valuable option being chosen while an extremely
        low parameter will lead to completely random choices.
        """
        alpha = .88  # Risk aversion parameter
        theta = 1  # Soft-max sensitivity

        up_belief = self.get_model_belief()
        portfolio_value = self.player.cash + self.player.hold * self.player.price
        n_moves = len(Constants.updates)

        utilities = []
        for this_hold in range(min(Constants.hold_range), max(Constants.hold_range) + 1):
            up_utilities = [(portfolio_value + this_hold * i) ** alpha * (up_belief / n_moves)
                            for i in Constants.updates]
            down_utilities = [(portfolio_value - this_hold * i) ** alpha * ((1 - up_belief) / n_moves)
                              for i in Constants.updates]

            # Dividing by 1000 so the soft-max doesn't blow up
            utilities += [sum(up_utilities + down_utilities) / 1000]

        # Soft-max:
        numerator = [np.e ** (theta * i) for i in utilities]
        denominator = sum(numerator)
        probabilities = [i / denominator for i in numerator]

        if Constants.show_debug_msg:
            print('Choice probabilities: {}'.format(probabilities))

        goal_hold = rd.choices(range(min(Constants.hold_range), max(Constants.hold_range) + 1), k=1,
                               weights=probabilities)[0]

        return goal_hold - self.player.hold

    def get_model_belief(self):
        if self.player.i_round_in_path == 0:
            return 50

        previous_self = self.player.in_round(self.round_number - 1)
        price_up = self.player.price > previous_self.price

        if self.player.condition_name == 'full_control':
            # Interaction effect dependent on returns:
            if self.player.returns > 0 and price_up or self.player.returns > 0 and not price_up:
                alpha = Constants.bot_base_alpha - Constants.bot_learning_effect
            else:
                alpha = Constants.bot_base_alpha
        elif self.player.condition_name == 'blocked_full_info':
            # less interaction effect, but still there:
            if self.player.returns > 0 and price_up or self.player.returns > 0 and not price_up:
                alpha = Constants.bot_base_alpha - Constants.bot_learning_effect / 2
            else:
                alpha = Constants.bot_base_alpha
        elif self.player.condition_name == 'blocked_blocked_info':
            # If we're jumping rounds do "rational" RL updating:
            # It's not too elegant, but this "goes back" to the last known belief and updates from there.
            # Sadly oTree doesn't let us change attributes of past rounds, so it's only stored temporarely.

            belief_last_round = previous_self.belief
            i = 1

            while belief_last_round is None:  # Backwards search
                i += 1
                belief_last_round = self.player.in_round(self.round_number - i).belief

            while i > 1:  # Forwards "solve"
                temp_self = self.player.in_round(self.round_number - i)
                temp_price_up = temp_self.price < self.player.in_round(self.round_number - i + 1).price
                belief_last_round = int(belief_last_round + Constants.bot_base_alpha *
                                        (100 * temp_price_up - belief_last_round))
                i -= 1

            # Then just update normally:
            alpha = Constants.bot_base_alpha
            return int(belief_last_round + alpha * (100 * price_up - belief_last_round))
        else:
            # Do whatever in the MLA case:
            alpha = Constants.bot_base_alpha

        return int(previous_self.belief + alpha * (100 * price_up - previous_self.belief))

    def get_wishful_trade(self):
        # Only simulate the effect in the "last decision". Otherwise trade randomly.
        if self.player.i_round_in_path == Constants.n_periods_per_phase * 2:
            if self.player.condition_name == 'full_control':
                # Invest somewhere around 0 shares:
                return rd.randint(-2, 2) - self.player.hold
            elif self.player.condition_name == 'blocked_full_info':
                # Invest more shares or short more, depending on the drift:
                goal = rd.randint(0, max(Constants.hold_range)) if self.player.drift > .5 \
                       else rd.randint(min(Constants.hold_range), 0)
                return goal - self.player.hold
            else:
                # Invest or short around the maximum:
                goal = max(Constants.hold_range) - rd.randint(0, 2) if\
                        self.player.drift > .5 else min(Constants.hold_range) +\
                        rd.randint(0, 2)
                return goal - self.player.hold
        else:
            return self.get_random_trade()

    def get_wishful_belief(self):
        if self.player.i_round_in_path == 0:
            return 50

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

        price_move = 100 if self.player.price > previous_self.price else 0
        return int(previous_self.belief + alpha * (price_move - previous_self.belief) /
                   (self.player.i_round_in_path + 1))


    def get_random_trade(self):
        min_transaction = min(Constants.hold_range) - self.player.hold
        max_transaction = max(Constants.hold_range) - self.player.hold
        return rd.randint(min_transaction, max_transaction)
