

class Settings():
    '''uma classe para armazenar todas as configuracoes da Invasao Alienigena.'''

    def __init__(self):
        # inicializa as configuracoes do jogo
        # configuracoes da tela
        self.screen_width = 1200
        self.screen_heigth = 800
        self.bg_color = (230, 230, 230)

        # configuracao dos alienigenas
        self.alien_speed_factor = 1
        # deslocamento da frota para baixo e esquerda quando atingir a borda da tela
        self.fleet_drop_speed = 10  # velocidade de descida dos alienigenas
        # fleet_direction = a 1 representa a direita, -1 representa a esquerda.
        self.fleet_direction = 1

        # configuracao da espaconave
        self.ship_speed_factor = 1.5  # ajustando a velocidade da espaconave
        # ou seja, a velocidade com que a tela atualiza sua posicao.
        self.ship_limit = 3

        # configuracoes dos projeteis
        self.bullet_speed_factor = 3
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3  # limitando o disparo de 3 projeteis

        # taxa com q a velocidade do jogo aumenta
        self.speedup_scale = 1.1
        # taxa com que os pontos para cada alienigena aumentam
        self.score_scale = 1.5

        # para inicizlizar os valores do atributos que deve mudar no curso de um jogo
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # inicializa as configuracoes que mudam no decorrer do jogo
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        # pontuacao
        self.alien_points = 50

        # aumentando a velocidade da espaconave e dos alienigenas
    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
