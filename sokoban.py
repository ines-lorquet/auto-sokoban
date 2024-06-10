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

screen.blit(background, (0, 0))
_grille.drawMap(screen)

_player = Player(_grille)
_player.drawPlayer(screen)

# Créer le bouton "Annuler"
undo_button = pygame.Rect(LARGEUR - 200, HAUTEUR - 50, 120, 30)
font = pygame.font.Font("Super Mario 64.TTF", 26)
button_text = font.render('BACK', True, (255, 255, 255))
button_color = (0, 128, 0)

# Créer le bouton "Solve"
solve_button = pygame.Rect(LARGEUR - 400, HAUTEUR - 50, 120, 30)
solve_text = font.render('SOLVE', True, (255, 255, 255))
solve_color = (0, 128, 128)

pygame.display.flip()

continuer = True
solution_path = []
solution_index = 0

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
                solution_path = []
                solution_index = 0
            if _grille.is_fini():
                current_level += 1
                if current_level < len(levels):
                    # Chargez le niveau suivant
                    _grille = Grille(levels[current_level])
                    screen.blit(background, (0, 0))
                    _grille.drawMap(screen)
                    _player = Player(_grille)
                    _player.drawPlayer(screen)
                else:
                    # Si tous les niveaux ont été complétés, quittez le jeu
                    continuer = False
        if event.type == MOUSEBUTTONDOWN:
            if undo_button.collidepoint(event.pos):
                _player.undo()
            if solve_button.collidepoint(event.pos):
                print("solve")
                solution_path = _grille.solve()  # Récupérer le chemin de la solution
                print(solution_path)  # Afficher le chemin parcouru (facultatif)
                solution_index = 0

    # Utiliser la solution pour faire bouger votre personnage
    if solution_path:
        if solution_index < len(solution_path):
            _player.move(solution_path[solution_index])
            solution_index += 1

    screen.blit(background, (0, 0))
    _grille.drawMap(screen)
    _player.drawPlayer(screen)

    # Dessiner le bouton "Annuler"
    pygame.draw.rect(screen, button_color, undo_button)
    screen.blit(button_text, (undo_button.x + 10, undo_button.y + 5))

    # Dessiner le bouton "Solve"
    pygame.draw.rect(screen, solve_color, solve_button)
    screen.blit(solve_text, (solve_button.x + 10, solve_button.y + 5))

    pygame.display.flip()

pygame.quit()
