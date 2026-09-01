import pygame
import configs
import database

COLORS = {
    "white":  (255, 255, 255),
    "black":  (0, 0, 0),
    "primary": (255, 210, 15),
    "secondary": (0, 45, 240),
    "tertiary": (245, 60, 27)
}

# created class for sign up screen
class SignUpScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.logo = pygame.transform.scale(configs.image.LOGO, (100, 96))
        self.font = pygame.font.Font(configs.font.ROBOTO_MONO_REGULAR, 13)
        self.background = configs.image.BACKGROUND
        self.background_scale = pygame.transform.scale(self.background, (configs.window.WIDTH, int(self.background.get_height() * 
                                                                        configs.window.WIDTH / self.background.get_width())))
        self.background_scale.set_alpha(100)
        self.username_label = self.font.render("Nome de utilizador", False, COLORS["black"])
        self.username_box = pygame.Rect(129, 200, 350, 30)
        self.password_label = self.font.render("Palavra passe", False, COLORS["black"])
        self.password_box = pygame.Rect(129, 275, 350, 30)
        self.password_confirm_label = self.font.render("Confirme a palavra passe", False, COLORS["black"])
        self.password_confirm_box = pygame.Rect(129, 350, 350, 30)
        self.go_button = pygame.Rect(725, 325, 100, 50)
        self.go_label = self.font.render("Começar", True, COLORS["black"])
        self.back_button = pygame.Rect(20, 20, 50, 50)
        self.username = ""
        self.password = ""
        self.password_confirmation = ""
        self.active_box = None
        self.message = "" 
        self.action = None
        self.user_id = None

    def handle_event(self, event):
        # detect mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if self.back_button.collidepoint(mx, my):
                self.action = "onBack"
            elif self.username_box.collidepoint(mx, my):
                self.active_box = "user"
            elif self.password_box.collidepoint(mx, my):
                self.active_box = "pass"
            elif self.password_confirm_box.collidepoint(mx, my):
                self.active_box = "pass confirm"
            elif self.go_button.collidepoint(mx, my):
                self.submit()
            else:
                self.active_box = None
        elif event.type == pygame.KEYDOWN and self.active_box is not None:
            # delete previous letter
            if event.key == pygame.K_BACKSPACE:
                if self.active_box == "user":
                    self.username = self.username[:-1]
                elif self.active_box == "pass":
                    self.password = self.password [:-1]
                elif self.active_box == "pass confirm":
                    self.password_confirmation = self.password_confirmation[:-1]
            # enter letters
            elif event.key != pygame.K_RETURN:
                if self.active_box == "user":
                    self.username += event.unicode
                elif self.active_box == "pass":
                    self.password += event.unicode
                elif self.active_box == "pass confirm":
                    self.password_confirmation += event.unicode

    def draw(self):
        # white background
        self.screen.fill(COLORS["white"])

        # blit background
        self.screen.blit(self.background_scale, (0,0))

        # blit logo
        self.screen.blit(self.logo, (129, 50))

        # blit username label
        self.screen.blit(self.username_label, (129, 175))

        # blit username box
        pygame.draw.rect(self.screen, COLORS["black"], self.username_box, 2)

        # blit current username text
        username_surface = self.font.render(self.username, True, COLORS["black"])
        self.screen.blit(username_surface, (self.username_box.x + 5, self.username_box.y + 5))

        # blit password label
        self.screen.blit(self.password_label, (129, 250))

        # blit password box
        pygame.draw.rect(self.screen, COLORS["black"], self.password_box, 2)

        # blit current password text
        password_surface = self.font.render("*" * len(self.password), True, COLORS["black"])
        self.screen.blit(password_surface, (self.password_box.x + 5, self.password_box.y + 5))

        # blit confirm password label
        self.screen.blit(self.password_confirm_label, (129, 325))

        # blit confirm password box
        pygame.draw.rect(self.screen, COLORS["black"], self.password_confirm_box, 2)

        # blit current confirm password text
        password_confirmation_surface = self.font.render("*" * len(self.password_confirmation), True, COLORS["black"])
        self.screen.blit(password_confirmation_surface, (self.password_confirm_box.x + 5, self.password_confirm_box.y + 5))

        # blit go button
        pygame.draw.rect(self.screen, COLORS["primary"], self.go_button, border_radius=15)

        # blit label on the go button
        self.screen.blit(self.go_label, (self.go_button.centerx - self.go_label.get_width() // 2,
                                         self.go_button.centery - self.go_label.get_height() // 2))

        # blit message
        message_surface = self.font.render(self.message, True, COLORS["tertiary"], )
        self.screen.blit(message_surface, (129, 425))

        # blit back button
        self.screen.blit(configs.image.BACK_BUTTON, self.back_button)
                
    def submit(self):
        if self.username.strip() == "" or self.password == "":
            self.message = "Preencha todos os campos."
            return
        if self.password != self.password_confirmation:
            self.message = "As palavras-passe não coincidem."
            return
        if database.register_user(self.username, self.password):
            self.action = "login"
        else:
            self.message = "Esse utilizador já existe."