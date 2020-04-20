from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, widgets
)
import random as rd


author = 'Kevin Trutmann'

doc = """

"""


class Constants(BaseConstants):
    name_in_url = 'Investment_Task'
    players_per_group = None

    # Experimental Flow
    n_phases = 2  # How many phases should there be?
    n_periods_per_phase = 5  # How long should the participants be "blocked"?
    n_distinct_paths = 5  # How many paths should be generated?
    condition_names = ['full_control', 'full_control_with_MLA',
                       'blocked_full_info', 'blocked_blocked_info']  # List of the conditions
    hold_range = [-10, 10]  # What's the minimum and maximum amount of shares that can be held.

    num_rounds = n_distinct_paths * n_periods_per_phase * n_phases

    # The parameters for the price path
    up_probs = [.4, .6]  # The possible probabilities of a price increase (i.e. "drifts")
    start_price = 1000  # The first price in the price path
    updates = [5, 10, 15]  # List of possible price movements
    starting_cash = 2500  # How much cash does the participant own at the start

    # Belief elicitation
    max_belief_bonus = 10  # How many points can be won in the belief elicitation task?
    belief_bonus_discount = .1  # How many "investment points are the lottery points worth?

    # Time:
    update_time = 3  # Number of seconds to show the price updates
    max_time = 6  # Number of seconds until a reminder to decide appears
    max_time_beliefs = 5  # Same but for the belief page


class mainSubsession(BaseSubsession):
    class Meta:
        abstract = True

