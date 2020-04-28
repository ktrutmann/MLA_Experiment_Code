from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class payment_info_page(Page):
    form_model = 'player'
    form_fields = ['matr_nr']


page_sequence = [
    payment_info_page,
]
