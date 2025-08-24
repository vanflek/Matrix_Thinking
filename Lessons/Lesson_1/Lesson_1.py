import pygame
import numpy

pygame.init()
#matrix
screen_matrix = numpy.zeros((16, 32), dtype=numpy.uint8)


#pygame
TILE_SIZE = 32
TILE_Y, TILE_X = screen_matrix.shape

WIDTH, HEIGHT = TILE_SIZE * TILE_X, TILE_SIZE * TILE_Y
FPS = 60
colors = {0:(255,255,255), 1:(0,0,0), 2:(255, 0,0), 3:(0,255,0), 4:(0,0,255), 5:(191,191,191)}
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #drawing
    for y in range(TILE_Y):
        for x in range(TILE_X):
            if screen_matrix[y][x] == 0:
                pygame.draw.rect(screen, colors[0], (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(screen, colors[1], (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, colors[1], (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()