import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        # adicionamos ai_settings para que a espaconave tenha acesso as
        # configuracoes de velocidade.

        # inicializa a espaconave e define sua posicao inicial.
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings  # transformando o parametro ai_settings
        # para que possamos usa-lo em update(). (atributo de classe)

        # carrega a imagem da espaconave e obtem seu rectangulo
        self.image = pygame.image.load('image/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # inicia cada nova espaconave na parte inferior central da tela
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # armazena um valor decimal para o centro da espaconave
        self.center = float(self.rect.centerx)  # pq senao rect armazenara
        # a parte inteira desse valor. eis o motivo pelo qual armazenamos
        # o valor decimal na variavel self.center. (float)

        # flag de movimento para 'manter' a condicao de movimento ou parada
        # com o pressionamento das teclas.
        self.moving_right = False  # sem pressionamento de teclas = parada.
        self.moving_left = False

    def update(self):  # para atualizar a posicao do flag de movimento
        # atualiza a posicao da espaconave de acordo com a flag de movimento.
        # atualiza o valor do centro da espaconave, e nao o retangulo

        # esta linha converte 'moving_right' para True /
        # aqui tb limitamos o alcance da nave na tela para nao ultrapassar
        # os limites.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # atualiza o objeto rect de acordo com self.center
        self.rect.centerx = self.center

    def blitme(self):
        # desenha a espaconave em sua posicao atual
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # centraliza a espaconave na tela
        self.center = self.screen_rect.centerx
