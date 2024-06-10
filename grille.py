import pygame
from config import * 
from collections import deque
from pygame.locals import K_q, K_d, K_z, K_s  # Importer les constantes de touche

class Grille:
    def __init__(self, fichier):
        self.ref_img = {
            MUR: pygame.image.load("img/mur.jpg"),
            CAISSE: pygame.image.load("img/caisse.jpg"),
            OBJECTIF: pygame.image.load("img/objectif.png"),
            CAISSE_OK: pygame.image.load("img/caisse_ok.jpg"),
        }
        with open(fichier, 'r') as fich:
            self.lvtest = [[int(l) for l in line.strip().split(" ")] for line in fich]

        self.coord_objec = []
        for y in range(len(self.lvtest)):
            for x in range(len(self.lvtest[y])):
                if self.lvtest[y][x] == OBJECTIF:
                    self.coord_objec.append((x, y))

    def drawMap(self, screen):
        for y in range(len(self.lvtest)):
            for x in range(len(self.lvtest[y])):
                img = self.lvtest[y][x]
                if img in (VIDE, PLAYER):
                    x += 1
                else:
                    screen.blit(self.ref_img[img], (x * SIZE, y * SIZE))

    def getPlayerPosition(self):
        for y in range(len(self.lvtest)):
            for x in range(len(self.lvtest[y])):
                if self.lvtest[y][x] == PLAYER:
                    return (x * SIZE, y * SIZE)
        return (0, 0)

    def moveCaisse(self, x, y, pos):
        self.is_fini()
        if pos == "gauche":
            if self.lvtest[y][x - 2] not in (MUR, CAISSE, CAISSE_OK):
                if self.lvtest[y][x - 1] == CAISSE_OK:
                    self.lvtest[y][x - 1] = OBJECTIF
                else:
                    self.lvtest[y][x - 1] = VIDE
                if self.lvtest[y][x - 2] == OBJECTIF:
                    self.lvtest[y][x - 2] = CAISSE_OK
                    return True
                else:
                    self.lvtest[y][x - 2] = CAISSE
                    return True

        if pos == "droite":
            if self.lvtest[y][x + 2] not in (MUR, CAISSE, CAISSE_OK):
                if self.lvtest[y][x + 1] == CAISSE_OK:
                    self.lvtest[y][x + 1] = OBJECTIF
                else:
                    self.lvtest[y][x + 1] = VIDE
                if self.lvtest[y][x + 2] == OBJECTIF:
                    self.lvtest[y][x + 2] = CAISSE_OK
                    return True
                else:
                    self.lvtest[y][x + 2] = CAISSE
                    return True

        if pos == "haut":
            if self.lvtest[y - 2][x] not in (MUR, CAISSE, CAISSE_OK):
                if self.lvtest[y - 1][x] == CAISSE_OK:
                    self.lvtest[y - 1][x] = OBJECTIF
                else:
                    self.lvtest[y - 1][x] = VIDE
                if self.lvtest[y - 2][x] == OBJECTIF:
                    self.lvtest[y - 2][x] = CAISSE_OK
                    return True
                else:
                    self.lvtest[y - 2][x] = CAISSE
                    return True

        if pos == "bas":
            if self.lvtest[y + 2][x] not in (MUR, CAISSE, CAISSE_OK):
                if self.lvtest[y + 1][x] == CAISSE_OK:
                    self.lvtest[y + 1][x] = OBJECTIF
                else:
                    self.lvtest[y + 1][x] = VIDE
                if self.lvtest[y + 2][x] == OBJECTIF:
                    self.lvtest[y + 2][x] = CAISSE_OK
                    return True
                else:
                    self.lvtest[y + 2][x] = CAISSE
                    return True
        return False

    def is_fini(self):
        lis = [self.lvtest[y][x] for (x, y) in self.coord_objec]
        return lis.count(CAISSE_OK) == len(self.coord_objec)

    def solve(self):
        start = self.getPlayerPosition()
        start = (start[0] // SIZE, start[1] // SIZE)
        stack = [(start, [])]  # Utiliser une pile (list) pour DFS
        visited = set()  # Pour stocker les états visités

        directions = {
            'gauche': (-1, 0, K_q),
            'droite': (1, 0, K_d),
            'haut': (0, -1, K_z),
            'bas': (0, 1, K_s),
        }

        while stack:
            (x, y), path = stack.pop()  # Récupérer le dernier état de la pile pour DFS

            if self.is_fini():
                return path  # Si l'état actuel est une solution, retourner le chemin correspondant

            # Marquer l'état actuel comme visité
            visited.add((x, y))

            # Générer les nouveaux états à partir de l'état actuel
            for direction, (dx, dy, key) in directions.items():
                nx, ny = x + dx, y + dy
                if (0 <= nx < len(self.lvtest[0]) and 0 <= ny < len(self.lvtest) and
                        (nx, ny) not in visited and
                        self.lvtest[ny][nx] not in (MUR, CAISSE, CAISSE_OK)):
                    new_path = path + [key]  # Mettre à jour le chemin parcouru
                    stack.append(((nx, ny), new_path))  # Ajouter le nouvel état à la pile

                    # Marquer le nouvel état comme visité
                    visited.add((nx, ny))

        return []  # Si aucune solution n'a été trouvée

if __name__ == '__main__':
    g = Grille("lv1.txt")
    solution = g.solve()
    print("Solution:", solution)
