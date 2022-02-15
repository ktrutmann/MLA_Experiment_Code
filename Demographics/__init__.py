from random import choice
from numpy import mod
from otree.api import *
import time


author = 'Kevin Trutmann'
doc = """
Demographics questionnaire,
partially taken from the New York Fed survey:
    https://www.newyorkfed.org/medialibrary/interactives/sce/sce/downloads/
    data/frbny-sce-survey-core-module-public-questionnaire.pdf
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
    age = models.IntegerField(label='Age', min=10, max=100)
    gender = models.StringField(label='Gender',
        choices=['Male', 'Female', 'Other', 'No Answer'],
        widget=widgets.RadioSelect())
    income_bracket = models.IntegerField(
        label='Which category represents the total combined pre-tax income of all members of' +\
            ' your household (including you) during the past 12 months?',
            choices=[[999, 'Prefer not to answer'],
                [1, 'Less than $10,000'],
                [2, '$10,000 to $19,999'],
                [3, '$20,000 to $29,999'],
                [4, '$30,000 to $39,999'],
                [5, '$40,000 to $49,999'],
                [6, '$50,000 to $59,999'],
                [7, '$60,000 to $74,999'],
                [8, '$75,000 to $99,999'],
                [9, '$100,000 to $149,999'],
                [10, '$150,000 to $199,999'],
                [11, '$200,000 or more']],
        widget=widgets.RadioSelect())
    household_size = models.IntegerField(
        label='How many people (including you) live in your Household?', min=1)
    household_children = models.IntegerField(
        label='How many of the people living in your household are children under the age of 18?', min=1)
    ethnicity = models.StringField(
        label='Please choose the race that you would most consider yourself to be:',
        choices=['White / Caucasian', 'Black or African American',
            'American Indian or Alaska Native', 'Asian',
            'Native Hawaiian or Other Pacific Islander'],
        widget=widgets.RadioSelect())
    education = models.IntegerField(
        label='What is the highest level of school you have completed or the highest degree you have received?',
        choices=[[1, 'Less than high school'],
               [2, 'High school diploma (or equivalent)'],
               [3, 'Some college but no degree (including academic, vocational, or occupational programs)'],
               [4, 'Associate / Junior College degree (including academic, vocational, or occupational programs)'],
               [5, 'Bachelor degree (For example: BA, BS)'],
               [6, 'Master\'s Degree (For example: MA, MBA, MS, MSW)'],
               [7, 'Doctoral Degree (For example: PhD)'],
               [8, 'Professional Degree (For example: MD, JD, DDS)'],
               [999, 'Prefer not to say']],
        widget=widgets.RadioSelect())
    math_abilities_self_report = models.IntegerField(
        label='How would you rate your mathematical and statistical abilities from  grades A - F?',
        choices=[[6, 'A'], [5, 'B'], [4, 'C'], [3, 'D'], [2, 'E'], [1, 'F']],
        widget=widgets.RadioSelectHorizontal())
    games_of_chance = models.BooleanField(
        label='Have you played any games of chance in the last 12 months (e.g. online, at the casino)?',
        choices=[[True, 'Yes'], [False, 'No']],
        widget=widgets.RadioSelectHorizontal())
    traded_stocks = models.BooleanField(
        label='Have you ever traded stocks?',
        choices=[[True, 'Yes'], [False, 'No']],
        widget=widgets.RadioSelectHorizontal())
    investment_experience = models.IntegerField(
        label='On a scale from 0-5, how much experience do you have with '
        'investment decisions (i.e. trading stocks / bonds ect.)?<br> '
        '(0 = No experience at all, 5 = Professional Investor)',
        choices=list(range(6)),
        widget=widgets.RadioSelectHorizontal())
    purpose = models.LongStringField(blank=True,
        label='Do you have an idea what the purpose of this study is?')
    attentiveness = models.IntegerField(
        label='On a scale from 0-5, how attentive were you throughout the study?',
        choices=list(range(6)),
        widget=widgets.RadioSelectHorizontal())
    attention_check = models.IntegerField(
        label='To ensure you are not an automated program or just clicking through the study, ' +
            'please answer this question with a value of 1.',
        choices=list(range(6)),
        widget=widgets.RadioSelectHorizontal())
    engagement = models.IntegerField(
        label='On a scale from 0-5, how engaging did you find the task?',
        choices=list(range(6)),
        widget=widgets.RadioSelectHorizontal())
    pattern = models.LongStringField(blank=True, label='')
    noticed_repetitions = models.BooleanField(label='',
        choices=[[True, 'Yes'], [False, 'No']], widget=widgets.RadioSelect())
    dont_use_data = models.BooleanField(label='',
        choices=[[True, 'Yes'], [False, 'No']], widget=widgets.RadioSelect())
    dont_use_data_reason = models.LongStringField(blank=True, label='') 
    general_comments = models.LongStringField(blank=True, label='')
    timestamp = models.FloatField()


# FUNCTIONS
# PAGES
class demographics_page(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'ethnicity',
        'education',
        'math_abilities_self_report',
        'attention_check',
        'attentiveness',
        'engagement',
        'household_size',
        'household_children',
        'income_bracket',
        'games_of_chance',
        'traded_stocks',
        'investment_experience',
        'purpose',
    ]


class comments_page(Page):
    form_model = 'player'
    form_fields = [
        'pattern',
        'noticed_repetitions',
        'dont_use_data',
        'dont_use_data_reason',
        'general_comments'
    ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.timestamp = time.time()


page_sequence = [demographics_page, comments_page]
