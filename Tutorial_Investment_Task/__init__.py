import time
from Investment_Task import Constants as MainConstants
from Investment_Task import (initialize_round, should_display_infos)
from Investment_Task import condition_page, trading_page, belief_page, update_page
from otree.api import *


author = 'Kevin Trutmann'
doc = """
Tutorial for the investment Task
"""


class Constants(MainConstants):
    name_in_url = 'Tutorial_Investment_Task'
    num_tutorial_paths = len(MainConstants.condition_names)
    num_rounds = num_tutorial_paths * (MainConstants.n_rounds_per_path + 1)  # Number of training rounds
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
    prolific_id = models.StringField(label='Prolific ID:')
    Q1 = models.IntegerField(widget=widgets.RadioSelect, blank=True,
                            label='A decrease in the assets price is...',
                            choices=[[1, '...more likely during an upward trend.'],
                                     [2, '...more likely during a downward trend.'],
                                     [3, '...equally likely during an upward as during a downward trend.']])
    Q2 = models.IntegerField(widget=widgets.RadioSelect, blank=True,
                            label='A price increase of 15 points is...',
                            choices=[[1, '...always equally as likely as an increase of 10.'],
                                     [2, '...more likely than a price increase of 10 if the asset has an upward trend.'],
                                     [3, '...always equally as likely as a decrease of 15 points.']])
    Q3 = models.IntegerField(widget=widgets.RadioSelect, blank=True,
                            label='When the asset has a downward trend...',
                            choices=[[1, '...there is a 50% chance that the price will in- or decrease.'],
                                     [2, '...there is a 35% chance that the price will increase and a 65% chance that it will decrease.'],
                                     [3, '...there is a 35% chance that the price will decrease and a 65% chance that it will increase.']])
    Q4 = models.IntegerField(widget=widgets.RadioSelect, blank=True,
                            label='Imagine that you have short sold the asset by two shares (i.e. you hold -2 shares). Which statement is correct?',
                            choices=[[1, 'If the asset has an upward trend, the value of your portfolio is more likely to increase now.'],
                                     [2, 'If the price decreases by 10 points, the value of your portfolio will decrease by 20 points.'],
                                     [3, 'If the price decreases by 15 points, the value of your portfolio will increase by 30 points.']])
    wrong_answers = models.IntegerField()

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
        player.timestamp = time.time()
        initialize_round(player,
            n_distinct_paths=len(Constants.condition_names),
            training=True)

class prolific_ID_page(Page):
    form_model = 'player'
    form_fields = ['prolific_id']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class tutorial_page(Page):
    form_model = 'player'
    form_fields = ['transaction']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return get_tutorial_vars(player)


class quiz_page(Page):
    form_model = 'player'
    form_fields = ['Q1', 'Q2', 'Q3', 'Q4', 'wrong_answers']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class end_page(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds


page_sequence = [
    prolific_ID_page,
    initializer_page,
    tutorial_page,
    quiz_page,
    condition_page,
    trading_page,
    belief_page,
    update_page,
    end_page,
]
