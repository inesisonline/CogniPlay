import pygame
import configs
from configs import COLORS
import database
import random
from timer import Timer
from instructions import Instructions

FLOWERS = [
    configs.flower.SUNFLOWER,
    configs.flower.SUNFLOWER2,
    configs.flower.DAISIES,
    configs.flower.DANDELION,
    configs.flower.DANDELION2,
    configs.flower.POPPY,
    configs.flower.CLOVER,
    configs.flower.TULIP,
    configs.flower.CORNFLOWER
]

INSTRUCTIONS_TEXT = (
    "No ecrã vão surgir alguns pares de cartas. "
    "Deverá clicar sobre as cartas uma de cada vez para as virar e fazer corresponder os pares."
)

# create class for card object
class Card:
    def __init__(self, rect, flower):
        self.rect = rect
        self.flower = flower
        self.face_up = False
        self.matched = False

    def flip(self):
        self.face_up = not self.face_up

    def is_clickable(self, pos):
        return self.rect.collidepoint(pos) and not self.face_up and not self.matched

    def matches(self, other):
        return self.flower == other.flower

    def draw(self, screen):
        if self.face_up or self.matched:
            pygame.draw.rect(screen, COLORS["white"], self.rect, border_radius=configs.px(10))
            pygame.draw.rect(screen, COLORS["black"], self.rect, configs.px(2), border_radius=configs.px(10))
            image_rect = self.flower.get_rect(center=self.rect.center)
            screen.blit(self.flower, image_rect)
        else:
            pygame.draw.rect(screen, COLORS["primary"], self.rect, border_radius=configs.px(10))

# create class for Memória Botânica game
class MemoriaBotanica:
    def __init__(self, screen, user_id):
        self.screen = screen
        self.user_id = user_id
        self.level = database.load_progress(self.user_id, "memoria_botanica")
        self.font = pygame.font.Font(configs.font.ROBOTO_MONO_REGULAR, configs.px(18))
        self.timer = Timer()
        self.back_button = pygame.Rect(configs.px(20), configs.px(20), configs.px(50), configs.px(50))

        self.positions = []
        self.first = None
        self.second = None
        self.flip_back = None
        self.cards_per_row = 3
        self.cards_per_column = 2
        self.card_width = configs.px(100)
        self.card_height = configs.px(100)
        self.TOP = configs.px(60)
        self.BOTTOM = configs.px(45)
        self.MARGIN = configs.px(20)
        self.cards = []
        self.action = None
        self.instructions = Instructions(INSTRUCTIONS_TEXT, self.font, self.timer)
        self.build_board()

    def pairs_for_level(self):
        return min(3 + (self.level - 1) // 3, 6)

    def create_card_positions(self):
        self.positions = []
        grid_width = self.cards_per_row * self.card_width + (self.cards_per_row - 1) * self.MARGIN
        grid_height = self.cards_per_column * self.card_height + (self.cards_per_column - 1) * self.MARGIN
        start_x = (configs.window.WIDTH - grid_width) // 2
        start_y = self.TOP + (configs.window.HEIGHT - self.TOP - self.BOTTOM - grid_height) // 2
        for i in range(self.cards_per_row):
            for j in range(self.cards_per_column):
                x = start_x + i * (self.card_width + self.MARGIN)
                y = start_y + j * (self.card_height + self.MARGIN)
                self.positions.append((x, y))
        return self.positions

    def build_board(self):
        pairs = self.pairs_for_level()
        self.cards_per_column = 2
        self.cards_per_row = pairs
        deck = random.sample(FLOWERS, pairs) * 2
        random.shuffle(deck)
        self.positions = self.create_card_positions()
        self.cards = [Card(pygame.Rect(x, y, self.card_width, self.card_height), flower)
                      for flower, (x, y) in zip(deck, self.positions)]
        
        self.first = None
        self.second = None
        self.flip_back = None

    def handle_event(self, event):
        # back button
        if event.type == pygame.MOUSEBUTTONDOWN and self.back_button.collidepoint(event.pos):
            self.action = "onBack"
            return
        if self.instructions.handle_event(event):
            return
        if self.flip_back is not None:
            return
        # check for clicks in each card
        if event.type == pygame.MOUSEBUTTONDOWN:
            for card in self.cards:
                if card.is_clickable(event.pos):
                    card.flip()
                    if self.first is None:
                        self.first = card
                    else:
                        self.second = card
                        if self.first.matches(self.second):
                            self.first.matched = True
                            self.second.matched = True
                            self.first = None
                            self.second = None
                            if all(card.matched for card in self.cards):
                                self.next_level()
                        else:
                            self.flip_back = pygame.time.get_ticks() + 800
                    break

    def update(self):
        # flips pairs back down
        if self.flip_back is not None and pygame.time.get_ticks() >= self.flip_back:
            self.first.flip()
            self.second.flip()
            self.first = None
            self.second = None
            self.flip_back = None

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

        # cards
        for card in self.cards:
            card.draw(self.screen)

        # blit back button
        self.screen.blit(configs.image.BACK_BUTTON, self.back_button)

        self.instructions.draw_hint(self.screen)

    def next_level(self):
        self.level += 1
        self.save_progress()
        self.build_board()

    def save_progress(self):
        database.save_progress(self.user_id, "memoria_botanica", self.level)