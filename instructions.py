import pygame
import configs

COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "primary": (255, 210, 15),
    "grey": (110, 110, 110)
}

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current = ""

    for word in words:
        test = word if current == "" else current + " " + word
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

class Instructions:
    def __init__(self, text, font, timer=None):
        self.font = font
        self.timer = timer
        self.lines = wrap_text(text, font, configs.window.WIDTH - configs.px(200))
        self.hint_font = pygame.font.Font(configs.font.ROBOTO_MONO_REGULAR, configs.px(13))
        self.visible = True
        self.already_played = False

        if self.timer is not None:
            self.timer.pause()

    def open(self):
        self.visible = True
        if self.timer is not None:
            self.timer.pause()

    def close(self):
        self.visible = False
        self.already_played = True
        if self.timer is not None:
            self.timer.resume()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
            if self.visible:
                self.close()
            else:
                self.open()
            return True

        return self.visible

    def draw(self, screen):
        screen.fill(COLORS["white"])

        line_height = self.font.get_height() + configs.px(8)
        y = (configs.window.HEIGHT - len(self.lines) * line_height) // 2
        for line in self.lines:
            text = self.font.render(line, True, COLORS["black"])
            screen.blit(text, (configs.window.WIDTH // 2 - text.get_width() // 2, y))
            y += line_height

        if self.already_played:
            message = "Pressione I para continuar"
        else:
            message = "Pressione I para começar"

        hint = self.font.render(message, True, COLORS["primary"])
        screen.blit(hint, (configs.window.WIDTH // 2 - hint.get_width() // 2, configs.window.HEIGHT - configs.px(60)))

    def draw_hint(self, screen):
        hint = self.hint_font.render("I = instruções", True, COLORS["grey"])
        screen.blit(hint, (configs.window.WIDTH // 2 - hint.get_width() // 2, configs.window.HEIGHT - configs.px(28)))
