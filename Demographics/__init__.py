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
    # TODO: (1) Replace is_student with "holds_stocks"
    # TODO: (4) Add the following questions:

# Have you ever traded stocks?	" [1, 'Yes'],
#            [0, 'No']"
#What is the highest level of school you have completed or the highest degree you have received?	"[1, 'less than high school degree'],
#            [2, 'high school degree or equivalent (e.g., GED)'],
#            [3, 'Some college but no degree'],
#            [4, 'Associate degree'],
#            [5, 'Bachelor degree'],
#            [6, 'Graduate degree'],
#            [0, 'Prefer not to say']"
#How good are your mathematical and statistical abilities from  grades A - F?	"[6, 'A'],
#            [5, 'B'],
#            [4, 'C'],
#            [3, 'D'],
#            [2, 'E'],
#            [1, 'F']"
#Have you played any games of chance in the last 12 months (e.g. online, at the casino)?'	"[1, 'Yes'],
#            [0, 'No']"
            
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
