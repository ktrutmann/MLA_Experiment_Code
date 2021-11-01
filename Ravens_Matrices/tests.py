from . import pages
from ._builtin import Bot


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.Introduction_1)
        yield (pages.Introduction_2)
        yield (pages.Introduction_3)
        yield (pages.Introduction_4)
        yield (pages.Start)
        yield (pages.Matrix_1, {'cogn_rpm_matrix_1': 0})
        yield (pages.Matrix_2, {'cogn_rpm_matrix_2': 0})
        yield (pages.Matrix_3, {'cogn_rpm_matrix_3': 0})
        yield (pages.Matrix_4, {'cogn_rpm_matrix_4': 0})
        yield (pages.Overestimation, {'pers_rpm_overestimation_answer': 4})
        yield (pages.Overplacement, {'pers_rpm_overplacement_answer': 4})
