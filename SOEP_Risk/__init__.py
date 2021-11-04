from otree.api import *


doc = """
The Socioeconomic pannel risk questionnaire
https://www.diw.de/documents/publikationen/73/diw_01.c.571151.de/diw_ssp0423.pdf
"""


class Constants(BaseConstants):
    name_in_url = 'soep_risk'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    soep_general = models.IntegerField(
    choices=[i for i in range(11)],
    widget=widgets.RadioSelectHorizontal(),
    label='')
    soep_driving = models.IntegerField(
    choices=[i for i in range(11)],
    widget=widgets.RadioSelectHorizontal(),
    label='')
    soep_finance = models.IntegerField(
    choices=[i for i in range(11)],
    widget=widgets.RadioSelectHorizontal(),
    label='')
    soep_leisure = models.IntegerField(
    choices=[i for i in range(11)],
    widget=widgets.RadioSelectHorizontal(),
    label='')
    soep_occupation = models.IntegerField(
    choices=[i for i in range(11)],
    widget=widgets.RadioSelectHorizontal(),
    label='')
    soep_health = models.IntegerField(
    choices=[i for i in range(11)],
    widget=widgets.RadioSelectHorizontal(),
    label='')
    soep_faith_in_people = models.IntegerField(
    choices=[i for i in range(11)],
    widget=widgets.RadioSelectHorizontal(),
    label='')


# PAGES
class soep_general_page(Page):
    form_model = 'player'
    form_fields = ['soep_general']

class soep_driving_page(Page):
    form_model = 'player'
    form_fields = ['soep_driving']

class soep_finance_page(Page):
    form_model = 'player'
    form_fields = ['soep_finance']

class soep_leisure_page(Page):
    form_model = 'player'
    form_fields = ['soep_leisure']

class soep_occupation_page(Page):
    form_model = 'player'
    form_fields = ['soep_occupation']

class soep_health_page(Page):
    form_model = 'player'
    form_fields = ['soep_health']

class soep_faith_in_people_page(Page):
    form_model = 'player'
    form_fields = ['soep_faith_in_people']


page_sequence = [
    soep_general_page,
    soep_driving_page,
    soep_finance_page,
    soep_leisure_page,
    soep_occupation_page,
    soep_health_page,
    soep_faith_in_people_page]
