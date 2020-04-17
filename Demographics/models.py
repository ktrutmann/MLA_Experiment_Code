from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Kevin Trutmann'

doc = """
Demographics questionnaire"""


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
    strategy_random = models.IntegerField(choices=[i+1 for i in range(7)], widget=widgets.RadioSelectHorizontal(),
                                          label='Ich habe die Aktie per Zufallsprinzip gekauft und verkauft.')
    strategy_feeling = models.IntegerField(choices=[i+1 for i in range(7)], widget=widgets.RadioSelectHorizontal(),
                                           label='Ich vertraute meinem Bauchgefühl über die Preisentwicklung.')
    strategy_rational = models.IntegerField(choices=[i+1 for i in range(7)], widget=widgets.RadioSelectHorizontal(),
                                            label='Ich investierte, wenn ich der Überzeugung war, dass es '
                                                  'wahrscheinlicher als 50% ist, dass der Preis ansteigen wird.')
    strategy_short_rational = models.IntegerField(choices=[i+1 for i in range(7)],
                                                  widget=widgets.RadioSelectHorizontal(),
                                                  label='Ich tätigte einen Blankoverkauf, wenn ich der Überzeugung war,'
                                                        'dass es wahrscheinlicher als 50% ist, dass der Preis fallen'
                                                        'wird.')
    strategy_risk_averse = models.IntegerField(choices=[i+1 for i in range(7)], widget=widgets.RadioSelectHorizontal(),
                                               label='Ich investierte nur, wenn ich sehr sicher war, dass der Preis '
                                                     'ansteigen wird.')
    strategy_short_risk_averse = models.IntegerField(choices=[i+1 for i in range(7)], widget=widgets.RadioSelectHorizontal(),
                                               label='Ich tätigte nur dann einen Blankoverkauf,'
                                                     'wenn ich sehr sicher war, dass der Preis fallen wird.')
    strategy_inertia = models.IntegerField(choices=[i+1 for i in range(7)], widget=widgets.RadioSelectHorizontal(),
                                           label='Ich versuchte die Aktie jeweils möglichst lange zu halten/'
                                                 'nicht zurück zu kaufen.')
    strategy_DE = models.IntegerField(choices=[i+1 for i in range(7)], widget=widgets.RadioSelectHorizontal(),
                                      label='Ich versuchte die Aktie möglichst nur zu verkaufen/zurückzukaufen,'
                                            'wenn ich damit Gewinn gemacht habe.')
    strategy_anti_DE = models.IntegerField(choices=[i+1 for i in range(7)], widget=widgets.RadioSelectHorizontal(),
                                           label='Ich versuchte, wenn ich einen Verlust gemacht habe, die Aktie'
                                                 ' möglichst schnell wieder zu verkaufen/zurückzukaufen.')



    age = models.IntegerField(min=10, max=100)
    gender = models.StringField(choices=['Männlich', 'Weiblich', 'Andere', 'Keine Angaben'],
                                widget=widgets.RadioSelect())
    is_student = models.StringField(choices=['Ja', 'Nein'], widget=widgets.RadioSelectHorizontal())
    study_field = models.StringField(blank=True)
    investment_experience = models.IntegerField(label='Auf einer Skala von 0-5, wie viel Erfahrung haben Sie mit '
                                                      'Investitionstätigkeiten (Geldanlage, Aktienhandel ect...)?'
                                                      ' (0 = Keine Erfahrung, 5 = Professionelle(r) Anleger(in))',
                                                choices=list(range(6)), widget=widgets.RadioSelectHorizontal())
    purpose = models.LongStringField(blank=True, label='')
    engagement = models.IntegerField(label='Auf einer Skala von 1-7, wie Aufmerksam waren Sie wärend der Studie?',
                                     choices=[i+1 for i in range(7)], widget=widgets.RadioSelectHorizontal())
    interest = models.IntegerField(label='Auf einer Skala von 1-7, wie spannend fanden Sie die Aufgaben?',
                                   choices=[i+1 for i in range(7)], widget=widgets.RadioSelectHorizontal())
    general_comments = models.LongStringField(blank=True, label='')
