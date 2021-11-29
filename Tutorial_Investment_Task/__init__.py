import copy
import random as rd
from numpy import tracemalloc_domain
import pandas as pd
import time
from Investment_Task import Constants as MainConstants
from Investment_Task import (make_price_paths, initialize_round, is_investable,
    should_display_infos, get_investment_span, get_trading_vars, make_update_list,
    calculate_final_payoff)
from Investment_Task import condition_page, trading_page, belief_page, update_page
from otree.api import *


author = 'Kevin Trutmann'
doc = """
Tutorial for the investment Task
"""


class Constants(MainConstants):
    name_in_url = 'Tutorial_Investment_Task'
    num_training_blocks_per_condition = 1
    num_tutorial_paths = num_training_blocks_per_condition * len(MainConstants.condition_names)
    num_rounds = num_tutorial_paths * MainConstants.n_rounds_per_path  # Number of training rounds
    shuffle_conditions = False
    # Constants specifically for the tutorial text
    num_blocks = MainConstants.num_paths
    n_conditions = len(set(MainConstants.condition_names))


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    transaction = models.IntegerField(label='')
    time_to_order = models.FloatField()
    unfocused_time_to_order = models.FloatField()
    changed_mind = models.BooleanField()
    erroneous_trade = models.StringField()
    belief = models.IntegerField(min=0, max=100, label='')
    time_to_belief_report = models.FloatField()
    unfocused_time_to_belief_report = models.FloatField()
    update_time_used = models.FloatField()
    price = models.IntegerField()
    cash = models.IntegerField()
    hold = models.IntegerField()
    base_price = models.FloatField()
    returns = models.IntegerField()
    final_cash = models.CurrencyField()
    i_round_in_path = models.IntegerField()
    investable = models.BooleanField()
    global_path_id = models.IntegerField()
    distinct_path_id = models.IntegerField()
    drift = models.FloatField()
    condition_name = models.StringField()
    timestamp = models.FloatField()


# FUNCTIONS
def get_tutorial_vars(player: Player):
    return {
        'n_rounds_per_block': MainConstants.n_rounds_per_path,
        'good_raise_prob': round(max(Constants.up_probs) * 100),
        'bad_raise_prob': round(min(Constants.up_probs) * 100),
        'example_move': [i + 1000 for i in Constants.updates],
        'start_price_twice': Constants.start_price * 2,
        'start_value': Constants.start_price * 2 + Constants.starting_cash,
        'base_bonus': player.session.config['base_bonus'],
        'conversion_percent': round(
            player.session.config['real_world_currency_per_point'] * 100, 2
        ),
        'showup_fee': player.session.config['participation_fee'],
        'example_payoff': player.session.config['participation_fee']
        + player.session.config['base_bonus']
        + 100 * player.session.config['real_world_currency_per_point'],
    }


# PAGES
class initializer_page(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.timestamp = time.time() # TODO: (5) Test this!
        initialize_round(player, n_distinct_paths=Constants.num_training_blocks_per_condition)


class tutorial_page(Page):
    form_model = 'player'
    form_fields = ['transaction']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return get_tutorial_vars(player)


class end_page(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds


page_sequence = [
    initializer_page,
    tutorial_page,
    condition_page,
    trading_page,
    belief_page,
    update_page,
    end_page,
]
