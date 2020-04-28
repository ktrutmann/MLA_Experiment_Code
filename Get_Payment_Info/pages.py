from ._builtin import Page


class payment_info_page(Page):
    form_model = 'player'
    form_fields = ['matr_nr']


page_sequence = [
    payment_info_page,
]
