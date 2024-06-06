import pygame
import sys
from pygame.locals import *

from grille import Grille
from player import Player
from config import *

pygame.init()
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption(TITRE)

background = pygame.image.load("img/back.png")

# Liste des fichiers de niveaux
levels = ["lvl/lv1.txt", "lvl/lv2.txt", "lvl/lv3.txt", "lvl/lv4.txt", "lvl/lv5.txt"]
current_level = 0

_grille = Grille(levels[current_level])

screen.blit(background, (0,0))
_grille.drawMap(screen)

_player = Player(_grille)
_player.drawPlayer(screen)

pygame.display.flip()

continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            _player.move(event.key)
            if event.key == K_r:
                # Rechargez le même niveau
                _grille = Grille(levels[current_level])
                _grille.drawMap(screen)
                _player = Player(_grille)
                _player.drawPlayer(screen)
            if _grille.is_fini():
                current_level += 1
                if current_level < len(levels):
                    # Chargez le niveau suivant
                    _grille = Grille(levels[current_level])
                    screen.blit(background, (0,0))
                    _grille.drawMap(screen)
                    _player = Player(_grille)
                    _player.drawPlayer(screen)
                else:
                    # Si tous les niveaux ont été complétés, quittez le jeu
                    continuer = False
    screen.blit(background, (0,0))
    _grille.drawMap(screen)
    _player.drawPlayer(screen)
    pygame.display.flip()
