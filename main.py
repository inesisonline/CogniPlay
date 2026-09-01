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
screen = pygame.display.set_mode([window.WIDTH, window.HEIGHT], pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption(window.TITLE)
pygame.display.set_icon(pygame.image.load('imgs/brain_icon.png'))

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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            pygame.display.toggle_fullscreen()
            continue
        current_screen.handle_event(event)

    current_screen.draw()

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