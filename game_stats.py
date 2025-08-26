class GameStats():
    # armazena dados estatisticos do jogo

    def __init__(self, ai_settings):
        # a pontuacao maxima jamais devera ser reiniciada
        self.high_score = 0
        # inicializa o jogo em um estado ativo
        self.game_active = True
        # inicializa os dados estatisticos
        self.ai_settings = ai_settings

        self.reset_stats()

        # inicia o jogo em um estado intaivo
        self.game_active = False

    def reset_stats(self):
        # inicializa os dados estatisticos que podem mudar durante o jogo
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
