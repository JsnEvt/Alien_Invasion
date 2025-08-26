import pygame.font


class Button():

    def __init__(self, ai_settings, screen, msg):
        # inicializa os atributos do botao
        self.screen = screen
        self.screen_rect = screen.get_rect()

    # define as dimensoes e as propriedades do botao
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

    # constroi o objeto rect do botao e o centraliza
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

    # a mensagem do botao deve ser preparada apenas uma vez
        self.prep_msg(msg)

    def prep_msg(self, msg):
        # transforma msg em imagem renderizada e centraliza o texto no botao
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # desenha um botao em branco e, em seguida, desenha a mensagem
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
