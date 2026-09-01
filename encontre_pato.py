import pygame
import configs
import database
import random
from timer import Timer
from instructions import Instructions

COLORS = {
    "white":  (255, 255, 255),
    "black":  (0, 0, 0),
    "primary": (255, 210, 15),
    "secondary": (0, 45, 240),
    "onError": (245, 60, 27)
}

ANIMALS = [
    configs.animal.DUCK,
    configs.animal.BIRD,
    configs.animal.FROG,
    configs.animal.FISH,
    configs.animal.LIZARD
]

INSTRUCTIONS_TEXT = (
    "No ecrã vão surgir alguns animais. "
    "Deverá encontrar e clicar sobre o pato."
)

# create class for animal object
class Animal:
    def __init__(self, rect, animal):
        self.rect = rect
        self.animal = animal

    def is_clickable(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, screen):
        image_rect = self.animal.get_rect(center = self.rect.center)
        screen.blit(self.animal, image_rect)

# create class for Encontre o Pato game
class EncontrePato:
    def __init__(self, screen, user_id):
        self.screen = screen
        self.user_id = user_id
        self.level = database.load_progress(self.user_id, "encontre_pato")
        self.font = pygame.font.Font(configs.font.ROBOTO_MONO_REGULAR, configs.px(18))
        self.timer = Timer()
        self.back_button = pygame.Rect(configs.px(20), configs.px(20), configs.px(50), configs.px(50))

        self.positions = []
        self.animals_per_row = 2
        self.animals_per_column = 2
        self.animal_width = configs.px(50)
        self.animal_height = configs.px(50)
        self.TOP = configs.px(70)
        self.BOTTOM = configs.px(45)
        self.MARGIN = configs.px(20)
        self.target = ANIMALS[0]
        self.wrong_animal = None
        self.wrong_timer = 0
        self.action = None
        self.instructions = Instructions(INSTRUCTIONS_TEXT, self.font, self.timer)
        self.build_board()

    def animals_for_level(self):
        return min(8 * (self.level + 1), 32)

    def create_animal_positions(self):
        self.positions = []
        grid_width = self.animals_per_row * self.animal_width + (self.animals_per_row - 1) * self.MARGIN
        grid_height = self.animals_per_column * self.animal_height + (self.animals_per_column - 1) * self.MARGIN
        start_x = (configs.window.WIDTH - grid_width) // 2
        start_y = self.TOP + (configs.window.HEIGHT - self.TOP - self.BOTTOM - grid_height) // 2
        for i in range(self.animals_per_row):
            for j in range(self.animals_per_column):
                x = start_x + i * (self.animal_width + self.MARGIN)
                y = start_y + j * (self.animal_height + self.MARGIN)
                self.positions.append((x, y))
        return self.positions

    def handle_event(self, event):
        # back button
        if event.type == pygame.MOUSEBUTTONDOWN and self.back_button.collidepoint(event.pos):
            self.action = "onBack"
            return
        if self.instructions.handle_event(event):
            return
        # check if user clicked on an animal
        if event.type == pygame.MOUSEBUTTONDOWN:
            for animal in self.animals:
                if animal.is_clickable(event.pos):
                    if animal.animal is self.target:
                        self.next_level()
                    else:
                        self.wrong_animal = animal.rect
                        self.wrong_timer = pygame.time.get_ticks() + 500
                    break

    def build_board(self):
        number_animals = self.animals_for_level()
        columns = 8
        self.animals_per_row = columns
        self.animals_per_column = (number_animals + columns - 1) // columns

        other_animals = []

        for animal in ANIMALS:
            if animal is not self.target:
                other_animals.append(animal)

        crowd = [self.target]
        for i in range(number_animals - 1):
            crowd.append(random.choice(other_animals))
        random.shuffle(crowd)

        self.positions = self.create_animal_positions()
        self.animals = [Animal(pygame.Rect(x, y, self.animal_width, self.animal_height), a)
                        for a, (x, y) in zip(crowd, self.positions)]

    def draw(self):
        if self.instructions.visible:
            self.instructions.draw(self.screen)
            self.screen.blit(configs.image.BACK_BUTTON, self.back_button)
            return

        self.screen.fill(COLORS["white"])

        elapsed = self.timer.time_elapsed()
        timer_text = self.font.render(f"{elapsed // 60:02}:{elapsed % 60:02}", True, COLORS["black"])
        self.screen.blit(timer_text, (configs.window.WIDTH // 2 - timer_text.get_width() // 2, configs.px(20)))

        # target image
        label = self.font.render("Encontre o", True, COLORS["black"])
        self.screen.blit(label, (configs.px(90), configs.px(30)))
        self.screen.blit(self.target, (configs.px(90) + label.get_width() + configs.px(10), configs.px(10)))
        
        # level
        level_text = self.font.render(f"Nível {self.level}", True, COLORS["black"])
        self.screen.blit(level_text, (configs.window.WIDTH - level_text.get_width() - configs.px(75), configs.px(20)))

        # animals
        for animal in self.animals:
            animal.draw(self.screen)

        # wrong animal
        if self.wrong_animal is not None and pygame.time.get_ticks() < self.wrong_timer:
            pygame.draw.line(self.screen, COLORS["onError"], self.wrong_animal.topleft, self.wrong_animal.bottomright, configs.px(5))
            pygame.draw.line(self.screen, COLORS["onError"], self.wrong_animal.topright, self.wrong_animal.bottomleft, configs.px(5))

        # blit back button
        self.screen.blit(configs.image.BACK_BUTTON, self.back_button)

        self.instructions.draw_hint(self.screen)

    def next_level(self):
        self.level += 1
        self.save_progress()
        self.build_board()

    def save_progress(self):
        database.save_progress(self.user_id, "encontre_pato", self.level)