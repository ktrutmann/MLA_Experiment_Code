from . import *
from otree.api import Bot
from otree.api import Submission


class PlayerBot(Bot):
    def play_round(self):
        yield (Introduction_1)
        yield (Introduction_2)
        yield (Introduction_3)
        yield (Introduction_4)
        yield (Start)
        yield Submission(Matrix_Page, {'cogn_rpm_matrix_1': 0, 'cogn_rpm_matrix_2': 0,
            'cogn_rpm_matrix_3': 0, 'cogn_rpm_matrix_4': 0,
            'cogn_rpm_matrix_5': 0, 'cogn_rpm_matrix_6': 0}, check_html=False)
        yield (Overestimation, {'pers_rpm_overestimation_answer': 4})
        yield (Overplacement, {'pers_rpm_overplacement_answer': 4})
