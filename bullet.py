import pygame
from pygame.sprite import Sprite

# ao usar sprite podemos agrupar elementos relacionados no jogo e atuar em
# todos os elementos agrupados de uma so vez.


class Bullet(Sprite):
    # uma classe que administra projeteis disparados pela espaconave.

    def __init__(self, ai_settings, screen, ship):  # tera tudo isso como parametros
        # visto que todos elementos contem conexoes com a formacao dos projeteis
        # e sua localizacao
        super(Bullet, self).__init__()  # super para herdar de modo apropriado
        # de Sprite
        self.screen = screen  # atributo de classe

        # cria um retangulo para o projetil em (0,0) e, em seguida, define a
        # posicao correta

        # o projetil nao esta baseado numa imagem. eis o motivo pelo qual
        # precisamos criar um retangulo do zero usando a classe pygame.Rect()

        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        # informando a localizacao de onde partira o projetil e a posicao da
        # nave para o disparo sair do local correto.
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # armazena a posicao do projetil como um valor decimal.
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        # move o projetil para cima na tela.
        # atualiza a posicao decimal do projetil
        # (-) pq move-se para cima / decrescimo na coordenada Y.
        self.y -= self.speed_factor
        # atualiza a posicao de rect
        self.rect.y = self.y

    def draw_bullet(self):
        # desenha o projetil na tela.
        pygame.draw.rect(self.screen, self.color, self.rect)
