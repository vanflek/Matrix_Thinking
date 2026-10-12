import pygame as pg

pg.init()

# --- window settings ---
width = 800
height = 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Ball follows mouse (cursor visible)")

pg.mouse.set_visible(True)  # show the system mouse cursor

# --- colors ---
BACKGROUND = (230, 230, 230)
BLUE = (60, 120, 200)

# --- timing ---
clock = pg.time.Clock()
FPS = 60

# --- ball settings ---
radius = 30

running = True

while running:

    # --- 1) events (input) ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    # --- 2) frame rate ---
    clock.tick(FPS)

    # --- 3) update (logic) ---
    x, y = pg.mouse.get_pos()   # mouse position is a vector (x, y)

    # keep the circle inside the window
    if x - radius < 0:
        x = radius
    elif x + radius > width:
        x = width - radius

    if y - radius < 0:
        y = radius
    elif y + radius > height:
        y = height - radius

    # --- 4) draw (render) ---
    screen.fill(BACKGROUND)
    pg.draw.circle(screen, BLUE, (x, y), radius)
    pg.display.flip()

pg.quit()
