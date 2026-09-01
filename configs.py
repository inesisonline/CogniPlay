import pygame

pygame.init()

SCALE = 1.6

def px(value):
    return int(value * SCALE)

COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "primary": (255, 210, 15),
    "secondary": (0, 45, 240),
    "onError": (245, 60, 27),
    "correct": (40, 160, 70),
    "grey": (110, 110, 110)
}

class window:
    TITLE = "CogniPlay"
    WIDTH = px(900)
    HEIGHT = WIDTH * 9 // 16

class font:
    ROBOTO_MONO_REGULAR = 'fonts/RobotoMono-Regular.ttf'

class image:
    BACKGROUND = pygame.image.load('imgs/background_paper.jpeg')
    LOGO = pygame.image.load('imgs/cogniplay_logo.png')
    BACK_BUTTON = pygame.transform.smoothscale(pygame.image.load('imgs/back_button.png'), (px(50), px(50)))

#class sound:
    #MAIN_THEME = None

class flower:
    SUNFLOWER = pygame.transform.smoothscale(pygame.image.load('imgs/girasol.jpg'), (px(80), px(80)))
    SUNFLOWER2 = pygame.transform.smoothscale(pygame.image.load('imgs/girasol 2.jpg'), (px(80), px(80)))
    DAISIES = pygame.transform.smoothscale(pygame.image.load('imgs/margaridas.jpg'), (px(80), px(80)))
    DANDELION = pygame.transform.smoothscale(pygame.image.load('imgs/dente de leao.jpg'), (px(80), px(80)))
    DANDELION2 = pygame.transform.smoothscale(pygame.image.load('imgs/yellow flor.jpg'), (px(80), px(80)))
    POPPY = pygame.transform.smoothscale(pygame.image.load('imgs/papoila.jpg'), (px(80), px(80)))
    CLOVER = pygame.transform.smoothscale(pygame.image.load('imgs/trevo.jpg'), (px(80), px(80)))
    TULIP = pygame.transform.smoothscale(pygame.image.load('imgs/tulipa.jpg'), (px(80), px(80)))
    CORNFLOWER = pygame.transform.smoothscale(pygame.image.load('imgs/blue flor.jpg'), (px(80), px(80)))

class animal:
    DUCK = pygame.transform.smoothscale(pygame.image.load('imgs/pato.png'), (px(50), px(50)))
    BIRD = pygame.transform.smoothscale(pygame.image.load('imgs/passaro.png'), (px(50), px(50)))
    FISH = pygame.transform.smoothscale(pygame.image.load('imgs/peixe.png'), (px(50), px(50)))
    FROG = pygame.transform.smoothscale(pygame.image.load('imgs/sapo.png'), (px(50), px(50)))
    LIZARD = pygame.transform.smoothscale(pygame.image.load('imgs/lagarto.png'), (px(50), px(50)))

class apple:
    APPLE = pygame.transform.smoothscale(pygame.image.load('imgs/apple.png'), (px(200), px(200)))
    ROTTEN_APPLE = pygame.transform.smoothscale(pygame.image.load('imgs/rotten apple.png'), (px(200), px(200)))