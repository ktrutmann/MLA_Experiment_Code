from otree.api import *
import time

author = 'Adrian Leuenberger / Kevin Trutmann'

doc = """
Raven’s Progressive Matrices (RPM)
Civalli, A. & Deck, S. (2017). A Flexible and Customizable Method for Assessing Cognitive Abilities:
https://digitalcommons.chapman.edu/cgi/viewcontent.cgi?article=1220&context=esi_working_papers
"""

class Constants(BaseConstants):
    name_in_url = 'RPM'
    players_per_group = None
    num_rounds = 1
    endowment = 10  # TODO: (4) Adjust endowment!


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    cogn_rpm_matrix_1 = models.IntegerField(
        choices=[[0, 'A'], [1, 'B'], [2, 'C'], [3, 'D'], [4, 'E'], [5, 'F']],
        label='Select the element which best fits the missing picture:',
        widget=widgets.RadioSelectHorizontal)
    cogn_rpm_matrix_2 = models.IntegerField(
        choices=[[0, 'A'], [1, 'B'], [2, 'C'], [3, 'D'], [4, 'E'], [5, 'F']],
        label='Select the element which best fits the missing picture:',
        widget=widgets.RadioSelectHorizontal)
    cogn_rpm_matrix_3 = models.IntegerField(
        choices=[[0, 'A'], [1, 'B'], [2, 'C'], [3, 'D'], [4, 'E'], [5, 'F']],
        label='Select the element which best fits the missing picture:',
        widget=widgets.RadioSelectHorizontal)
    cogn_rpm_matrix_4 = models.IntegerField(
        choices=[[0, 'A'], [1, 'B'], [2, 'C'], [3, 'D'], [4, 'E'], [5, 'F']],
        label='Select the element which best fits the missing picture:',
        widget=widgets.RadioSelectHorizontal)
    cogn_rpm_matrix_5 = models.IntegerField(
        choices=[[0, 'A'], [1, 'B'], [2, 'C'], [3, 'D'], [4, 'E'], [5, 'F']],
        label='Select the element which best fits the missing picture:',
        widget=widgets.RadioSelectHorizontal)
    cogn_rpm_matrix_6 = models.IntegerField(
        choices=[[0, 'A'], [1, 'B'], [2, 'C'], [3, 'D'], [4, 'E'], [5, 'F']],
        label='Select the element which best fits the missing picture:',
        widget=widgets.RadioSelectHorizontal)
    cogn_rpm_total_points = models.IntegerField(initial=None)
    pers_rpm_overestimation_answer = models.IntegerField(label='Amount:', min=0, max=6)
    pers_rpm_overestimation_score = models.IntegerField()
    pers_rpm_overplacement_answer = models.IntegerField(label='Rank:', min=1, max=100)

def add_earnings_to_payoff(player: Player):
    # TODO: (5) Test whether the bonus propagates till the end.
    answer_key = [1, 5, 4, 3, 0, 0]
    total_score = 0

    for i, this_right_answer in enumerate(answer_key):
        total_score += getattr(player, f'cogn_rpm_matrix_{i + 1}') == this_right_answer
    player.cogn_rpm_total_points = total_score
    player.payoff = cu(player.cogn_rpm_total_points * Constants.endowment)


# Pages: ----
class Introduction_1(Page):
    form_model = 'player'
    

class Introduction_2(Page):
    form_model = 'player'
    

class Introduction_3(Page):
    form_model = 'player'
    

class Introduction_4(Page):
    form_model = 'player'
    

class Start(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # user has 3 minutes to complete as many pages as possible
        player.participant.vars['expiry'] = time.time() + 4.5*60


class Matrix_Page(Page):
    form_model = 'player'
    form_fields = ['cogn_rpm_matrix_1', 'cogn_rpm_matrix_2',
    	'cogn_rpm_matrix_3', 'cogn_rpm_matrix_4',
        'cogn_rpm_matrix_5', 'cogn_rpm_matrix_6',]
    timer_text = 'Remaining time:'

    @staticmethod
    def get_timeout_seconds(player: Player):
	    return player.participant.vars['expiry'] - time.time()

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        add_earnings_to_payoff(player)

class Overestimation(Page):
    form_model = 'player'
    form_fields = ['pers_rpm_overestimation_answer']


class Overplacement(Page):
    form_model = 'player'
    form_fields = ['pers_rpm_overplacement_answer']


page_sequence = [
    Introduction_1, 
    Introduction_2,
    Introduction_3,
    Introduction_4,
    Start,
    Matrix_Page,
    Overestimation,
    Overplacement]
