import pygame
import numpy

pygame.init()
#matrix
screen_matrix = numpy.zeros((16, 32), dtype=numpy.uint8)
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
    pygame.draw.line(surface, colors[1], (0, y * TILE_SIZE), (WIDTH, y * TILE_SIZE),1)
for x in range(TILE_X + 1):
    pygame.draw.line(surface, colors[1], (x * TILE_SIZE, 0), (x * TILE_SIZE, HEIGHT),1)
clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #drawing
    for y in range(TILE_Y):
        for x in range(TILE_X):
            pygame.draw.rect(screen, colors[screen_matrix[y,x]], (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    screen.blit(surface, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()