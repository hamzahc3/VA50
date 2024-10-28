import pygame
import heapq
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 30, 30  # Nombre de lignes et colonnes dans la grille
SQUARE_SIZE = WIDTH // COLS

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)

# Fenêtre Pygame
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entités avec Chemins")

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * SQUARE_SIZE
        self.y = col * SQUARE_SIZE
        self.color = WHITE
        self.neighbors = []
        self.cost = float("inf")  # Coût initial infini
        self.came_from = None

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE

    def make_barrier(self):
        self.color = BLACK

    def make_path(self):
        self.color = GREY

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = BLUE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_barrier():  # Bas
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # Haut
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < COLS - 1 and not grid[self.row][self.col + 1].is_barrier():  # Droite
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # Gauche
            self.neighbors.append(grid[self.row][self.col - 1])

# Fonction heuristique (utilisée par A*)
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Algorithme A*
def a_star_algorithm(grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    came_from = {}

    while not len(open_set) == 0:
        current = heapq.heappop(open_set)[2]

        if current == end:
            return reconstruct_path(came_from, current)

        open_set_hash.remove(current)

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = g_score[neighbor] + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

    return []

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


class Entite:
    def __init__(self, start_node, path_algorithm="A*", vie=100, esprit=50, vitesse=5):
        self.position = start_node
        self.vie = vie
        self.esprit = esprit
        self.vitesse = vitesse  # Plus la valeur est grande, plus l'entité est lente
        self.chemin = []
        self.path_algorithm = path_algorithm
        self.move_counter = 0  # Pour gérer la vitesse

    def set_path(self, path):
        self.chemin = path

    def update(self, grid, start, end):
        if self.path_algorithm == "A*":
            self.set_path(a_star_algorithm(grid, start, end))
        else:
            self.set_path(biased_path(grid, start, end))

    def move(self):
        self.move_counter += 1
        if self.move_counter % self.vitesse == 0 and len(self.chemin) > 0:
            self.position = self.chemin.pop(0)

    def draw(self, win):
        pygame.draw.circle(win, RED, (self.position.x + SQUARE_SIZE // 2, self.position.y + SQUARE_SIZE // 2), SQUARE_SIZE // 4)

# Création de la grille
def make_grid():
    grid = []
    for i in range(ROWS):
        grid.append([])
        for j in range(COLS):
            node = Node(i, j)
            grid[i].append(node)
    return grid

# Dessiner la grille
def draw_grid(win, grid, entities):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)

    for entite in entities:
        entite.draw(win)

    for i in range(ROWS):
        pygame.draw.line(win, GREY, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE))
        for j in range(COLS):
            pygame.draw.line(win, GREY, (j * SQUARE_SIZE, 0), (j * SQUARE_SIZE, HEIGHT))

    pygame.display.update()

# Fonction principale
def main():
    grid = make_grid()
    start = None  # Point de départ
    end = None  # Point d'arrivée
    entities = []

    running = True
    while running:
        draw_grid(win, grid, entities)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # Clic gauche pour sélectionner start, end ou barrière
                pos = pygame.mouse.get_pos()
                row, col = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != start and node != end:
                    node.make_barrier()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    # Créer des entités avec des algorithmes différents
                    for _ in range(50):
                        algorithm = random.choice(["A*", "biased"])
                        entite = Entite(start, path_algorithm=algorithm, vitesse=random.randint(2, 10))
                        entite.update(grid, start, end)
                        entities.append(entite)

        for entite in entities:
            entite.move()

    pygame.quit()

if __name__ == "__main__":
    main()
