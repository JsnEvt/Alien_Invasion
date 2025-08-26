import sys
from typing import AsyncIterable
from time import sleep

import pygame

from bullet import Bullet

from alien import Alien


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # responde a eventos de pressionamento das teclas do mouse.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets,  mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets,
                      mouse_x, mouse_y):
    # inicia um novo jogo quando o jogador clicar em Play
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reinicia as configuracoes do jogo
        ai_settings.initalize_dynamic_settings()

        # oculta o cursor do mouse
        pygame.mouse.set_visible(False)

        # reinicia os dados estatisticos do jogo
        stats.reset_stats()
        stats.game_active = True

        # reinicia as imagens do painel de pontuacao
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # esvazia a lista de alienigenas e de projeteis
        aliens.empty()
        bullets.empty()

        # cria uma nova frota e centraliza a espaconave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # atualiza as imagens na tela e alterna para a nova tela.
    # redesenha a tela a cada passagem pelo laco.
    # redesenha todos os projeteis atras da espaconave e dos alienigenas
    screen.fill(ai_settings.bg_color)
    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # desenha a informacao sobre a pontuacao
    sb.show_score()

    # desenha o botao play se o jogo estiver inativo
    if not stats.game_active:
        play_button.draw_button()

    # deixa a tela mais recente visivel
    pygame.display.flip()


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    # responde a pressionamento de teclas
    if event.key == pygame.K_RIGHT:
        # move a espaconave para a direita
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:  # ELSE IF (O CONTRARIO DO IF)
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        # cria um projetil e adiciona ao grupo de projeteis
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)
    elif event.key == pygame.k_q:
        sys.exit()


def check_keyup_events(event, ship):
    # responde a solturas de teclas
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


# para manter o arquivo principal do programa, alien_invasion, o mais simples
# possivel, passaremos o gerenciamento de projeteis para o arquivo game_functions

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # atualiza a posicao dos projenteis e se livra dos projeteis antigos.
    # atualiza as posicoes dos projeteis.
    # verifica se um projetil atingiu os alienigenas
    # caso afirmativo, livra-se do projetil e do alienigena

    bullets.update()

# livra-se dos projeteis que desapareceram
# livra-se dos projeteis que desapareceram para nao consumir memoria
# desnecessariamente
    for bullet in bullets.copy():
        # devido ao fato de nao poder remover itens de uma lista de um grupo
        # em um laco for, precisamos usar uma copia do grupo no laco.
        # o metodo copy permite modificar bullets no laco.
        # verifica-se se o projetil desapareceu e assim ele e removido de
        # bullets.
        if bullet.rect.bottom <= 0:  # quando a bala ultrapassar a parte
            # superior da tela
            bullets.remove(bullet)
    check_bullet_alien_collisions(
        ai_settings, screen, ship, stats, sb, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, stats, sb, aliens, bullets):
    # responde a colisioes entre projeteis e alienigenas
    # remove qualquer projetil e alienigena colidido.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        # poderao haver erros na contabilizacao dos alienigenas atingidos, portanto,
        # ajustaremos o codigo para evita-los.
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # se a frota toda for destruida, inicia um novo nivel
        # destroi os projeteis e cria uma nova frota e aumenta a velocidade do jogo
        ai_settings.increase_speed()
        bullets.empty()

        # aumenta o nivel
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def create_fleet(ai_settings, screen, ship, aliens):
    # cria uma frota completa de alienigenas
    # cria um alienigena e calcula o numero de alienigenas em uma linha
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height)

# cria a frota de alienigenas
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    # determina o numero de alienigenas que cabem em uma linha
    # cria uma frota completa de alienigenas
    # cria um alienigena e calcula o numero de alienigenas em uma linha
    # o espacamento entre os alienigenas e igula a largura de um alienigena

    avaliable_space_x = ai_settings.screen_width - \
        2 * alien_width  # espaco disponivel em x
    # numero de alien em x
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # cria um alienigena e o posiciona na linha
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_heigth):
    # determina o numero de linhas com alienigenas que cabem na tela
    avaliable_space_y = (ai_settings.screen_heigth - (3 * alien_heigth)
                         - ship_height)
    number_rows = int(avaliable_space_y / (2 * alien_heigth))
    return number_rows


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # atualiza a posicao de todos os alienigenas da frota
    # Verifica se a frota está em uma das bordas
    # e então atualiza as posições de todos os alienígenas da frota
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # verifica se houve colisoes entre alienigenas e a espaconave
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    # responde apropriadamente se algum alienigena alcancou uma borda
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    # faz toda frota descer e muda de direcao
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    # verifica se a frota esta em uma das bordas e entao atualiza as posicoes
    # de todos os alienigenas da frota
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    check_aliens_bottom(ai_settings, stats, sb,  screen, ship, aliens, bullets)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # responde ao fato da nave ter sido atingido por um alienigena
    if stats.ships_left > 0:
        # decrementa ship_left
        stats.ships_left -= 1
        # atualiza o painel de pontuacoes
        sb.prep_ships()

    # esvazia a lista de alienigenas e de projeteis
        aliens.empty()
        bullets.empty()

    # cria uma nova frota e centraliza a espaconave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

    # faz uma pausa
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    # verifica se algum alienigena alcancou a parte inferior da tela
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # trata esse caso do mesmo modo quando a nave e atingida
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

# para verificar se ha uma pontuacao maxima


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
