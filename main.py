import pygame
from pathAlgos import a_star
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 840, 600
ROWS, COLS = 30, 60  # Nombre de lignes et colonnes dans la grille
SQUARE_WIDTH = WIDTH // COLS
SQUARE_HEIGHT = HEIGHT // ROWS


class SQUARE:
    def __init__(self, size, pos, free=True):
        self.size = size
        self.pos = pos
        self.free = free
    def __lt__(self, other):
        # Compare squares based on position or other attributes if needed
        return self.pos < other.pos
    def __eq__(self, other):
        return self.pos == other.pos


squares = []  # Create a 2D list to hold squares
# Assuming ROWS and COLS are defined and SQUARE is a class or function
for i in range(COLS):
    line = []  # Create a new row for each row index
    for j in range(ROWS):
        square = SQUARE((SQUARE_WIDTH, SQUARE_HEIGHT), (i, j))  # Create a square
        line.append(square)  # Add the square to the current row
    squares.append(line)  # Append the completed row to the squares list

Start_square = squares[0][10]
End_square = squares[59][20]




a_stare_path = a_star(Start_square, End_square, squares)


class Entite:
    def __init__(self, pathAlgo, health=100, speed=1, damage=10):
        self.pos = Start_square.pos  # Starting position
        self.size = 5  # the size
        self.pathAlgo = pathAlgo  # Pathfinding algorithm the A*
        self.health = health  # Health
        self.speed = speed  # Speed of the entite
        self.damage = damage  # Damage caused by the towers
        self.target = End_square  # Target square the end square

    def path(self):
        if self.pathAlgo == "A*":
            # Call the A* algorithm 
            return a_stare_path
        return None
    
    def move(self):
        if self.target:
           
            pass

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
      
        print("Enemy has died.")

    def check_alive(self):
        return self.health > 0

    def set_target(self, target):
        self.target = target 

entites = []
num_entites = 2
for i in range(num_entites):
    entites.append(Entite("A*"))


         
          

# Fenêtre Pygame
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("test des Chemins")

image = pygame.image.load("Untitled.svg")

# Create a clock object to manage the frame rate
clock = pygame.time.Clock()




win.fill((255, 255, 255))

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
             print(event.pos)
             win.blit(pygame.transform.scale(image, (100, 100)), (event.pos[0] - 50, event.pos[1] - 50))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for entite in entites:
                    entite.pos = Start_square.pos
            if event.key == pygame.K_a:
                for square in a_stare_path:
                    pygame.draw.rect(win, (0,255,255), (square.pos[0] * SQUARE_WIDTH, square.pos[1] * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))

                    
    for i in range(ROWS):
        pygame.draw.line(win, (0,0,0), (0, i * SQUARE_HEIGHT), (WIDTH, i * SQUARE_HEIGHT))
    for j in range(COLS):
        pygame.draw.line(win, (0,0,0), (j * SQUARE_WIDTH, 0), (j * SQUARE_WIDTH, HEIGHT))
    #start square drawing
    
    pygame.draw.rect(win, (0,255,0), (Start_square.pos[0] * SQUARE_WIDTH, Start_square.pos[1] * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))
    pygame.draw.rect(win, (255,0,0), (End_square.pos[0] * SQUARE_WIDTH, End_square.pos[1] * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))
    
    for entite in entites:
        pygame.draw.circle(win, (0,0,0), (entite.pos[0] * SQUARE_WIDTH, entite.pos[1] * SQUARE_HEIGHT), entite.size)
        
        entite.pos =  (entite.pos[0] + 0.01, entite.pos[1] + 0.01)
    
    pygame.display.update()
    clock.tick(120)

pygame.quit()






