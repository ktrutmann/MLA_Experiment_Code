from otree.api import *
import time

author = 'Adrian Leuenberger / Kevin Trutmann'

doc = """
Raven’s Progressive Matrices (RPM)
Civalli, A. & Deck, S. (2017). A Flexible and Customizable Method for Assessing Cognitive Abilities:
https://digitalcommons.chapman.edu/cgi/viewcontent.cgi?article=1220&context=esi_working_papers
"""
# TODO: (2) Add extra matrices!
# TODO: (3) Translate Instructions!

class Constants(BaseConstants):
    name_in_url = 'RPM'
    players_per_group = None
    num_rounds = 1
    endowment = 10  # TODO: (2) How much to give?


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass



def scale_1(label):
    return models.IntegerField(
        choices=[
            [0, 'A'],
            [1, 'B'],
            [0, 'C'],
            [0, 'D'],
            [0, 'E'],
            [0, 'F'],
        ],
        label=label,
        widget=widgets.RadioSelectHorizontal,
    )

def scale_2(label):
    return models.IntegerField(
        choices=[
            [0, 'A'],
            [0, 'B'],
            [0, 'C'],
            [0, 'D'],
            [1, 'E'],
            [0, 'F'],
        ],
        label=label,
        widget=widgets.RadioSelectHorizontal,
    )

def scale_3(label):
    return models.IntegerField(
        choices=[
            [1, 'A'],
            [0, 'B'],
            [0, 'C'],
            [0, 'D'],
            [0, 'E'],
            [0, 'F'],
        ],
        label=label,
        widget=widgets.RadioSelectHorizontal,
    )


def scale_4(label):
    return models.IntegerField(
        choices=[
            [1, 'A'],
            [0, 'B'],
            [0, 'C'],
            [0, 'D'],
            [0, 'E'],
            [0, 'F'],
        ],
        label=label,
        widget=widgets.RadioSelectHorizontal,
    )

class Player(BasePlayer):
    cogn_rpm_matrix_1 = scale_1('Wählen Sie das Element, welches das Bild oben sinnvoll ergänzt:')
    cogn_rpm_matrix_2 = scale_2('Wählen Sie das Element, welches das Bild oben sinnvoll ergänzt:')
    cogn_rpm_matrix_3 = scale_3('Wählen Sie das Element, welches das Bild oben sinnvoll ergänzt:')
    cogn_rpm_matrix_4 = scale_4('Wählen Sie das Element, welches das Bild oben sinnvoll ergänzt:')
    cogn_rpm_total_points = models.IntegerField(initial=None)
    pers_rpm_overestimation_answer = models.IntegerField(label='Anzahl:', min=0, max=4)
    pers_rpm_overestimation_score = models.IntegerField()
    pers_rpm_overplacement_answer = models.IntegerField(label='Rang:', min=1, max=100)

def get_timeout_seconds(player: Player):
    return player.participant.vars['expiry'] - time.time()

def is_displayed(player: Player): # TODO: (2) What is happening here?
    return player.participant.vars['expiry'] - time.time() > 0

def add_earnings_to_payoff(player: Player):
    # Calculate the points:
    player.cogn_rpm_total_points = player.cogn_rpm_matrix_1 + player.cogn_rpm_matrix_2 +\
                                        player.cogn_rpm_matrix_3 + player.cogn_rpm_matrix_4
    player.payoff = c(player.cogn_rpm_total_points * Constants.endowment)
    player.participant.vars['payoff_dict']['ravens_bonus'] = player.payoff

    # Update the total payoff
    player.participant.vars['payoff_dict']['payoff_total'] = player.participant.payoff_plus_participation_fee()


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
    def is_displayed(player: Player):
        return player.round_number == 1 

    def before_next_page(player: Player, timeout_happened):
        # user has 3 minutes to complete as many pages as possible
        player.participant.vars['expiry'] = time.time() + 3*60


class Matrix_1(Page):
    form_model = 'player'
    form_fields = ['cogn_rpm_matrix_1']
    timer_text = 'Verbleibende Zeit für die Matrizenaufgaben:'
    def get_timeout_seconds(player: Player):
        return get_timeout_seconds(player)

    def is_displayed(player: Player):
        return player.round_number == 1 



class Matrix_2(Page):
    form_model = 'player'
    form_fields = ['cogn_rpm_matrix_2']
    timer_text = 'Verbleibende Zeit für die Matrizenaufgaben:'
    def get_timeout_seconds(player: Player):
        return get_timeout_seconds(player)

    def is_displayed(player: Player):
        return player.round_number == 1 

    def before_next_page(player: Player, timeout_happened, self): # TODO: (2) Test whether the back button still works! -> It does not
        if self.request.POST.get('Zurück'):
            if self.request.POST.get('Zurück')[0] == '1':
                self._is_frozen = False
                self._index_in_pages -= 2
                self.participant._index_in_pages -= 2


class Matrix_3(Page):
    form_model = 'player'
    form_fields = ['cogn_rpm_matrix_3']
    timer_text = 'Verbleibende Zeit für die Matrizenaufgaben:'
    def get_timeout_seconds(player: Player):
        return player.get_timeout_seconds()

    def is_displayed(player: Player):
        return player.round_number == 1 

    def before_next_page(player: Player, timeout_happened):
        if player.request.POST.get('Zurück'):
            if player.request.POST.get('Zurück')[0] == '1':
                player._is_frozen = False
                player._index_in_pages -= 2
                player.participant._index_in_pages -= 2
  

class Matrix_4(Page):
    form_model = 'player'
    form_fields = ['cogn_rpm_matrix_4']
    timer_text = 'Verbleibende Zeit für die Matrizenaufgaben:'
    def get_timeout_seconds(player: Player):
        return player.get_timeout_seconds()

    def is_displayed(player: Player):
        return player.round_number == 1 

    def before_next_page(player: Player, timeout_happened):
        player.add_earnings_to_payoff()

        if player.request.POST.get('Zurück'):
            if player.request.POST.get('Zurück')[0] == '1':
                player._is_frozen = False
                player._index_in_pages -= 2
                player.participant._index_in_pages -= 2


class Overestimation(Page):
    form_model = 'player'
    form_fields = ['pers_rpm_overestimation_answer']


class Overplacement(Page):
    form_model = 'player'
    form_fields = ['pers_rpm_overplacement_answer']


page_sequence = [
    # Introduction_1, # TODO: (3) Uncomment!
    # Introduction_2,
    # Introduction_3,
    # Introduction_4,
    Start,
    Matrix_1,
    Matrix_2,
    Matrix_3,
    Matrix_4,
    Overestimation,
    Overplacement]
