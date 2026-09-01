import pygame
import configs
from configs import COLORS
import database
import random
from timer import Timer
from instructions import Instructions

APPLES = [
    configs.apple.APPLE,
    configs.apple.ROTTEN_APPLE
]

INSTRUCTIONS_TEXT = (
    "No ecrã vão surgir maçãs, uma de cada vez. "
    "Deverá pressionar a barra de ESPAÇO quando surgir uma maçã boa, "
    "e não fazer nada quando surgir uma maçã podre."
)

# create class for apple object
class Apple:
    def __init__(self, rect, apple):
        self.rect = rect
        self.apple = apple

    def draw(self, screen):
        pygame.draw.rect(screen, COLORS["black"], self.rect, configs.px(2), border_radius=configs.px(10))
        image_rect = self.apple.get_rect(center=self.rect.center)
        screen.blit(self.apple, image_rect)

# create class for Colheita Atenta game
class ColheitaAtenta:
    def __init__(self, screen, user_id):
        self.screen = screen
        self.user_id = user_id
        self.level = database.load_progress(self.user_id, "colheita_atenta")
        self.font = pygame.font.Font(configs.font.ROBOTO_MONO_REGULAR, configs.px(18))
        self.timer = Timer()
        self.back_button = pygame.Rect(configs.px(20), configs.px(20), configs.px(50), configs.px(50))

        self.current_fruit = random.choice(APPLES)
        self.good_apple = configs.apple.APPLE
        self.rotten_apple = configs.apple.ROTTEN_APPLE
        self.shown_at = pygame.time.get_ticks()
        self.user_response = False
        self.count = 0
        self.fruits_per_level = 30
        self.error_timer = 0
        self.correct_timer = 0
        self.action = None
        self.instructions = Instructions(INSTRUCTIONS_TEXT, self.font, self.timer)

    def new_fruit(self):
        self.current_fruit = random.choice(APPLES)
        self.user_response = False
        self.shown_at = pygame.time.get_ticks()
        self.count += 1
        self.error_timer = 0
        self.correct_timer = 0

    def apple_display_time(self):
        return max(1500 - (self.level - 1) * 50, 700)

    def update(self):
        if pygame.time.get_ticks() - self.shown_at >= self.apple_display_time():
            if self.count >= self.fruits_per_level:
                self.next_level()
            else:
                self.new_fruit()

    def handle_event(self, event):
        # back button
        if event.type == pygame.MOUSEBUTTONDOWN and self.back_button.collidepoint(event.pos):
            self.action = "onBack"
            return
        if self.instructions.handle_event(event):
            if not self.instructions.visible:
                self.shown_at = pygame.time.get_ticks()
            return
        # check for clicks on the apples
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.current_fruit == self.good_apple:
                    self.count += 1
                    self.correct_timer = pygame.time.get_ticks() + 500
                elif self.current_fruit == self.rotten_apple:
                    self.error_timer = pygame.time.get_ticks() + 500

    def draw(self):
        if self.instructions.visible:
            self.instructions.draw(self.screen)
            self.screen.blit(configs.image.BACK_BUTTON, self.back_button)
            return
        self.update()
        self.screen.fill(COLORS["white"])

        # timer
        elapsed = self.timer.time_elapsed()
        timer_text = self.font.render(f"{elapsed // 60:02}:{elapsed % 60:02}", True, COLORS["black"])
        self.screen.blit(timer_text, (configs.window.WIDTH // 2 - timer_text.get_width() // 2, configs.px(20)))

        # level
        level_text = self.font.render(f"Nível {self.level}", True, COLORS["black"])
        self.screen.blit(level_text, (configs.window.WIDTH - level_text.get_width() - configs.px(75), configs.px(20)))

        # apples
        image = self.current_fruit
        rect = image.get_rect(center=(configs.window.WIDTH // 2, configs.window.HEIGHT // 2))
        self.screen.blit(image, rect)

        # press space on rotten apple
        if pygame.time.get_ticks() < self.error_timer:
            pygame.draw.line(self.screen, COLORS["onError"], rect.topleft, rect.bottomright, configs.px(10))
            pygame.draw.line(self.screen, COLORS["onError"], rect.topright, rect.bottomleft, configs.px(10))

        if pygame.time.get_ticks() < self.correct_timer:
            start = (int(rect.left + rect.width * 0.18), int(rect.top + rect.height * 0.52))
            corner = (int(rect.left + rect.width * 0.42), int(rect.top + rect.height * 0.78))
            end = (int(rect.left + rect.width * 0.84), int(rect.top + rect.height * 0.22))
            pygame.draw.line(self.screen, COLORS["correct"], start, corner, configs.px(10))
            pygame.draw.line(self.screen, COLORS["correct"], corner, end, configs.px(10))
            pygame.draw.circle(self.screen, COLORS["correct"], corner, configs.px(5))

        # blit back button
        self.screen.blit(configs.image.BACK_BUTTON, self.back_button)

        self.instructions.draw_hint(self.screen)

    def next_level(self):
            self.level += 1
            self.save_progress()
            self.count = 0
            self.new_fruit()
    
    def save_progress(self):
        database.save_progress(self.user_id, "colheita_atenta", self.level)