from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, widgets
)
import random as rd
import csv
import os


author = 'Kevin Trutmann'

doc = """
An oTree implementation of the Trading Task used in Frydman et al., 2014
"""

class Constants(BaseConstants):
    name_in_url = 'Investment_Task'
    players_per_group = None
    # Needs to include a 'main_condition':
    condition_sequence = ['baseline', 'baseline', 'main_condition', 'main_condition']
    lottery_prob = 1  # What proportions of the periods has a lottery attached?
    lottery_bonus = 10  # How many points can be won in the belief elicitation task?
    lottery_discount = .1  # How many "investment points are the lottery points worth?
    n_periods_per_block = 75  # How many periods should each block contain?
    num_rounds = (n_periods_per_block + 1) * len(condition_sequence)

    update_time = 3  # Number of seconds to show the price updates
    max_time = 6  # Number of seconds until a reminder to decide appears
    max_time_beliefs = 5  # Same but for the belief page

    # The parameters for the price path
    import_path = ''  # Leave as '' if the path should be generated
    up_prob = .65  # The probability of a price raise given the good state
    switch_prob = .2  # The probability of flipping the states
    start_price = 1000  # The first price in the price path
    updates = [5, 10, 15]  # List of possible price movements

    # The starting portfolio
    starting_cash = 2500


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
    bayes_prob_good = models.FloatField()
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
    main_condition = models.StringField()
    i_round_in_block = models.IntegerField()
    i_block = models.IntegerField()

    # Validated in R
    def make_price_paths(self, save_path=True, conditions=tuple('training')):
        if not Constants.import_path == '':
            self.read_price_path()
        else:
            self.participant.vars['price_path'] = []
            self.participant.vars['price_raise'] = []
            self.participant.vars['good_state'] = []

            for i_condition, this_condition in enumerate(conditions):
                while True:
                    all_is_fine = True
                    switches = [rd.random() < Constants.switch_prob
                                for _ in range(Constants.n_periods_per_block)]

                    price = [Constants.start_price]
                    good_state = [rd.random() < .5]
                    price_raise = []
                    for this_switch in switches:
                        this_update = rd.sample(Constants.updates, 1)[0]

                        # Determine whether to raise the price
                        if good_state[-1]:
                            increase = rd.random() < Constants.up_prob
                        else:
                            increase = rd.random() < (1 - Constants.up_prob)

                        # If yes, raise the price
                        if increase:
                            price_raise.append(True)
                            price.append(price[-1] + this_update)
                        else:
                            price_raise.append(False)
                            price.append(price[-1] - this_update)

                        # Determine whether to switch states
                        if this_switch:
                            good_state.append(not good_state[-1])
                        else:
                            good_state.append(good_state[-1])

                        # Check whether we're still above 0:
                        if price[-1] < 0:
                            all_is_fine = False
                            break

                    if all_is_fine:
                        break

                self.participant.vars['price_path'] += price
                self.participant.vars['price_raise'] += price_raise + [True]  # Filler
                self.participant.vars['good_state'] += good_state

                if save_path:
                    self.save_price_path(i_condition, this_condition, price, good_state)

    def read_price_path(self):
        with open(Constants.import_path, 'r') as file:
            reader = csv.reader(file)
            this_data = []
            for this_row in reader:
                this_data.append(this_row)

        # Check for errors
        if this_data[0] != ['price', 'good_state']:
            raise ValueError('Please provide a csv with exactly the columns'
                             '"price" and "good_state".')
        elif len(this_data) - 1 != Constants.num_rounds:
            raise IndexError('The price path has not the same length ({})'
                             'as determined in Constants ({}).'.format(len(this_data) - 1,
                                                                       Constants.num_rounds))
        else:
            this_data.pop(0)
            price = [int(i[0]) for i in this_data]
            price_raise = [price[i] < price[i + 1] for i in range(len(price) - 1)] + [False]
            self.participant.vars['price_path'] = price
            self.participant.vars['good_state'] = [i[1] for i in this_data]
            self.participant.vars['price_raise'] = price_raise

            print('Successfully imported price path')

            # Re-Save the price paths in the right format
            for i_condition, this_condition in enumerate(self.participant.vars['condition_sequence']):
                this_price = price[(i_condition * (Constants.n_periods_per_block + 1)):
                                   ((i_condition + 1) * (Constants.n_periods_per_block + 1))]
                good_state = self.participant.vars['good_state'][
                             (i_condition * (Constants.n_periods_per_block + 1)):
                             ((i_condition + 1) * (Constants.n_periods_per_block + 1))]

                self.save_price_path(i_condition, this_condition, this_price, good_state)

    def save_price_path(self, i_condition, this_condition, price, good_state):
        filename = os.path.join('Investment_Task', 'price_paths',
                                'price_path_participant-{}_session-{}_Condition-{}-{}.csv'.format(
                                 self.participant.code, self.session.code, i_condition, this_condition))
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['price', 'good_state'])
            for i in range(Constants.n_periods_per_block + 1):
                writer.writerow([price[i], good_state[i]])


    def calculate_bayesian_prob(self):
        self.participant.vars['bayes_prob_good'] = []  # P(good_state|data)
        self.participant.vars['bayes_prob_up'] = []   # P(price_increase|data)
        for i in range(Constants.num_rounds):
            # Set it to .5 if we're starting a new block
            if i % (Constants.n_periods_per_block + 1) == 0:
                self.participant.vars['bayes_prob_good'].append(.5)
                self.participant.vars['bayes_prob_up'].append(.5)
            else:
                prior = self.participant.vars['bayes_prob_good'][-1]
                if self.participant.vars['price_raise'][i - 1]:
                    likelihood = Constants.up_prob
                    bayes_denominator = Constants.up_prob * prior + (1 - Constants.up_prob) * (1 - prior)
                else:
                    likelihood = 1 - Constants.up_prob
                    bayes_denominator = prior * (1 - Constants.up_prob) + (1 - prior) * Constants.up_prob

                prob_good = (prior * likelihood) / bayes_denominator

                # Add the probability of a switch
                prob_good = prob_good * (1 - Constants.switch_prob) + (1 - prob_good) * Constants.switch_prob
                prob_up = prob_good * Constants.up_prob + (1 - prob_good) * (1 - Constants.up_prob)

                self.participant.vars['bayes_prob_good'].append(prob_good)
                self.participant.vars['bayes_prob_up'].append(prob_up)

    def advance_round(self):
        self.participant.vars['i_in_block'] += 1

        if self.participant.vars['skipper']:
            self.participant.vars['skipper'] = False
            self.participant.vars['i_in_block'] = 0
            self.participant.vars['i_block'] += 1
            self.participant.vars['condition'] = self.participant.vars[
                'condition_sequence'][self.participant.vars['i_block']]

        elif self.participant.vars['i_in_block'] == Constants.n_periods_per_block:
            self.participant.vars['skipper'] = True

    def initialize_portfolio(self):
        self.hold = rd.sample([-1, 0, 1], 1)[0]
        self.cash = Constants.starting_cash - (self.hold * Constants.start_price)
        self.base_price = abs(self.hold * Constants.start_price)
        self.returns = 0
        self.bayes_prob_up = .5
        self.bayes_prob_good = .5
        self.belief_bonus_cumulative = 0
        self.price = Constants.start_price

    def calculate_belief_bonus(self):
        actual_lottery_prob = rd.random()

        if self.belief < actual_lottery_prob:  # Play the lottery:
            self.belief_bonus = Constants.lottery_bonus * int(actual_lottery_prob < rd.random())
        else:  # Bet on the price increasing:
            self.belief_bonus = Constants.lottery_bonus *\
                                int(self.participant.vars['price_path'][self.round_number - 1] <
                                    self.participant.vars['price_path'][self.round_number])

        self.belief_bonus *= Constants.lottery_discount  # Discount the lottery/bet earnings

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
