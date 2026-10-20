import pygame as pg

pg.init()

# --- window settings ---
width = 800
height = 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("First while: falling circle (FPS + tick)")

# --- colors ---
BACKGROUND = (230, 230, 230)
BLUE = (60, 120, 200)

# --- timing ---
clock = pg.time.Clock()
FPS = 60                         # maximum frames per second

# --- circle settings ---
radius = 30
speed = 60                      # pixels per second

# --- start position ---
x = width // 2
y = height // 2

running = True

while running:

    pg.event.pump()              # keep the window alive (event.get() later)

    dt = clock.tick(FPS) / 1000  # milliseconds -> seconds

    # --- update ---
    y = y + speed * dt           # compute the new y position for this frame

    if y + radius >= height:
        running = False

    # --- draw ---
    screen.fill(BACKGROUND)
    pg.draw.circle(screen, BLUE, (x, int(y)), radius)
    pg.display.flip()

pg.quit()
