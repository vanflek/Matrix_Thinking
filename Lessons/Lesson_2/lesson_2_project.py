import pygame
import numpy

pygame.init()
#matrix
screen_matrix = numpy.zeros((16, 32), dtype=numpy.uint8)
# chess board
"""screen_matrix[::2, 1::2] = 1  # black on even Rows
screen_matrix[1::2, ::2] = 1  # vice versa"""
#boards
"""t = 2
screen_matrix[t:screen_matrix.shape[0]-t:, t:screen_matrix.shape[1]-t:] = 1"""
#diagonal
"""for i in range(screen_matrix.shape[0]):
    screen_matrix[i : :,  : i :] = 1"""
#diamond
"""for i in range(screen_matrix.shape[0]):
    screen_matrix[i : :,  : i :] = 1
    screen_matrix[:-i-1:, : i + 1:] = 1
    screen_matrix[0: i:, screen_matrix.shape[1] // 2 + i : screen_matrix.shape[1]:] = 1
    screen_matrix[-i-1::, screen_matrix.shape[1] // 2 + i+1 : screen_matrix.shape[1]:] = 1
"""

x = 4
y = 3
c = 4
w = 2
h = 6
screen_matrix[y:y+h:1, x:x+w:1] = c

print(screen_matrix)
#pygame
TILE_SIZE = 32
TILE_Y, TILE_X = screen_matrix.shape

WIDTH, HEIGHT = TILE_SIZE * TILE_X, TILE_SIZE * TILE_Y
FPS = 60
colors = numpy.array (((255,255,255), (0,0,0), (255, 0,0), (0,255,0), (0,0,255), (191,191,191)), dtype=numpy.uint8)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#grid
surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
surface.fill((0, 0, 0, 0))
for y in range(TILE_Y + 1):
    pygame.draw.line(surface, colors[5], (0, y * TILE_SIZE), (WIDTH, y * TILE_SIZE),1)
for x in range(TILE_X + 1):
    pygame.draw.line(surface, colors[5], (x * TILE_SIZE, 0), (x * TILE_SIZE, HEIGHT),1)
clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #drawing
    x = numpy.random.randint(0, screen_matrix.shape[1])
    y = numpy.random.randint(0, screen_matrix.shape[0])
    c = numpy.random.randint(0, 5)
    w = numpy.random.randint(1, screen_matrix.shape[1] - x+1)
    h = numpy.random.randint(1, screen_matrix.shape[0] - y+1)
    screen_matrix[y:y + h:1, x:x + w:1] = c
    print(screen_matrix)
    for y in range(TILE_Y):
        for x in range(TILE_X):
            pygame.draw.rect(screen, colors[screen_matrix[y,x]], (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    screen.blit(surface, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()