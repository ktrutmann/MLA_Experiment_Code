from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class open_strategy_page(Page):
    form_model = 'player'
    form_fields = ['strategy']


class closed_strategy_page(Page):
    form_model = 'player'
    form_fields = ['strategy_random', 'strategy_feeling', 'strategy_rational',
                   'strategy_short_rational', 'strategy_short_risk_averse', 'strategy_risk_averse',
                   'strategy_inertia', 'strategy_DE', 'strategy_anti_DE']


class demographics_page(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'is_student', 'study_field',
                   'investment_experience', 'purpose', 'engagement', 'interest']

class comments_page(Page):
    form_model = 'player'
    form_fields = ['general_comments']


page_sequence = [
    open_strategy_page,
    closed_strategy_page,
    demographics_page,
    comments_page
]
