from otree.api import *


author = 'Kevin Trutmann'
doc = """
Whatever information we need to pay the participants
"""


class Constants(BaseConstants):
    name_in_url = 'get_info'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    matr_nr = models.StringField(label='Matricle-Nr')


# FUNCTIONS
# PAGES
class payment_info_page(Page):
    form_model = 'player'
    form_fields = ['matr_nr']


page_sequence = [
    payment_info_page,
]
