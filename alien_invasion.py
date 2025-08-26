import pygame

from settings import Settings

from ship import Ship

import game_functions as gf

from pygame.sprite import Group

from alien import Alien

from game_stats import GameStats

from scoreboard import Scoreboard

from button import Button


def run_game():
    # inicializa o jogo e cria um objeto para a tela
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_heigth))
    pygame.display.set_caption("Alien Invasion")

    # cria uma instanacia para armazenar dados estatisticos do jogo
    stats = GameStats(ai_settings)

    # criando o painel de pontuacao
    sb = Scoreboard(ai_settings, screen, stats)

    # cria o botao Play
    play_buttton = Button(ai_settings, screen, "Play")

    ship = Ship(ai_settings, screen)  # isso sao argumentos lancados na criacao
    # da instancia (o objeto)

    # cria um grupo no qual serao armazenados os projeteis
    bullets = Group()

    # cria uma alienigena
    alien = Alien(ai_settings, screen)

    # criando um grupo de alienigenas
    aliens = Group()

    # cria a frota de alienigenas
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # inicial o laco principal do jogo
    while True:

        # observa eventos do telado e do mouse
        gf.check_events(ai_settings, screen, stats, sb,
                        play_buttton, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats,
                              sb, ship, aliens, bullets)
        # redesenha a tela a cada passagem pelo laco
            gf.update_aliens(ai_settings, stats, screen,
                             sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship,
                         aliens, bullets, play_buttton)
        # deixa a tela mais recente visivel
        pygame.display.flip()


run_game()
