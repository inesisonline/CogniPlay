import pygame
import configs
import database
import MemoriaBotanica
import EncontrePato
import ColheitaAtenta

COLORS = {
    "white":  (255, 255, 255),
    "black":  (0, 0, 0),
    "primary": (255, 210, 15),
    "secondary": (0, 45, 240),
    "tertiary": (245, 60, 27)
}

# created class for the selection screen
# in this screen, the user can choose a game to play
class SelectionScreen:
    def __init__(self, screen, user_id):
        self.screen = screen
        self.user_id = user_id
        self.clock = pygame.time.Clock()
        self.logo = pygame.transform.scale(configs.image.LOGO, (100, 96))
        self.font = pygame.font.Font(configs.font.ROBOTO_MONO_REGULAR, 20)
        self.background = configs.image.BACKGROUND
        self.background_scale = pygame.transform.scale(self.background, (configs.window.WIDTH, int(self.background.get_height() * 
                                                                        configs.window.WIDTH / self.background.get_width())))
        self.background_scale.set_alpha(100)
        self.memoria_botanica_label = self.font.render("Memória\nBotânica", False, COLORS["black"])
        self.memoria_botanica_box = pygame.Rect(112, 200, 150, 150)
        self.encontre_pato_label = self.font.render("Encontre\no Pato", False, COLORS["black"])
        self.encontre_pato_box = pygame.Rect(374, 200, 150, 150)
        self.colheita_atenta_label = self.font.render("Colheita\nAtenta", False, COLORS["black"])
        self.colheita_atenta_box = pygame.Rect(636, 200, 150, 150)
        self.back_button = pygame.Rect(20, 20, 50, 50)
        self.action = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if self.back_button.collidepoint(mx, my):
                self.action = "onBack"
            elif self.memoria_botanica_box.collidepoint(mx, my):
                self.action = "memoriabotanica"
            elif self.encontre_pato_box.collidepoint(mx, my):
                self.action = "encontrepato"
            elif self.colheita_atenta_box.collidepoint(mx, my):
                self.action = "colheitaatenta"

    def draw(self):
        # white background
        self.screen.fill(COLORS["white"])

        # blit background
        self.screen.blit(self.background_scale, (0,0))

        # blit logo
        self.screen.blit(self.logo, (129, 50))

        # blit memória botânica box
        pygame.draw.rect(self.screen, COLORS["primary"], self.memoria_botanica_box, 2)

        # blit memória botânica label
        self.screen.blit(self.memoria_botanica_label, (122, 205))

        # blit encontre o pato box
        pygame.draw.rect(self.screen, COLORS["primary"], self.encontre_pato_box, 2)

        # blit encontre o pato label
        self.screen.blit(self.encontre_pato_label, (384, 205))

        # blit colheita atenta box
        pygame.draw.rect(self.screen, COLORS["primary"], self.colheita_atenta_box, 2)

        # blit colheita atenta label
        self.screen.blit(self.colheita_atenta_label, (646, 205))

        # blit back button
        self.screen.blit(configs.image.BACK_BUTTON, self.back_button)