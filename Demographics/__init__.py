from otree.api import *
import time


author = 'Kevin Trutmann'
doc = """
Demographics questionnaire
"""


class Constants(BaseConstants):
    name_in_url = 'Demographics'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(min=10, max=100)
    gender = models.StringField(
        choices=['Male', 'Female', 'Other', 'No Answer'], widget=widgets.RadioSelect()
    )
    is_student = models.StringField(choices=['Yes', 'No'], widget=widgets.RadioSelectHorizontal())
    study_field = models.StringField(blank=True)
    investment_experience = models.IntegerField(
        label='On a scale from 0-5, how much experience do you have with '
        'investment decisions (i.e. trading stocks / bonds ect.)?<br> '
        '(0 = No experience at all, 5 = Professional Investor)',
        choices=list(range(6)),
        widget=widgets.RadioSelectHorizontal(),
    )
    purpose = models.LongStringField(blank=True,
        label='Do you have an idea what the purpose of this study is?')
    attentiveness = models.IntegerField(
        label='On a scale from 0-5, how attentive were you throughout the study?',
        choices=list(range(6)),
        widget=widgets.RadioSelectHorizontal(),
    )
    attention_check = models.IntegerField(
        label='To ensure you are not an automated program or just clicking through the study, ' +
            'please answer this question with a value of 1.',
        choices=list(range(6)),
        widget=widgets.RadioSelectHorizontal(),
    )
    engagement = models.IntegerField(
        label='On a scale from 0-5, how engaging did you find the task?',
        choices=list(range(6)),
        widget=widgets.RadioSelectHorizontal(),
    )
    pattern = models.LongStringField(blank=True, label='')
    dont_use_data = models.LongStringField(blank=True, label='') 
    general_comments = models.LongStringField(blank=True, label='')
    timestamp = models.FloatField()


# FUNCTIONS
# PAGES
class demographics_page(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'is_student',
        'study_field',
        'investment_experience',
        'purpose',
        'attention_check',
        'attentiveness',
        'engagement',
    ]


class comments_page(Page):
    form_model = 'player'
    form_fields = [
        'pattern',
        'dont_use_data',
        'general_comments'
    


    ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.timestamp = time.time()


page_sequence = [demographics_page, comments_page]
