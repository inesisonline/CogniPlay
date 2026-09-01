import pygame

class Timer:
    def __init__(self):
        self.start_ticks = pygame.time.get_ticks()
        self.paused = False
        self.paused_at = 0

    def reset(self):
        self.start_ticks = pygame.time.get_ticks()
        self.paused = False
        self.paused_at = 0

    def pause(self):
        # remember the moment we stopped, so the clock freezes
        if not self.paused:
            self.paused = True
            self.paused_at = pygame.time.get_ticks()

    def resume(self):
        # push the start forward by however long we were paused
        if self.paused:
            self.start_ticks += pygame.time.get_ticks() - self.paused_at
            self.paused = False

    def time_elapsed(self):
        # while paused, keep reading the frozen moment instead of "now"
        now = self.paused_at if self.paused else pygame.time.get_ticks()
        return (now - self.start_ticks) // 1000

    def draw_timer(self, screen, font):
        seconds = self.time_elapsed()
        text = font.render(f"Tempo: {seconds}s", True, (0, 0, 0))
        screen.blit(text, (400, 20))