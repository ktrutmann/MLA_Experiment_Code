from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Kevin Trutmann'

doc = """
Your app description
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
