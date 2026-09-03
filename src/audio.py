import pygame


pygame.mixer.init()


def play_sound(path):
    sound = pygame.mixer.Sound(path)
    sound.play()