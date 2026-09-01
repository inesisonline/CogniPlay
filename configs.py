import pygame

pygame.init()

class window:
    TITLE = "CogniPlay"
    WIDTH = 900
    HEIGHT = 506

class font:
    ROBOTO_MONO_REGULAR = 'fonts/RobotoMono-Regular.ttf'

class image:
    BACKGROUND = pygame.image.load('imgs/background_paper.jpeg')
    LOGO = pygame.image.load('imgs/cogniplay_logo.png')
    BACK_BUTTON = pygame.transform.scale(pygame.image.load('imgs/back_button.png'), (50, 50))

#class sound:
    #MAIN_THEME = None

class flower:
    SUNFLOWER = pygame.transform.scale(pygame.image.load('imgs/girasol.jpg'), (80, 80))
    SUNFLOWER2 = pygame.transform.scale(pygame.image.load('imgs/girasol 2.jpg'), (80, 80))
    DAISIES = pygame.transform.scale(pygame.image.load('imgs/margaridas.jpg'), (80, 80))
    DANDELION = pygame.transform.scale(pygame.image.load('imgs/dente de leao.jpg'), (80, 80))
    DANDELION2 = pygame.transform.scale(pygame.image.load('imgs/yellow flor.jpg'), (80, 80))
    POPPY = pygame.transform.scale(pygame.image.load('imgs/papoila.jpg'), (80, 80))
    CLOVER = pygame.transform.scale(pygame.image.load('imgs/trevo.jpg'), (80, 80))
    TULIP = pygame.transform.scale(pygame.image.load('imgs/tulipa.jpg'), (80, 80))
    CORNFLOWER = pygame.transform.scale(pygame.image.load('imgs/blue flor.jpg'), (80, 80))

class animal:
    DUCK = pygame.transform.scale(pygame.image.load('imgs/pato.png'), (50, 50))
    BIRD = pygame.transform.scale(pygame.image.load('imgs/passaro.png'), (50, 50))
    FISH = pygame.transform.scale(pygame.image.load('imgs/peixe.png'), (50, 50))
    FROG = pygame.transform.scale(pygame.image.load('imgs/sapo.png'), (50, 50))
    LIZARD = pygame.transform.scale(pygame.image.load('imgs/lagarto.png'), (50, 50))

class apple:
    APPLE = pygame.transform.scale(pygame.image.load('imgs/apple.png'), (200, 200))
    ROTTEN_APPLE = pygame.transform.scale(pygame.image.load('imgs/rotten apple.png'), (200, 200))