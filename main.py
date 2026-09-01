# for testing purposes
# user: test
# password: test123

from configs import *
from start_screen import StartScreen
from login_screen import LogInScreen
from signup_screen import SignUpScreen
from selection_screen import SelectionScreen
from memoria_botanica import MemoriaBotanica
from encontre_pato import EncontrePato
from colheita_atenta import ColheitaAtenta

# window
screen = pygame.display.set_mode([window.WIDTH, window.HEIGHT], pygame.SCALED | pygame.RESIZABLE | pygame.FULLSCREEN)
pygame.display.set_caption(window.TITLE)
pygame.display.set_icon(pygame.image.load('imgs/brain_icon.png'))

exit_button = pygame.Rect(window.WIDTH - px(60), px(20), px(40), px(40))

def draw_exit_button(surface):
    pygame.draw.rect(surface, COLORS["white"], exit_button, border_radius=px(8))
    pygame.draw.rect(surface, COLORS["primary"], exit_button, px(2), border_radius=px(8))
    inset = px(12)
    pygame.draw.line(surface, COLORS["black"], (exit_button.left + inset, exit_button.top + inset),
                     (exit_button.right - inset, exit_button.bottom - inset), px(2))
    pygame.draw.line(surface, COLORS["black"], (exit_button.right - inset, exit_button.top + inset),
                     (exit_button.left + inset, exit_button.bottom - inset), px(2))

# clock
clock = pygame.time.Clock()

# start screen
current_screen = StartScreen(screen)

# Navigation graph
navigation_graph = []

# game loop
while True:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and exit_button.collidepoint(event.pos):
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            pygame.display.toggle_fullscreen()
            continue
        current_screen.handle_event(event)

    current_screen.draw()
    draw_exit_button(screen)

    previous_screen = current_screen

    if current_screen.action == "signup":
        current_screen = SignUpScreen(screen)
        navigation_graph.append(previous_screen)
    elif current_screen.action == "login":
        current_screen = LogInScreen(screen)
        navigation_graph.append(previous_screen)
    elif current_screen.action == "menu":
        current_screen = SelectionScreen(screen, current_screen.user_id)
        navigation_graph.append(previous_screen)
    elif current_screen.action == "memoriabotanica":
        current_screen = MemoriaBotanica(screen, current_screen.user_id)
        navigation_graph.append(previous_screen)
    elif current_screen.action == "encontrepato":
        current_screen = EncontrePato(screen, current_screen.user_id)
        navigation_graph.append(previous_screen)
    elif current_screen.action == "colheitaatenta":
        current_screen = ColheitaAtenta(screen, current_screen.user_id)
        navigation_graph.append(previous_screen)
    elif current_screen.action == "onBack":
        if navigation_graph:
            current_screen = navigation_graph.pop()
        current_screen.action = None

    pygame.display.update()