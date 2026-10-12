import pygame as pg

pg.init()

# --- window settings ---
width = 800
height = 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Falling circle + events")

# --- colors ---
BACKGROUND = (230, 230, 230)
BLUE = (60, 120, 200)

# --- timing ---
clock = pg.time.Clock()
FPS = 60

# --- circle settings ---
radius = 30
speed = 240                      # pixels per second

# --- start position ---
x = width // 2
y = height // 2

running = True

while running:

    # --- 1) events (input) ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    # --- 2) time step ---
    dt = clock.tick(FPS) / 1000  # milliseconds -> seconds

    # --- 3) update (logic) ---
    y = y + speed * dt           # update y coordinate using distance = speed * time

    # stop when the circle reaches the floor
    if y + radius >= height:
        running = False

    # --- 4) draw (render) ---
    screen.fill(BACKGROUND)
    pg.draw.circle(screen, BLUE, (x, int(y)), radius)
    pg.display.flip()

pg.quit()
