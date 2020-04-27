from otree.api import (
    models, BaseGroup, BasePlayer, widgets
)
import random as rd
import pandas as pd

from Investment_Task.models import Constants as mainConstants, mainSubsession


author = 'Kevin Trutmann'

doc = """
Tutorial for the Trading Task
"""

# TODO (After Pilot): Also update the readme
# TODO (After Pilot): Put the belief page in a template as well

class Constants(mainConstants):
    name_in_url = 'Tutorial_Investment_Task'
    # TODO (After Pilot): Bring back training rounds!
    num_rounds = 1  # Number of training rounds

    # Parameters specifically for the tutorial text
    num_blocks = mainConstants.num_paths
    n_conditions = len(set(mainConstants.condition_names))


class Subsession(mainSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    participant_name = models.StringField(label='Vor und Nachname')
    transaction = models.IntegerField(label='', blank=True)

    # TODO (After Pilot): Bring back the quizz
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
        max_moves_per_path = Constants.n_periods_per_phase * max(Constants.n_phases) + 1

        for this_drift in drift_list:
            moves = []

            for _ in range(max_moves_per_path):
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
                # Trim the path if the last phase is not needed in this condition:
                all_moves_list[i_cond][i_path] = all_moves_list[i_cond][i_path][:Constants.n_periods_per_phase *
                                                                                Constants.n_phases[i_cond] + 1]

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
        # Not too elegant with the for loops, but it does the trick...
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
            grouped_df = [group for _, group in price_df.groupby('condition_id')]
            rd.shuffle(grouped_df)
            price_df = pd.concat(grouped_df).reset_index

        self.participant.vars['price_info'] = price_df


    def initialize_round(self):
        # If this is the very first round
        if self.round_number == 1:
            self.make_price_paths()

        # Record the relevant price variables into the database:
        for this_var in ['price', 'drift', 'condition_name', 'i_round_in_path', 'global_path_id', 'distinct_path_id']:
            setattr(self, this_var, self.participant.vars['price_info'][this_var][self.round_number - 1])

        # If this is the first round of a new path:
        if self.participant.vars['price_info'].i_round_in_path[self.round_number - 1] == 0:
            self.hold = rd.choice(range(Constants.hold_range[0], Constants.hold_range[1] + 1))
            self.cash = Constants.starting_cash - (self.hold * Constants.start_price)
            self.base_price = Constants.start_price if self.hold != 0 else 0
            self.returns = 0
            self.belief_bonus_cumulative = 0
            self.price = Constants.start_price
        else:
            former_self = self.in_round(self.round_number - 1)
            self.hold = former_self.hold + former_self.transaction
            self.cash = former_self.cash - former_self.transaction *\
                self.participant.vars['price_info'].price[self.round_number - 2]
            former_self.belief_bonus_cumulative += former_self.belief_bonus
            self.belief_bonus_cumulative = former_self.belief_bonus_cumulative

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
                                   self.participant.vars['price_info'].price[self.round_number - 2]) /\
                                   abs(self.hold)

            self.returns = self.hold *\
                (self.participant.vars['price_info'].price[self.round_number - 1] - self.base_price)

            # If this is the last round of a block:
            if self.round_number == Constants.num_rounds or\
                    self.participant.vars['price_info'].i_round_in_path[self.round_number] == 0:
                self.belief_bonus = 0
                self.belief_bonus_cumulative = self.in_round(self.round_number - 1).belief_bonus_cumulative
                # "Sell everything" for the last price:
                self.final_cash = self.cash + self.hold *\
                    self.participant.vars['price_info'].price[self.round_number - 1]
                self.payoff = (self.final_cash - Constants.starting_cash) + self.belief_bonus_cumulative


    # Display functions:
    def get_tutorial_vars(self):
        return {'n_rounds': Constants.num_rounds,
                'n_rounds_per_block_list': [Constants.n_periods_per_phase * i for i in set(Constants.n_phases)],
                'n_rounds_per_phase': Constants.n_periods_per_phase,
                'min_hold': Constants.hold_range[0],
                'max_hold': Constants.hold_range[1],
                'good_raise_prob': round(max(Constants.up_probs) * 100),
                'bad_raise_prob': round(min(Constants.up_probs) * 100),
                'lottery_bonus': Constants.max_belief_bonus,
                'lottery_discount': round(Constants.belief_bonus_discount * 100),
                'movements': Constants.updates,
                'example_move': [i + 1000 for i in Constants.updates],
                'n_blocks': Constants.num_blocks,
                'max_time': Constants.max_time,
                'start_price': Constants.start_price,
                'start_cash': Constants.starting_cash,
                'update_time': Constants.update_time,
                'max_belief_bonus': Constants.max_belief_bonus,
                'belief_bonus_discount': round(Constants.belief_bonus_discount * 100, 2),
                'base_bonus': self.session.config['base_bonus'],
                'conversion_percent': round(self.session.config['real_world_currency_per_point'] * 100, 2),
                'showup_fee': self.session.config['participation_fee'],
                'example_payoff': self.session.config['participation_fee'] + self.session.config['base_bonus'] +
                100 * self.session.config['real_world_currency_per_point']
                }

    # For displaying the page
    def get_trading_vars(self):
        price = self.participant.vars['price_info'].price[self.round_number - 1]

        percentage_returns = 0
        if self.base_price != 0:
            percentage_returns = round((self.returns / self.base_price) * 100, 1)

        return {'price': price,
                'cash': self.cash,
                'hold': self.hold,
                'min_hold': Constants.hold_range[0],
                'max_hold': Constants.hold_range[1],
                'base_price': self.base_price,
                'percentage_returns': percentage_returns,
                'all_val': price * self.hold,
                'wealth': int(price * self.hold + self.cash),
                'max_time': Constants.max_time,
                'condition': self.participant.vars['price_info'].condition_name[self.round_number - 1]
                }