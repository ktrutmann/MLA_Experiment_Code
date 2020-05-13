from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, widgets, Currency as c
)
import random as rd
import pandas as pd


author = 'Kevin Trutmann'

doc = """
    This is the main investment task app. See the Readme.md for more information.
"""


class Constants(BaseConstants):
    name_in_url = 'Investment_Task'
    players_per_group = None

    # Experimental Flow
    n_periods_per_phase = 4  # How long should the participants be "blocked"?
    n_distinct_paths = 7  # How many paths should be generated?
    condition_names = ['blocked_full_info',
                       'full_control_with_MLA',  # TODO (After Pilot): Remove this condition...
                       'blocked_blocked_info',
                       'full_control'
                       ]  # List of the conditions
    n_phases = [2, 3, 2, 2]  # How many phases should there be per condition
    extra_inv_phase = [1, 0, 1, 1]  # Whether to add "one last question" after the last phase # TODO now: Implement
    hold_range = [-4, 4]  # What's the minimum and maximum amount of shares that can be held.
    shuffle_conditions = True  # Should the conditions be presented in "blocks" or shuffled?

    num_paths = n_distinct_paths * len(condition_names)
    num_rounds = n_distinct_paths * n_periods_per_phase * sum(n_phases) + (n_distinct_paths * len(condition_names)) +\
        sum(extra_inv_phase) * n_distinct_paths

    # The parameters for the price path
    up_probs = [.2, .8]  # The possible probabilities of a price increase (i.e. "drifts")
    start_price = 1000  # The first price in the price path  # TODO now: Random starting value?
    updates = [5, 10, 15]  # List of possible price movements
    starting_cash = 50000  # How much cash does the participant own at the start

    # Time:
    update_time = 7  # Number of seconds to show the price updates  # TODO now: Give more time for blocked info!
    max_time = 6  # Number of seconds until a reminder to decide appears
    max_time_beliefs = 5  # Same but for the belief page

    experimenter_email = 'k.trutmann@unibas.ch'

    # Bot testing:
    bot_type = 'custom'  # Indicates what browser bots to use (if active). See the readme for details.


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    time_to_order = models.FloatField()
    unfocused_time_to_order = models.FloatField()
    changed_mind = models.BooleanField()
    erroneous_trade = models.StringField()
    time_to_belief_report = models.FloatField()
    unfocused_time_to_belief_report = models.FloatField()
    update_time_used = models.FloatField()

    belief = models.IntegerField(min=0, max=100, widget=widgets.Slider, label='')
    cash = models.IntegerField()
    final_cash = models.CurrencyField()

    hold = models.IntegerField()
    returns = models.IntegerField()
    transaction = models.IntegerField(label='')
    base_price = models.FloatField()
    price = models.IntegerField()
    drift = models.FloatField()
    investable = models.BooleanField()

    condition_name = models.StringField()
    i_round_in_path = models.IntegerField()
    global_path_id = models.IntegerField()
    distinct_path_id = models.IntegerField()

    # TODO now: Make usable for Training blocks!
    def make_price_paths(self):
        """
        This method first creates distinct movement sets and then multiplies and scrambles them
        (paths within the experiment and movements within phases). In the end it applies the movement sets
        to create the actual price paths. It takes no arguments since everything is handled via the Constants.
        """

        # Determine the drift for each path:
        drift_list = rd.choices(Constants.up_probs, k=Constants.n_distinct_paths)
        distinct_path_moves_list = []  # Will be a list of lists

        # How many rounds are there per path?
        # One more phase for the MLA treatment.
        max_moves_per_path = Constants.n_periods_per_phase * max(Constants.n_phases)

        for this_drift in drift_list:
            moves = []

            for _ in range(max_moves_per_path):
                movement_direction = rd.choices([1, -1], weights=[this_drift, 1 - this_drift])[0]
                movement_magnitude = rd.choice(Constants.updates)
                moves += [movement_direction * movement_magnitude]

            distinct_path_moves_list += [moves]

        # Scramble the moves differently for each condition:
        all_moves_list = [[i for i in distinct_path_moves_list] for _, _ in enumerate(Constants.condition_names)]
        all_drifts_list = [[i for i in drift_list] for _, _ in enumerate(Constants.condition_names)]
        # The levels here are [condition][path][period]

        for i_cond, _ in enumerate(Constants.condition_names):
            for i_path in range(Constants.n_distinct_paths):
                # Trim the path if the last phase is not needed in this condition:
                all_moves_list[i_cond][i_path] = \
                    [i for i in all_moves_list[i_cond][i_path][:(Constants.n_periods_per_phase *
                                                                 Constants.n_phases[i_cond] + 1)]]

                # Create a moving window to scramble the movements:
                for i_phase in range(Constants.n_phases[i_cond]):
                    these_moves = all_moves_list[i_cond][i_path][(i_phase * Constants.n_periods_per_phase):
                                                                 ((i_phase + 1) * Constants.n_periods_per_phase)]
                    rd.shuffle(these_moves)
                    all_moves_list[i_cond][i_path][(i_phase * Constants.n_periods_per_phase):
                                                   ((i_phase + 1) * Constants.n_periods_per_phase)] = these_moves

        # Now also shuffle the paths together with their drifts:
        distinct_path_ids = [list(range(Constants.n_distinct_paths))] * len(Constants.condition_names)
        for i_cond, _ in enumerate(Constants.condition_names):
            these_ids = distinct_path_ids[i_cond].copy()
            rd.shuffle(these_ids)
            distinct_path_ids[i_cond] = these_ids
            all_drifts_list[i_cond] = [all_drifts_list[i_cond][path_id] for path_id in distinct_path_ids[i_cond]]
            all_moves_list[i_cond] = [all_moves_list[i_cond][path_id] for path_id in distinct_path_ids[i_cond]]

        # Apply the price movements to create actual prices and save them in the participant vars:
        # Not too elegant with the for loops, but it does the trick... ¯\_(ツ)_/¯
        prices = []
        i_path_global = 0
        i_path_global_list = []
        i_round_in_path = []
        distinct_path_id = []
        drift = []
        i_condition = []
        last_trial_in_path = []

        for i_cond, _ in enumerate(Constants.condition_names):
            for i_path in range(Constants.n_distinct_paths):
                prices += [Constants.start_price]
                i_path_global_list += [i_path_global]
                distinct_path_id += [distinct_path_ids[i_cond][i_path]]
                i_round_in_path += [0]
                drift += [all_drifts_list[i_cond][i_path]]
                i_condition += [i_cond]
                last_trial_in_path += [False]

                for i_move, this_move in enumerate(all_moves_list[i_cond][i_path]):
                    prices += [prices[-1] + this_move]
                    i_path_global_list += [i_path_global]
                    distinct_path_id += [distinct_path_ids[i_cond][i_path]]
                    i_round_in_path += [i_move + 1]
                    drift += [all_drifts_list[i_cond][i_path]]
                    i_condition += [i_cond]
                    last_trial_in_path += [False]
                i_path_global += 1
                last_trial_in_path[-1] = True

        condition_name = [Constants.condition_names[i] for i in i_condition]

        price_df = pd.DataFrame(dict(global_path_id=i_path_global_list,
                                     distinct_path_id=distinct_path_id,
                                     i_round_in_path=i_round_in_path,
                                     last_trial_in_path=last_trial_in_path,
                                     price=prices,
                                     drift=drift,
                                     condition_id=i_condition,
                                     condition_name=condition_name))

        if Constants.shuffle_conditions:
            grouped_df = [group.copy() for _, group in price_df.groupby('global_path_id')]
            rd.shuffle(grouped_df)
            price_df = pd.concat(grouped_df.copy()).reset_index(drop=True)

        self.participant.vars['price_info'] = price_df
        # pd.set_option('display.max_rows', None)
        # print(price_df)

    def initialize_round(self):
        # If this is the very first round
        if self.round_number == 1:
            self.make_price_paths()
            self.global_path_id = 1
        else:
            self.global_path_id = self.in_round(self.round_number - 1).global_path_id

        # Record the relevant price variables into the database:
        for this_var in ['price', 'drift', 'condition_name', 'i_round_in_path', 'distinct_path_id']:
            setattr(self, this_var, self.participant.vars['price_info'][this_var][self.round_number - 1])
        self.investable = self.is_investable()
        print(self.is_investable())

        # If this is the first round of a new path:
        if self.i_round_in_path == 0:
            self.hold = rd.choice(range(Constants.hold_range[0], Constants.hold_range[1] + 1))
            self.cash = Constants.starting_cash - (self.hold * Constants.start_price)
            self.base_price = Constants.start_price if self.hold != 0 else 0
            self.returns = 0
            self.price = Constants.start_price
            if self.round_number > 1:
                self.global_path_id = self.in_round(self.round_number - 1).global_path_id + 1
        else:
            former_self = self.in_round(self.round_number - 1)
            if former_self.transaction is None:  # TODO (After pilot) This is a hot-fix. Could be better.
                former_self.transaction = 0
            self.hold = former_self.hold + former_self.transaction
            self.cash = former_self.cash - former_self.transaction * \
                        self.participant.vars['price_info'].price[self.round_number - 2]

            # Base price:
            if self.hold == 0:
                self.base_price = 0
            elif (self.hold > 0) is not (former_self.hold > 0):  # "Crossed" the 0 hold line
                self.base_price = self.participant.vars['price_info'].price[self.round_number - 2]
            elif former_self.transaction == 0 or abs(former_self.hold) - abs(self.hold) > 0:  # Only sales or nothing
                self.base_price = former_self.base_price
            else:
                self.base_price = (abs(former_self.hold) * former_self.base_price +
                                   abs(former_self.transaction) *
                                   self.participant.vars['price_info'].price[self.round_number - 2]) / \
                                  abs(self.hold)

            self.returns = self.hold * \
                           (self.participant.vars['price_info'].price[self.round_number - 1] - self.base_price)

            # If this is the last round of a block:
            if self.round_number == Constants.num_rounds or \
                    self.participant.vars['price_info'].i_round_in_path[self.round_number] == 0:
                # "Sell everything" for the last price:
                self.final_cash = self.cash.item() + self.hold * \
                                  self.participant.vars['price_info'].price[self.round_number - 1].item()
                self.payoff = (self.final_cash - Constants.starting_cash)

    # For displaying the page
    def is_investable(self):
        """Find out whether the participant should be able to make an investment decision in this round."""
        # FIXME now: Last trial of blocked_info is also marked as investable. Maybe also other conditions?
        is_phase_start = self.i_round_in_path % Constants.n_periods_per_phase == 0
        is_block_start = self.i_round_in_path == 0
        is_first_phase = self.i_round_in_path < Constants.n_periods_per_phase
        is_last_mla_phase = self.condition_name == 'full_control_with_MLA' and self.i_round_in_path >\
            (Constants.n_phases[self.participant.vars['price_info'].condition_id[self.round_number - 1]] - 1) *\
            Constants.n_periods_per_phase
        is_blocked_condition = self.condition_name in ['blocked_full_info', 'blocked_blocked_info'] or\
            is_last_mla_phase

        return (is_phase_start and not is_block_start and not is_last_mla_phase) or\
               (not is_first_phase and not is_blocked_condition)

    def should_display_infos(self):
        """Figures out whether this is a 'blocked info' trial, and should therefore be completely skipped."""
        last_round = self.participant.vars['price_info'].last_trial_in_path[self.round_number - 1]
        start_of_phase = self.i_round_in_path % Constants.n_periods_per_phase == 0
        blocked_condition = self.condition_name == 'blocked_blocked_info'
        first_phase = self.i_round_in_path < Constants.n_periods_per_phase

        return ((not blocked_condition) or first_phase or start_of_phase) and not last_round

    def get_investment_span(self):
        """Given you can invest in this round, how many periods into the future is this investment for?"""
        rounds_in_this_path = Constants.n_periods_per_phase * Constants.n_phases[
            self.participant.vars['price_info'].condition_id[self.round_number - 1]]

        if self.condition_name == 'full_control':
            return 1
        elif self.condition_name in ['blocked_full_info', 'blocked_blocked_info']:
            return Constants.n_periods_per_phase if (self.i_round_in_path + 1) < rounds_in_this_path else 1
        elif self.condition_name == 'full_control_with_MLA':
            return 1 if self.i_round_in_path < rounds_in_this_path - Constants.n_periods_per_phase\
                else Constants.n_periods_per_phase

    def get_trading_vars(self):
        percentage_returns = 0
        if self.base_price != 0:
            percentage_returns = round((self.returns / self.base_price) * 100, 1)

        if self.returns > 0:
            return_color = 'green'
        elif self.returns < 0:
            return_color = 'red'
        else:
            return_color = 'black'

        return {'return_color': return_color,
                'percentage_returns': percentage_returns,
                'all_val': self.price * self.hold,
                'wealth': int(self.price * self.hold + self.cash),
                'condition': self.participant.vars['price_info'].condition_name[self.round_number - 1],
                'investable': self.is_investable(),
                'n_periods_to_invest': self.get_investment_span()
                }

    def make_update_list(self):
        """Creates a zipped list for django to display as the updates. The length depends on the condition."""
        if self.condition_name == 'blocked_blocked_info' and self.i_round_in_path  == Constants.n_periods_per_phase:
            # We are at the last decision of the blocked and low info condition, so show a list of updates:
            price_list = self.participant.vars['price_info'].price
            # This is shown right after the blocked trade has been made. Hence "future".
            future_indexes = range(self.round_number - 1, self.round_number + Constants.n_periods_per_phase - 1)

            was_increase = [price_list[i + 1] > price_list[i] for i in future_indexes]
            differences = [abs(price_list[i + 1] - price_list[i]) for i in future_indexes]
            new_price = [price_list[i + 1] for i in future_indexes]

            return zip(was_increase, differences, new_price)
        else:
            was_increase = self.participant.vars['price_info'].price[self.round_number] > self.price
            difference = abs(self.participant.vars['price_info'].price[self.round_number] - self.price)
            new_price = self.participant.vars['price_info'].price[self.round_number]

            return zip([was_increase], [difference], [new_price])

    # In the very last round, calculate how much was earned
    def calculate_final_payoff(self):
        end_cash_list = [self.in_round(i + 1).final_cash - Constants.starting_cash for
                         i in range(Constants.num_rounds) if
                         self.participant.vars['price_info'].last_trial_in_path[i]]
        print(end_cash_list)
        sum_end_cash = sum(end_cash_list)

        # Add the base_payoff to the game-payoff and make sure that it is floored at 0
        self.participant.payoff = c(self.session.config['base_bonus'] /
                                    self.session.config['real_world_currency_per_point'] + sum_end_cash)

        if self.participant.payoff < 0:
            self.participant.payoff -= self.participant.payoff  # For some reason 0 didn't work.

        self.participant.vars['payoff_dict'] =\
            {'payoff_list': zip(end_cash_list),
             'end_cash_sum': sum_end_cash,
             'payoff_total': self.participant.payoff_plus_participation_fee(),
             'showup_fee': self.session.config['participation_fee'],
             'base_payoff': self.session.config['base_bonus'],
             'percent_conversion': round(self.session.config['real_world_currency_per_point'] * 100, 2)
             }

