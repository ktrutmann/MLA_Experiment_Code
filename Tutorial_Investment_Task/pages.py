from ._builtin import Page
from .models import Constants
from Investment_Task.pages import condition_page, trading_page, belief_page, update_page


class initializer_page(Page):
    def before_next_page(self):
        self.player.initialize_round(n_distinct_paths=Constants.num_training_blocks_per_condition)


class tutorial_page(Page):
    form_model = 'player'
    form_fields = ['transaction']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return self.player.get_tutorial_vars()


class end_page(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [initializer_page,
                 tutorial_page,
                 condition_page,
                 trading_page,
                 belief_page,
                 update_page,
                 end_page]
