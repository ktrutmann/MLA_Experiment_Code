from otree.api import (
    models, BaseGroup, BasePlayer, widgets
)
import random as rd
import csv
import os

from Investment_Task.models import Constants as mainConstants, mainSubsession


author = 'Kevin Trutmann'

doc = """
Tutorial for the Trading Task
"""


class Constants(mainConstants):
    name_in_url = 'Tutorial_Investment_Task'
    num_rounds = 30  # Number of training rounds
    belief_trials = [True] * num_rounds

    # Parameters specifically for the tutorial text
    num_blocks = len(mainConstants.condition_sequence)
    n_conditions = len(set(mainConstants.condition_sequence))

    # IMPORTANT: THE PICTURE IN THE TUTORIAL IS NOT DYNAMIC!
    # IF YOU CHANGE PARAMETERS, CHANGE THE PICTURE AS WELL!

    start_hold = True


class Subsession(mainSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    participant_name = models.StringField(label='Vor und Nachname')
    booth_nr = models.IntegerField(label='Sitzplatznummer')
    transaction = models.IntegerField(label='', blank=True)

    Q1 = models.StringField(widget=widgets.RadioSelect, blank=True,
                            label='Wenn die Firma in einem guten Zustand ist, '
                                  'dann ist die Wahrscheinlichkeit, dass der Preis der Aktie um 5 steigt...',
                            choices=['...kleiner als die Wahrscheinlichkeit, dass er um 10 sinkt.',
                                     '...gleich gross wie die Wahrscheinlichkeit, dass er um 5 sinkt.',
                                     '...gleich gross wie die Wahrscheinlichkeit, dass er um 15 steigt.'])
    Q2 = models.StringField(widget=widgets.RadioSelect, blank=True,
                            label='Dass der Preis um 10 sinkt ist...',
                            choices=['...wahrscheinlicher im schlechten als im guten Zustand.',
                                     '...immer gleich wahrscheinlich wie dass er um 10 steigt.',
                                     '...wahrscheinlicher im guten als im schlechten Zustand'])
    Q3 = models.StringField(widget=widgets.RadioSelect, blank=True,
                            label='Wenn die Firma in der letzten Runde im guten Zustand war...',
                            choices=['...ist es wahrscheinlicher, dass sie in den schlechten Zustand ändert.',
                                     '...ist es wahrscheinlicher, dass sie im guten Zustand bleibt.',
                                     '...ist es gleich wahrscheinlich, dass sie im guten Zustand bleibt wie '
                                     'dass sie in den schlechten Zustand ändert.'])
    Q4 = models.StringField(widget=widgets.RadioSelect, blank=True,
                            label='Stellen Sie sich vor, dass Sie mit dem Slider angegeben haben, dass die Lotterie '
                                  'in dieser Runde mindestens eine Gewinnwahrscheinlichkeit von 50% haben muss. '
                                  'Die im Hintergrund gezogene Gewinnwahrscheinlichkeit der Lotterie in dieser Runde '
                                  'ist 40%. Was wird in diesem Fall passieren?',
                            choices=['Ich gehe automatisch die Wette ein und erhalte die Bonuspunkte falls '
                                     'der Preis nun ansteigt.',
                                     'Ich spiele automatisch die Lotterie und gewinne mit 40% Wahrscheinlichkeit '
                                     'die Bonuspunkte.',
                                     'Ich spiele automatisch die Lotterie und gewinne mit 50% Wahrscheinlichkeit '
                                     'die Bonuspunkte.'])
    Q5 = models.StringField(widget=widgets.RadioSelect, blank=True,
                            label='Sie geben an, dass die Lotterie eine hohe Gewinnwahrscheinlichkeit haben muss, '
                                  'damit Sie sich gegen die Wette auf den Preisanstieg entscheiden. '
                                  'Wann ist dies sinnvoll?',
                            choices=['Wenn ich mir sehr unsicher über den zukünftigen Verlauf des Aktienpreises bin.',
                                     'Wenn ich mir relativ sicher bin, dass der Preis der Aktie fallen wird.',
                                     'Wenn ich mir relativ sicher bin, dass der Preis der Aktie steigen wird.'])
    Q6 = models.StringField(widget=widgets.RadioSelect, blank=True,
                            label='Nehmen Sie an, die folgende Tabelle würde Ihr Portfolio in der letzten Runde '
                                  'repräsentieren.\nSie haben sich entschieden, die Aktie weiterhin zu halten. '
                                  'Das Preis-Update zeigt an, dass der Preis der Aktie um 10 Punkte steigt. '
                                  'Wie viele Punkte werden Ihnen für die Bonusauszahlung gutgeschrieben?',
                            choices=['5800',
                                     '2010',
                                     '5810'])
    wrong_answers = models.IntegerField()

    cash = models.IntegerField()
    hold = models.IntegerField()
    base_price = models.FloatField()
    returns = models.IntegerField()
    belief = models.IntegerField(min=0, max=100, widget=widgets.Slider, label='')


    # Initializing functions:
    # Validated in R
    def make_price_paths(self, conditions=tuple('training')):
        self.participant.vars['price_path'] = []
        self.participant.vars['price_raise'] = []
        self.participant.vars['good_state'] = []

        for _, _ in enumerate(conditions):
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


    def initialize_portfolio(self):
        self.hold = rd.sample([-1, 0, 1], 1)[0]
        self.cash = Constants.starting_cash - (self.hold * Constants.start_price)
        self.base_price = abs(self.hold * Constants.start_price)
        self.returns = 0

    def update_vars(self):
        future_me = self.in_round(self.round_number + 1)
        i_round = self.round_number

        # Base Price
        if self.transaction != 0 and self.hold + self.transaction != 0:
            future_me.base_price = self.participant.vars['price_path'][i_round - 1]
        elif self.transaction == 0:
            future_me.base_price = self.base_price
        else:
            future_me.base_price = 0

        # Cash and belief before last period
        future_me.cash = self.cash -\
            (self.transaction * self.participant.vars['price_path'][i_round - 1])

        # Holdings
        future_me.hold = self.hold + self.transaction

        # Returns
        future_me.returns = int(future_me.hold * (self.participant.vars['price_path'][i_round] - future_me.base_price))

    # Display functions:
    def get_tutorial_vars(self):
        return {'n_rounds': Constants.num_rounds,
                'n_rounds_per_block': Constants.n_periods_per_block,
                'movements': Constants.updates,
                'example_move': [i + 1000 for i in Constants.updates],
                'n_blocks': Constants.num_blocks,
                'max_time': Constants.max_time,
                'start_price': Constants.start_price,
                'start_cash': Constants.starting_cash,
                'start_value': Constants.start_hold * Constants.start_price,
                'value_all': (Constants.start_hold * Constants.start_price + Constants.starting_cash),
                'non_switch_prob': int((1 - Constants.switch_prob) * 100),
                'switch_prob': int(Constants.switch_prob * 100),
                'raise_prob_good': int(Constants.up_prob * 100),
                'fall_prob_good': int((1 - Constants.up_prob) * 100),
                'update_time': Constants.update_time,
                'belief_elicitation': self.participant.vars['belief_elicitation'],
                'lottery_bonus': Constants.lottery_bonus,
                'lottery_discount': round(Constants.lottery_discount * 100, 2),
                'main_condition': self.participant.vars['main_condition'],
                'base_bonus': self.session.config['base_bonus'],
                'conversion_percent': round(self.session.config['real_world_currency_per_point'] * 100, 2),
                'showup_fee': self.session.config['participation_fee'],
                'example_payoff': self.session.config['participation_fee'] + self.session.config['base_bonus'] +
                100 * self.session.config['real_world_currency_per_point']
                }

    def get_trading_vars(self):
        price = self.participant.vars['price_path'][self.round_number - 1]

        percentage_returns = 0
        if self.base_price != 0:
            percentage_returns = round((self.returns / self.base_price) * 100, 1)

        return {'price': price,
                'cash': int(self.cash),
                'hold': self.hold,
                'base_price': round(self.base_price, 2),
                'percentage_returns': percentage_returns,
                'all_val': price * self.hold,
                'wealth': int(price * self.hold + self.cash),
                'max_time': Constants.max_time,
                'main_condition': self.participant.vars['main_condition'],
                }
