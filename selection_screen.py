import pygame
import configs

COLORS = {
    "white":  (255, 255, 255),
    "black":  (0, 0, 0),
    "primary": (255, 210, 15),
    "secondary": (0, 45, 240),
    "onError": (245, 60, 27),
    "grey": (110, 110, 110)
}

CARD_SIZE = configs.px(150)
CARD_LEFT = configs.px(112)
CARD_STEP = configs.px(262)
LOGO_BOTTOM = configs.px(146)
CARD_TOP = LOGO_BOTTOM + (configs.window.HEIGHT - LOGO_BOTTOM - CARD_SIZE) // 2

GAMES = [
    {
        "title": ("Memória", "Botânica"),
        "image": "imgs/girasol.jpg",
        "skill": "MEMÓRIA",
        "action": "memoriabotanica"
    },
    {
        "title": ("Encontre", "o Pato"),
        "image": "imgs/pato.png",
        "skill": "ATENÇÃO",
        "action": "encontrepato"
    },
    {
        "title": ("Colheita", "Atenta"),
        "image": "imgs/apple.png",
        "skill": "AUTOCONTROLO",
        "action": "colheitaatenta"
    }
]

class SelectionScreen:
    def __init__(self, screen, user_id):
        self.screen = screen
        self.user_id = user_id
        self.logo = pygame.transform.smoothscale(configs.image.LOGO, (configs.px(100), configs.px(96)))
        self.background = configs.image.BACKGROUND
        self.background_scale = pygame.transform.scale(self.background, (configs.window.WIDTH, int(self.background.get_height() *
                                                                        configs.window.WIDTH / self.background.get_width())))
        self.background_scale.set_alpha(100)
        self.back_button = pygame.Rect(configs.px(20), configs.px(20), configs.px(50), configs.px(50))
        self.action = None

        self.padding = int(CARD_SIZE * 0.07)
        self.icon_size = int(CARD_SIZE * 0.44)
        self.radius = int(CARD_SIZE * 0.08)
        self.title_font = pygame.font.Font(configs.font.ROBOTO_MONO_REGULAR, int(CARD_SIZE * 0.087))
        self.skill_font = pygame.font.Font(configs.font.ROBOTO_MONO_REGULAR, int(CARD_SIZE * 0.075))

        self.cards = []
        for i, game in enumerate(GAMES):
            icon = pygame.image.load(game["image"]).convert_alpha()
            self.cards.append({
                "box": pygame.Rect(CARD_LEFT + i * CARD_STEP, CARD_TOP, CARD_SIZE, CARD_SIZE),
                "icon": pygame.transform.smoothscale(icon, (self.icon_size, self.icon_size)),
                "title": game["title"],
                "skill": game["skill"],
                "action": game["action"]
            })

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self.action = "onBack"
                return
            for card in self.cards:
                if card["box"].collidepoint(event.pos):
                    self.action = card["action"]
                    return

    def draw(self):
        self.screen.fill(COLORS["white"])
        self.screen.blit(self.background_scale, (0, 0))
        self.screen.blit(self.logo, (configs.px(129), configs.px(50)))

        for card in self.cards:
            box = card["box"]
            pygame.draw.rect(self.screen, COLORS["white"], box, border_radius=self.radius)
            pygame.draw.rect(self.screen, COLORS["primary"], box, 2, border_radius=self.radius)

            self.screen.blit(card["icon"], card["icon"].get_rect(center=(box.centerx, box.y + self.padding + self.icon_size // 2)))

            y = box.y + self.padding + self.icon_size + int(CARD_SIZE * 0.027)
            for line in card["title"]:
                text = self.title_font.render(line, True, COLORS["black"])
                self.screen.blit(text, (box.centerx - text.get_width() // 2, y))
                y += self.title_font.get_height()

            y += int(CARD_SIZE * 0.025)
            pygame.draw.line(self.screen, COLORS["primary"], (box.x + self.padding * 2, y), (box.right - self.padding * 2, y), 1)
            y += int(CARD_SIZE * 0.035)

            text = self.skill_font.render(card["skill"], True, COLORS["grey"])
            self.screen.blit(text, (box.centerx - text.get_width() // 2, y))

        self.screen.blit(configs.image.BACK_BUTTON, self.back_button)
