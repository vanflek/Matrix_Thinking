import pygame
import numpy

def grid_draw(screen_size, b_ground_color, greed_color):
    surface = pygame.Surface(screen_size, pygame.SRCALPHA)
    surface.fill(b_ground_color)
    for y in range(TILE_Y + 1):
        pygame.draw.line(surface, greed_color, (0, y * TILE_SIZE), (WIDTH, y * TILE_SIZE),1)
    for x in range(TILE_X + 1):
        pygame.draw.line(surface, greed_color, (x * TILE_SIZE, 0), (x * TILE_SIZE, HEIGHT),1)
    return surface
pygame.init()
screen_matrix = numpy.zeros((16, 16, 2), dtype=numpy.uint8)
COLORS = numpy.array(([255, 255, 255], [0, 255, 0], [0, 0, 255],[0, 0, 0]), dtype=numpy.uint8)
TILE_SIZE = 32
TILE_Y, TILE_X = screen_matrix.shape[:2]
WIDTH, HEIGHT = TILE_SIZE * TILE_X, TILE_SIZE * TILE_Y
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

surface_greed = grid_draw(screen.get_size(), numpy.append(COLORS[0], 0), COLORS[3])
#player
player_coordinates = numpy.array((TILE_Y//2, TILE_X//2), dtype=numpy.int32)
screen_matrix[player_coordinates[0], player_coordinates[1], 0] = 1
player_velocities = numpy.array(([0,0],[0,1],[0, -1], [1,0], [-1,0]), dtype=numpy.int8)
velocity = 0



#target
target_coordinates = numpy.array((numpy.random.randint(TILE_Y), numpy.random.randint(TILE_X)), dtype=numpy.int32)
screen_matrix[target_coordinates[0], target_coordinates[1], 1] = 2


run = True
while run:
    velocity = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                velocity = 4
            if event.key == pygame.K_DOWN:
                velocity = 3
            if event.key == pygame.K_LEFT:
                velocity = 2
            if event.key == pygame.K_RIGHT:
                velocity = 1
    if numpy.any((player_coordinates + player_velocities[velocity]) // (TILE_Y, TILE_X)) == 0:
        screen_matrix[player_coordinates[0], player_coordinates[1], 0] = 0
        player_coordinates += player_velocities[velocity]
        screen_matrix[player_coordinates[0], player_coordinates[1], 0] = 1
    temp = screen_matrix[:,:,0] + screen_matrix[:,:,1]
    for y in range(screen_matrix.shape[0]):
        for x in range(screen_matrix.shape[1]):
            pygame.draw.rect(screen, COLORS[temp[y, x]],
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)

    screen.blit(surface_greed, (0, 0))

    pygame.display.update()

pygame.quit()