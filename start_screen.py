import pygame
import configs
from configs import COLORS
from instructions import wrap_text

# renamed to "primary" "secondary" etc
# welcome text to introduce the app to the user
welcome_text = ("O CogniPlay é um programa de estimulação cognitiva que, "
                "através de pequenos jogos, o ajuda a treinar e fortalecer a mente. "
                "De forma simples e divertida, cada jogo foi pensado para exercitar "
                "diferentes funções cognitivas, à medida que a dificuldade aumenta e "
                "acompanha a sua evolução. Ao jogar, estará a trabalhar três principais "
                "funções cognitivas: "
                "a Memória - a capacidade de reter e recordar informação - "
                "a Atenção - a capacidade de se concentrar e detetar o que é relevante, mesmo quando surgem distrações - "
                "e as Funções executivas - a capacidade de planear, controlar o comportamento e responder no momento certo. "
                "Escolha um jogo, pressione a tecla I para ver instruções e comece a treinar a sua mente!")

# create class for the start screen
class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.logo = pygame.transform.smoothscale(configs.image.LOGO, (configs.px(269), configs.px(258)))
        self.scroll_y = 0
        self.font = pygame.font.Font(configs.font.ROBOTO_MONO_REGULAR, configs.px(18))
        self.line_height = self.font.get_height() + configs.px(4)
        self.margin = configs.px(70)
        self.text_x = configs.px(129)
        self.text_lines_config = wrap_text(welcome_text, self.font, configs.window.WIDTH - self.text_x - self.margin)
        self.background = configs.image.BACKGROUND
        self.background_scale = pygame.transform.smoothscale(self.background, (configs.window.WIDTH, int(self.background.get_height() * 
                                                                        configs.window.WIDTH / self.background.get_width())))
        self.background_scale.set_alpha(100)
        self.logo_top = configs.px(100)
        self.logo_bottom = self.logo_top + self.logo.get_height()
        self.text_top = self.logo_bottom + configs.px(30)
        self.text_bottom = self.text_top + len(self.text_lines_config) * self.line_height
        self.button_y = self.text_bottom + configs.px(50)
        self.signup_label = self.font.render("Registar-se", True, COLORS["black"])
        self.login_label = self.font.render("Iniciar sessão", True, COLORS["black"])
        pad = configs.px(30)
        gap = configs.px(40)
        signup_width = self.signup_label.get_width() + pad * 2
        login_width = self.login_label.get_width() + pad * 2
        start_x = (configs.window.WIDTH - (signup_width + gap + login_width)) // 2
        self.signup_button = pygame.Rect(start_x, self.button_y, signup_width, configs.px(50))
        self.login_button = pygame.Rect(start_x + signup_width + gap, self.button_y, login_width, configs.px(50))
        self.page_height = self.button_y + configs.px(50) + configs.px(40)
        self.max_scroll = max(0, self.page_height - configs.window.HEIGHT)
        self.action = None

    def handle_event(self, event):
        # detect mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            my += self.scroll_y
            if self.signup_button.collidepoint(mx, my):
                self.action = "signup"
            elif self.login_button.collidepoint(mx, my):
                self.action = "login"
        # detect mouse scroll
        elif event.type == pygame.MOUSEWHEEL:
            self.scroll_y -= event.y * configs.px(40)
            self.scroll_y = max(0, min(self.scroll_y, self.max_scroll))

    def draw(self):
        # white background
        self.screen.fill(COLORS["white"])

        # blit background
        self.screen.blit(self.background_scale, (0,0))

        # blit logo
        self.screen.blit(self.logo, (configs.px(129), self.logo_top - self.scroll_y))

        # blit log in and sign up buttons
        signup_rect = self.signup_button.move(0, -self.scroll_y)
        login_rect = self.login_button.move(0, -self.scroll_y)
        pygame.draw.rect(self.screen, COLORS["primary"], signup_rect, border_radius=configs.px(15))
        pygame.draw.rect(self.screen, COLORS["primary"], login_rect, border_radius=configs.px(15))

        # centre the labels
        self.screen.blit(self.signup_label, (signup_rect.centerx - self.signup_label.get_width() // 2,
                                             signup_rect.centery - self.signup_label.get_height() // 2))
        self.screen.blit(self.login_label, (login_rect.centerx - self.login_label.get_width() // 2,
                                            login_rect.centery - self.login_label.get_height() // 2))

        # blit welcome text
        x = self.text_x
        top = self.text_top
        for i, line in enumerate(self.text_lines_config):
            surface = self.font.render(line, True, COLORS["black"])
            self.screen.blit(surface, (x, top + i * self.line_height - self.scroll_y))