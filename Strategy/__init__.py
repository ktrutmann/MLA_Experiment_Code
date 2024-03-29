from otree.api import *


author = 'Kevin Trutmann'
doc = """
Strategy questionnaire
"""


class Constants(BaseConstants):
    name_in_url = 'Strategy'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    strategy = models.LongStringField()
    strategy_random = models.IntegerField(
        choices=[i + 1 for i in range(7)],
        widget=widgets.RadioSelectHorizontal(),
        label='I sold and bought the asset mainly randomly.',
    )
    strategy_feeling = models.IntegerField(
        choices=[i + 1 for i in range(7)],
        widget=widgets.RadioSelectHorizontal(),
        label='I trusted my feelings about the price development.',
    )
    strategy_rational = models.IntegerField(
        choices=[i + 1 for i in range(7)],
        widget=widgets.RadioSelectHorizontal(),
        label='I invested whenever I thought it was more likely than 50% that '
        'the price will increase.',
    )
    strategy_short_rational = models.IntegerField(
        choices=[i + 1 for i in range(7)],
        widget=widgets.RadioSelectHorizontal(),
        label='I short sold whenever I thought it was more likely than '
        '50% that the price will decrease.',
    )
    strategy_risk_averse = models.IntegerField(
        choices=[i + 1 for i in range(7)],
        widget=widgets.RadioSelectHorizontal(),
        label='I only invested when I was very certain that the price would ' 'increase.',
    )
    strategy_short_risk_averse = models.IntegerField(
        choices=[i + 1 for i in range(7)],
        widget=widgets.RadioSelectHorizontal(),
        label='I only short sold when I was very certain that the price' 'would increase.',
    )
    strategy_inertia = models.IntegerField(
        choices=[i + 1 for i in range(7)],
        widget=widgets.RadioSelectHorizontal(),
        label='I tried to keep an investment or short position for as long as' ' possible.',
    )
    strategy_DE = models.IntegerField(
        choices=[i + 1 for i in range(7)],
        widget=widgets.RadioSelectHorizontal(),
        label='I tried to only sell the asset / buy back short positions when I had '
        'made a profit from it.',
    )
    strategy_anti_DE = models.IntegerField(
        choices=[i + 1 for i in range(7)],
        widget=widgets.RadioSelectHorizontal(),
        label='If I had made a loss, I tried to get rid of that investment as '
        'quick as possible.',
    )


# FUNCTIONS
# PAGES
class open_strategy_page(Page):
    form_model = 'player'
    form_fields = ['strategy']


class closed_strategy_page(Page):
    form_model = 'player'
    form_fields = [
        'strategy_random',
        'strategy_feeling',
        'strategy_rational',
        'strategy_short_rational',
        'strategy_short_risk_averse',
        'strategy_risk_averse',
        'strategy_inertia',
        'strategy_DE',
        'strategy_anti_DE',
    ]


page_sequence = [open_strategy_page, closed_strategy_page]
