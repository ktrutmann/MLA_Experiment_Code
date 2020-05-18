from otree.api import (BaseGroup, BaseSubsession)

from Investment_Task.models import Constants as MainConstants
from Investment_Task.models import MainPlayer

author = 'Kevin Trutmann'

doc = """
Tutorial for the investment Task
"""


class Constants(MainConstants):
    name_in_url = 'Tutorial_Investment_Task'
    num_training_blocks_per_condition = 1
    num_paths = num_training_blocks_per_condition * len(MainConstants.condition_names)
    num_rounds = num_training_blocks_per_condition * MainConstants.n_periods_per_phase * sum(MainConstants.n_phases) +\
        num_paths + sum(MainConstants.extra_inv_phase) * num_training_blocks_per_condition  # Number of training rounds

    shuffle_conditions = False

    # Parameters specifically for the tutorial text
    num_blocks = MainConstants.num_paths
    n_conditions = len(set(MainConstants.condition_names))


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(MainPlayer):
    def get_tutorial_vars(self):
        rounds_per_block_set = {Constants.n_periods_per_phase * Constants.n_phases[i] +
                                Constants.extra_inv_phase[i] for i, _ in enumerate(Constants.condition_names)}
        return {
                'n_rounds_per_block_list': list(rounds_per_block_set),
                'good_raise_prob': round(max(Constants.up_probs) * 100),
                'bad_raise_prob': round(min(Constants.up_probs) * 100),
                'example_move': [i + 1000 for i in Constants.updates],
                'start_price_twice': Constants.start_price * 2,
                'base_bonus': self.session.config['base_bonus'],
                'conversion_percent': round(self.session.config['real_world_currency_per_point'] * 100, 2),
                'showup_fee': self.session.config['participation_fee'],
                'example_payoff': self.session.config['participation_fee'] + self.session.config['base_bonus'] +
                100 * self.session.config['real_world_currency_per_point']
                }
