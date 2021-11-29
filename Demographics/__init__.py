from otree.api import *
import time

# TODO: (2) Separate away Demographics and put them at the end!

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
    age = models.IntegerField(min=10, max=100)
    gender = models.StringField(
        choices=['Male', 'Female', 'Other', 'No Answer'], widget=widgets.RadioSelect()
    )
    is_student = models.StringField(choices=['Yes', 'No'], widget=widgets.RadioSelectHorizontal())
    study_field = models.StringField(blank=True)
    investment_experience = models.IntegerField(
        label='On a scale from 0-5, how much experience do you have with '
        'investment decisions (i.e. trading stocks / bonds ect.)? '
        '(0 = No experience at all, 5 = Professional Investor',
        choices=list(range(6)),
        widget=widgets.RadioSelectHorizontal(),
    )
    purpose = models.LongStringField(blank=True, label='')
    engagement = models.IntegerField(
        label='On a scale from 1-7, how attentive were you throughout the study?',
        choices=[i + 1 for i in range(7)],
        widget=widgets.RadioSelectHorizontal(),
    )
    interest = models.IntegerField(
        label='On a scale from 1-7, how engaging did you find the task?',
        choices=[i + 1 for i in range(7)],
        widget=widgets.RadioSelectHorizontal(),
    )
    pattern = models.LongStringField(blank=True, label='')
    dont_use_data = models.LongStringField(blank=True, label='') 
    general_comments = models.LongStringField(blank=True, label='')
    timestamp = models.FloatField()


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


class demographics_page(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'is_student',
        'study_field',
        'investment_experience',
        'purpose',
        'engagement',
        'interest',
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
        player.timestamp = time.time() # TODO: (6) Test this!


page_sequence = [open_strategy_page, closed_strategy_page, demographics_page, comments_page]
