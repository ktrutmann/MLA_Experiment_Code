from typing import TypedDict
from otree.api import *


doc = """
The general risk and financial risk questions of the Socioeconomic pannel risk questionnaire
https://www.diw.de/documents/publikationen/73/diw_01.c.571151.de/diw_ssp0423.pdf
Also the SOEP Ambiguity and Loss Aversion questions.
An "implusivenes" question from Chapman, J., Dean, M., Ortoleva, P., Snowberg, E., & Camerer, C. (2018). Econographics (No. w24931). National Bureau of Economic Research.
Lastly the patience question from Falk et al. (2018) was also used
(Falk, A., Becker, A., Dohmen, T., Enke, B., Huffman, D. & Sunde, U. (2018). Global Evidence on Economic Preferences).
"""


class Constants(BaseConstants):
    name_in_url = 'individual_measures'
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
    soep_finance = models.IntegerField(
        choices=[i for i in range(11)],
        widget=widgets.RadioSelectHorizontal(),
        label='')
    soep_ambiguity = models.IntegerField(
        choices=[i for i in range(11)],
        widget=widgets.RadioSelectHorizontal(),
        label='')
    soep_loss_aversion = models.IntegerField(
        choices=[i for i in range(11)],
        widget=widgets.RadioSelectHorizontal(),
        label='')
    falk_patience_question = models.IntegerField(
        choices=[i for i in range(11)],
        widget=widgets.RadioSelectHorizontal(),
        label='')
    chapman_impulse_question = models.IntegerField(
        choices=[i for i in range(11)],
        widget=widgets.RadioSelectHorizontal(),
        label='')
    prob_no_dept_payment = models.IntegerField(min=0, max=100, label='')


# PAGES
class soep_general_page(Page):
    form_model = 'player'
    form_fields = ['soep_general']

class soep_finance_page(Page):
    form_model = 'player'
    form_fields = ['soep_finance']

class soep_ambiguity_page(Page):
    form_model = 'player'
    form_fields = ['soep_ambiguity']

class soep_loss_aversion_page(Page):
    form_model = 'player'
    form_fields = ['soep_loss_aversion']

class falk_patience_page(Page):
    form_model = 'player'
    form_fields = ['falk_patience_question']

class chapman_impulse_page(Page):
    form_model = 'player'
    form_fields = ['chapman_impulse_question']

class dept_payment_page(Page):
    form_model = 'player'
    form_fields = ['prob_no_dept_payment']


page_sequence = [
    soep_general_page,
    soep_finance_page,
    soep_ambiguity_page,
    soep_loss_aversion_page,   
    falk_patience_page,
    chapman_impulse_page,
    dept_payment_page]