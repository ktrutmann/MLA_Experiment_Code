from . import *
from otree.api import Bot
from otree.api import Submission

import random as rd
import numpy as np


class PlayerBot(Bot):

    rational_belief_up_asset = .5
    # Building the cases to be checked:
    case_list = []
    case_id = 1
    for this_prob in np.arange(.6, .85, .05):
        for this_model in ['CSRL', 'RL_single']:
            case_list += [dict(
                response='model',
                model=this_model,
                learning_rates = dict(
                    fav_gain = .119,
                    fav_loss = .123,
                    unfav_gain = .182,
                    unfav_loss = .074,
                    not_inv = .082,
                    single = .108),
                up_probs=[this_prob, 1 - this_prob],
                case_id=case_id)]
            case_id += 1
    cases = case_list

    file = open('case_list.txt','w')
    for items in case_list:
        file.writelines(str(items) + '\n')
    file.close()

    def play_round(self):
        if self.player.round_number == 1:
            self.player.participant.vars['up_probs'] = self.case['up_probs']
            self.player.participant.vars['learning_rates'] = self.case['learning_rates']
            self.player.participant.label = f'CaseID: {self.case["case_id"]}'
            print(f'@@@@@ This round uses: {self.player.participant.vars}')

        yield Submission(initializer_page, check_html=False)

        if self.round_number != 1:
            self.update_optimal_belief()

        if self.player.i_round_in_path == 0:
            yield condition_page

        # Trading page:
        if is_investable(self.player):
            if self.case['response'] == 'custom':
                transaction = self.get_wishful_trade()
            elif self.case['response'] == 'model':
                transaction = self.get_model_trade()
            elif self.case['response'] == 'optimal':
                goal = max(Constants.hold_range) if self.get_optimal_belief() > .5 else min(Constants.hold_range)
                transaction = goal - self.player.hold
            else:
                transaction = self.get_random_trade()

            yield Submission(trading_page, {'transaction': transaction,
                                                  'time_to_order': 2,
                                                  'unfocused_time_to_order': 0,
                                                  'changed_mind': False,
                                                  'erroneous_trade': 'none'},
                             check_html=False)
        elif should_display_infos(self.player):
            yield Submission(trading_page, {'transaction': 0,
                                                  'time_to_order': 2,
                                                  'unfocused_time_to_order': 0,
                                                  'changed_mind': False,
                                                  'erroneous_trade': 'none'},
                             check_html=False)

        # Belief page:
        if should_display_infos(self.player):
            if self.case['response'] == 'custom':
                belief = self.get_wishful_belief()
            elif self.case['response'] == 'model':
                belief = self.get_model_belief()
            elif self.case['response'] == 'optimal':
                belief = int(self.get_optimal_belief() * 100)
            else:
                belief = rd.randint(0, 100)
            yield Submission(belief_page, {'belief': belief,
                                                 'time_to_belief_report': 3,
                                                 'unfocused_time_to_belief_report': 0},
                             check_html=False)

        if should_display_infos(self.player):
            yield update_page, {'update_time_used': 2}

        if self.round_number == Constants.num_rounds:
            yield end_page

    def update_optimal_belief(self):
        if self.player.i_round_in_path == 0:
            self.rational_belief_up_asset = .5
        else:
            previous_self = self.player.in_round(self.round_number - 1)
            price_up = self.player.price > previous_self.price
            move_prob = max(self.player.participant.vars['up_probs']) \
                if price_up else min(self.player.participant.vars['up_probs'])  # Note: This assumes symmetry!

            # This will introduce rounding errors but oh well...
            self.rational_belief_up_asset = self.rational_belief_up_asset * move_prob / \
                (self.rational_belief_up_asset * max(self.player.participant.vars['up_probs']) +
                (1 - self.rational_belief_up_asset) * min(self.player.participant.vars['up_probs']))

    def get_optimal_belief(self):
        return (self.rational_belief_up_asset * max(self.player.participant.vars['up_probs']) +
                (1 - self.rational_belief_up_asset) * min(self.player.participant.vars['up_probs']))

    def get_model_trade(self):
        """
        This implements a simple expected utility power function as well as a soft-max choice rule with a given
        sensitivity parameter. This parameter (theta) can be understood as a "randomness" parameter,
        as an extremely high value will lead to the most valuable option being chosen while an extremely
        low parameter will lead to completely random choices.
        """
        alpha = .88  # Risk aversion parameter
        theta = 5  # Soft-max sensitivity

        up_belief = self.get_model_belief() / 100
        portfolio_value = self.player.cash + self.player.hold * self.player.price
        n_moves = len(Constants.updates)

        utilities = []
        for this_hold in range(min(Constants.hold_range), max(Constants.hold_range) + 1):
            up_utilities = [(portfolio_value + this_hold * i) ** alpha * (up_belief / n_moves)
                            for i in Constants.updates]
            down_utilities = [(portfolio_value - this_hold * i) ** alpha * ((1 - up_belief) / n_moves)
                              for i in Constants.updates]

            utilities += [sum(up_utilities + down_utilities)]

        # Soft-max:
        # Lowering utilities. What matters is the difference:
        utilities = [utilities[i] - min(utilities) for i, _ in enumerate(utilities)]
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
        learning_rates = self.case['learning_rates']
        price_up = self.player.price > previous_self.price

        favorable_move = price_up == (previous_self.hold > 0)
        return_after_trade = previous_self.returns if \
            (previous_self.hold > 0) is (self.player.hold > 0) and self.player.hold != 0 else 0
        gain_pos = return_after_trade > 0
        loss_pos = return_after_trade < 0

        if self.player.condition_name == 'full_control':
            if favorable_move and gain_pos:
                alpha = learning_rates['fav_gain']
            elif favorable_move and loss_pos:
                alpha = learning_rates['fav_loss']
            elif (not favorable_move) and gain_pos:
                alpha = learning_rates['unfav_gain']
            elif (not favorable_move) and loss_pos:
                alpha = learning_rates['unfav_loss']
            else:
                alpha = learning_rates['not_inv']

            if (self.case['model'] == 'RL_single' or self.player.i_round_in_path <= Constants.n_periods_per_phase):
                alpha = learning_rates['single']

        elif self.player.condition_name == 'blocked_full_info':
            if favorable_move and gain_pos:
                alpha = (learning_rates['fav_gain'] + learning_rates['single']) / 2
            elif favorable_move and loss_pos:
                alpha = (learning_rates['fav_loss'] + learning_rates['single']) / 2
            elif (not favorable_move) and gain_pos:
                alpha = (learning_rates['unfav_gain'] + learning_rates['single']) / 2
            elif (not favorable_move) and loss_pos:
                alpha = (learning_rates['unfav_loss'] + learning_rates['single']) / 2
            else:
                alpha = (learning_rates['not_inv'] + learning_rates['single']) / 2
                
            if (self.case['model'] == 'RL_single' or
                    self.player.i_round_in_path <= Constants.n_periods_per_phase):
                alpha = learning_rates['single']

        elif self.player.condition_name == 'blocked_blocked_info':
            # If we're jumping rounds do "rational" RL updating:
            # It's not too elegant, but this "goes back" to the last known belief and updates from there.
            # Sadly oTree doesn't let us change attributes of past rounds, so it's only stored temporarely.

            belief_last_round = previous_self.field_maybe_none('belief')
            i = 1

            while belief_last_round is None:  # Backwards search
                i += 1
                belief_last_round = self.player.in_round(self.round_number - i).field_maybe_none('belief')

            while i > 1:  # Forwards "solve"
                temp_self = self.player.in_round(self.round_number - i)
                temp_price_up = temp_self.price < self.player.in_round(self.round_number - i + 1).price
                belief_last_round = int(belief_last_round + learning_rates['single'] *
                                        (100 * temp_price_up - belief_last_round))
                i -= 1

            # Then just update normally:
            alpha = learning_rates['single']
            return int(belief_last_round + alpha * (100 * price_up - belief_last_round))
        else:
            raise ValueError('Invalid Experimental Condition!')

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
            while previous_self.field_maybe_none('belief') is None:
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