# This is so that the turorial can use it as well
class Subsession(mainSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    time_to_order = models.FloatField()
    unfocused_time_to_order = models.FloatField()
    time_to_belief_report = models.FloatField()
    unfocused_time_to_belief_report = models.FloatField()
    update_time_used = models.FloatField()

    bayes_prob_up = models.FloatField()
    state = models.BooleanField()
    belief = models.IntegerField(min=0, max=100, widget=widgets.Slider, label='')
    belief_bonus = models.CurrencyField()
    belief_bonus_cumulative = models.CurrencyField()
    cash = models.CurrencyField()
    final_cash = models.CurrencyField()

    hold = models.IntegerField()
    returns = models.IntegerField()
    transaction = models.IntegerField()
    base_price = models.IntegerField()
    price = models.IntegerField()

    condition = models.StringField()
    i_round_in_block = models.IntegerField()
    i_block = models.IntegerField()

    # TODO: Validate in R!
    # TODO: Do we need extra rounds for training / burner? Maybe by using an argument "training"?
    def make_price_paths(self):
        """
        This function first creates distinct movement sets and then multiplies and scrambles them
        (paths within the experiment and movements within phases). In the end it applies the movement sets
        to create the actual price paths. It takes no arguments since everything is handled via the Constants.
        """

        # Determine the drift for each path:
        drift_list = rd.choices(Constants.up_probs, k=Constants.n_distinct_paths)
        distinct_path_moves_list = []  # Will be a list of lists

        # How many rounds are there per path?
        # One more phase for the MLA treatment.
        n_moves_per_path = Constants.n_periods_per_phase * (Constants.n_phases + 1)

        for this_drift in drift_list:
            moves = []

            for _ in range(n_moves_per_path):
                movement_direction = rd.choices([1, -1], weights=[this_drift, 1 - this_drift])[0]
                movement_magnitude = rd.choice(Constants.updates)
                moves += [movement_direction * movement_magnitude]

            distinct_path_moves_list += [moves]

        # Scramble the moves differently for each condition:
        all_moves_list = [distinct_path_moves_list] * len(Constants.condition_names)
        all_drifts_list = [drift_list] * len(Constants.condition_names)
        # The levels here are [condition][path][period]

        for i_cond, _ in enumerate(Constants.condition_names):
            for i_path in range(Constants.n_distinct_paths):
                # Create a moving window to scramble the movements:
                for i_phase in range(Constants.n_phases):
                    these_moves = all_moves_list[i_cond][i_path][(i_phase * Constants.n_periods_per_phase):
                                                                 ((i_phase + 1) * Constants.n_periods_per_phase)]
                    rd.shuffle(these_moves)
                    all_moves_list[i_cond][i_path][(i_phase * Constants.n_periods_per_phase):
                                                   ((i_phase + 1) * Constants.n_periods_per_phase)] = these_moves

        # Now also shuffle the paths together with their drifts:
        # TODO: Make sure the structure of the lists is always correct (lists within lists instead of just appending).
        distinct_path_ids = [list(range(Constants.n_distinct_paths))] * len(Constants.condition_names)
        for i_cond, _ in enumerate(Constants.condition_names):
            rd.shuffle(distinct_path_ids[i_cond])
            all_drifts_list[i_cond] = [all_drifts_list[i_cond][path_id] for path_id in distinct_path_ids[i_cond]]
            all_moves_list[i_cond] = [all_moves_list[i_cond][path_id] for path_id in distinct_path_ids[i_cond]]

        # Apply the price movements to create actual prices and concatenate all price paths:
        prices = []
        i_path_global = 0
        i_path_global_list = []
        distinct_path_id = []
        drift = []

        for i_cond, _ in enumerate(Constants.condition_names):
            for i_path in range(Constants.n_distinct_paths):
                prices = [Constants.start_price]
                i_path_global_list += [i_path_global]
                distinct_path_id += distinct_path_ids[i_cond][i_path]
                drift += all_drifts_list[i_cond][i_path]

                for this_move in all_moves_list[i_cond][i_path]:
                    prices += [prices[-1] + this_move]
                    i_path_global_list += [i_path_global]
                    distinct_path_id += distinct_path_ids[i_cond][i_path]
                    drift += all_drifts_list[i_cond][i_path]
                i_path_global += 1

        self.participant.vars['i_path'] = i_path_global_list
        self.participant.vars['distinct_path_id'] = distinct_path_id
        self.participant.vars['price'] = prices
        self.participant.vars['drift'] = drift

    def initialize_portfolio(self):
        self.hold = rd.choice(range(Constants.hold_range[0], Constants.hold_range[1] + 1))
        self.cash = Constants.starting_cash - (self.hold * Constants.start_price)
        self.base_price = Constants.start_price if self.hold != 0 else 0
        self.returns = 0
        self.belief_bonus_cumulative = 0
        self.price = Constants.start_price

    # TODO: Continue adapting from here
    def advance_round(self):
        # TODO: make sure to record the distinct_path_id and the drift in each round!
        self.participant.vars['i_in_block'] += 1

        if self.participant.vars['skipper']:
            self.participant.vars['skipper'] = False
            self.participant.vars['i_in_block'] = 0
            self.participant.vars['i_block'] += 1
            self.participant.vars['condition'] = self.participant.vars[
                'condition_sequence'][self.participant.vars['i_block']]

        elif self.participant.vars['i_in_block'] == Constants.n_periods_per_block:
            self.participant.vars['skipper'] = True

    def calculate_belief_bonus(self):
        actual_lottery_prob = rd.random()

        if self.belief < actual_lottery_prob:  # Play the lottery:
            self.belief_bonus = Constants.max_belief_bonus * int(actual_lottery_prob < rd.random())
        else:  # Bet on the price increasing:
            self.belief_bonus = Constants.max_belief_bonus * \
                                int(self.participant.vars['price_path'][self.round_number - 1] <
                                    self.participant.vars['price_path'][self.round_number])

        self.belief_bonus *= Constants.belief_bonus_discount  # Discount the lottery/bet earnings

    def update_vars(self):
        future_me = self.in_round(self.round_number + 1)
        i_round = self.round_number

        self.condition = self.participant.vars['condition']
        self.main_condition = self.participant.vars['main_condition']
        self.i_round_in_block = self.participant.vars['i_in_block']
        self.i_block = self.participant.vars['i_block']

        # Get the bayesian beliefs and state
        self.bayes_prob_good = self.participant.vars['bayes_prob_good'][self.round_number - 1]
        self.bayes_prob_up = self.participant.vars['bayes_prob_up'][self.round_number - 1]
        self.state = self.participant.vars['good_state'][self.round_number - 1]

        # Get the next price
        if self.round_number < Constants.num_rounds:
            future_me.price = self.participant.vars['price_path'][self.round_number]

        # Figure out that we're not in the last round of a condition
        if self.participant.vars['i_in_block'] < Constants.n_periods_per_block - 1:
            # Base Price
            if self.transaction != 0 and self.hold + self.transaction != 0:
                future_me.base_price = self.participant.vars['price_path'][i_round - 1]
            elif self.transaction == 0:
                future_me.base_price = self.base_price
            else:
                future_me.base_price = 0

            # Cash and belief bonus before last period
            future_me.cash = self.cash -\
                (self.transaction * self.participant.vars['price_path'][i_round - 1])

            if self.participant.vars['i_in_block'] > 0:
                if self.participant.vars['belief_elicitation']:
                    self.belief_bonus_cumulative = self.in_round(self.round_number - 1).belief_bonus_cumulative + \
                                                   self.belief_bonus
                else:
                    self.belief_bonus_cumulative = 0
            else:
                self.belief_bonus_cumulative = self.belief_bonus

            # Holdings
            future_me.hold = self.hold + self.transaction

            # Returns
            future_me.returns = int(future_me.hold *
                                    (self.participant.vars['price_path'][i_round] - future_me.base_price))

        else:  # In the last period of a condition, just update the final cash and belief bonus
            # First, update the belief_bonus:
            if self.participant.vars['belief_elicitation']:
                self.belief_bonus_cumulative = self.in_round(self.round_number - 1).belief_bonus_cumulative + \
                                               self.belief_bonus
            else:
                self.belief_bonus_cumulative = 0

            # Update the cash according to the last trade-decision:
            self.final_cash = self.cash -\
                self.transaction * self.participant.vars['price_path'][i_round - 1]
            # Then update the cash according to the forced-sale at the end:
            self.final_cash += (self.hold + self.transaction) *\
                self.participant.vars['price_path'][i_round]
            # Then add this to the payoff together with the belief bonus
            self.payoff = (self.final_cash - Constants.starting_cash) +\
                self.belief_bonus_cumulative

    # For displaying the page
    def get_trading_vars(self):
        price = self.participant.vars['price_path'][self.round_number - 1]

        percentage_returns = 0
        if self.base_price != 0:
            percentage_returns = round((self.returns / self.base_price) * 100, 1)

        up_prob_state = int(Constants.up_prob * 100)
        if not self.participant.vars['good_state'][self.round_number - 1]:
            up_prob_state = int((1 - Constants.up_prob) * 100)

        return {'price': price,
                'cash': int(self.cash),
                'hold': self.hold,
                'base_price': self.base_price,
                'percentage_returns': percentage_returns,
                'all_val': price * self.hold,
                'wealth': int(price * self.hold + self.cash),
                'max_time': Constants.max_time,
                'condition': self.participant.vars['condition'],
                'main_condition': self.participant.vars['main_condition'],
                'bayes_prob': round(self.participant.vars['bayes_prob_up'][self.round_number - 1] * 100, 2),
                'up_prob_state': up_prob_state
                }

    # After the last round, calculate how much was earned
    def calculate_final_payoff(self):
        blockend_rounds = list(range(Constants.n_periods_per_block, Constants.num_rounds + 1,
                                     Constants.n_periods_per_block + 1))
        end_cash_list = [self.player.in_round(i).final_cash - Constants.starting_cash for i in blockend_rounds]
        sum_end_cash = sum(end_cash_list)

        end_belief_bonus_list = [self.player.in_round(i).belief_bonus_cumulative for i in blockend_rounds]
        sum_end_belief_bonus = sum(end_belief_bonus_list)

        # Add the base_payoff to the game-payoff and make sure that it is floored at 0
        self.player.payoff = self.session.config['base_bonus'] *\
            (1 / self.session.config['real_world_currency_per_point'])

        if self.participant.payoff < 0:
            self.participant.payoff -= self.participant.payoff  # For some reason 0 didn't work.

        self.player.participant.vars['payoff_dict'] = {'payoff_list': zip(end_cash_list, end_belief_bonus_list),
                                               'end_cash_sum': sum_end_cash,
                                               'belief_bonus_sum': sum_end_belief_bonus,
                                               'payoff_game': sum_end_cash + sum_end_belief_bonus,
                                               'payoff_total': self.participant.payoff_plus_participation_fee(),
                                               'showup_fee': self.session.config['participation_fee'],
                                               'base_payoff': self.session.config['base_bonus'],
                                               'percent_conversion':
                                                       self.session.config['real_world_currency_per_point'] * 100
                                                       }