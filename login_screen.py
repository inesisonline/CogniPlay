import pygame
import configs
from configs import COLORS
import database

LOGO_BOTTOM = configs.px(146)
FORM_HEIGHT = configs.px(200)


# created class for log in screen
class LogInScreen():
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.logo = pygame.transform.smoothscale(configs.image.LOGO, (configs.px(100), configs.px(96)))
        self.font = pygame.font.Font(configs.font.ROBOTO_MONO_REGULAR, configs.px(13))
        self.background = configs.image.BACKGROUND
        self.background_scale = pygame.transform.smoothscale(self.background, (configs.window.WIDTH, int(self.background.get_height() * configs.window.WIDTH / self.background.get_width())))
        self.background_scale.set_alpha(100)
        self.form_top = LOGO_BOTTOM + (configs.window.HEIGHT - LOGO_BOTTOM - FORM_HEIGHT) // 2
        self.username_label = self.font.render("Nome de utilizador", False, COLORS["black"])
        self.username_box = pygame.Rect(configs.px(129), self.form_top + configs.px(25), configs.px(350), configs.px(30))
        self.password_label = self.font.render("Palavra passe", False, COLORS["black"])
        self.password_box = pygame.Rect(configs.px(129), self.form_top + configs.px(100), configs.px(350), configs.px(30))
        self.go_button = pygame.Rect(configs.px(725), self.form_top + configs.px(150), configs.px(100), configs.px(50))
        self.go_label = self.font.render("Entrar", True, COLORS["black"])
        self.back_button = pygame.Rect(configs.px(20), configs.px(20), configs.px(50), configs.px(50))
        self.username = ""
        self.password = ""
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
            # enter letters
            elif event.key != pygame.K_RETURN:
                if self.active_box == "user":
                    self.username += event.unicode
                elif self.active_box == "pass":
                    self.password += event.unicode

    def draw(self):
        # white background
        self.screen.fill(COLORS["white"])

        # blit background
        self.screen.blit(self.background_scale, (0,0))

        # blit logo
        self.screen.blit(self.logo, (configs.px(129), configs.px(50)))

        # blit username label
        self.screen.blit(self.username_label, (configs.px(129), self.form_top))

        # blit username box
        pygame.draw.rect(self.screen, COLORS["black"], self.username_box, configs.px(2))

        # blit current username text
        username_surface = self.font.render(self.username, True, COLORS["black"])
        self.screen.blit(username_surface, (self.username_box.x + configs.px(5), self.username_box.y + configs.px(5)))

        # blit password label
        self.screen.blit(self.password_label, (configs.px(129), self.form_top + configs.px(75)))

        # blit password box
        pygame.draw.rect(self.screen, COLORS["black"], self.password_box, configs.px(2))

        # blit current password text
        password_surface = self.font.render("*" * len(self.password), True, COLORS["black"])
        self.screen.blit(password_surface, (self.password_box.x + configs.px(5), self.password_box.y + configs.px(5)))

        # blit go button
        pygame.draw.rect(self.screen, COLORS["primary"], self.go_button, border_radius=configs.px(15))
        
        # centre the label on the go button
        self.screen.blit(self.go_label, (self.go_button.centerx - self.go_label.get_width() // 2,
                                         self.go_button.centery - self.go_label.get_height() // 2))

        message_surface = self.font.render(self.message, True, COLORS["onError"])
        self.screen.blit(message_surface, (configs.px(129), configs.window.HEIGHT - configs.px(60)))

        # blit back button
        self.screen.blit(configs.image.BACK_BUTTON, self.back_button)

    def submit(self):
        self.user_id = database.login_user(self.username, self.password)

        if self.user_id:
            self.action = "menu"
        else:
            self.message = "Nome de utilizador ou palavra-passe incorretos."