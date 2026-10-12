import pygame as pg

pg.init()

# --- window settings ---
width = 800
height = 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Ball control (KEYDOWN)")

# --- colors ---
BACKGROUND = (230, 230, 230)
BLUE = (60, 120, 200)

# --- timing ---
clock = pg.time.Clock()
FPS = 60

# --- ball settings ---
radius = 30

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

            # ESC closes the program
            if event.key == pg.K_ESCAPE:
                running = False

            # arrows move the ball (one step per key press)
            elif event.key == pg.K_LEFT:
                x = x - 40
            elif event.key == pg.K_RIGHT:
                x = x + 40
            elif event.key == pg.K_UP:
                y = y - 40
            elif event.key == pg.K_DOWN:
                y = y + 40

    # --- 2) frame rate ---
    clock.tick(FPS)

    # --- 3) keep the circle inside the window ---
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
    pg.draw.circle(screen, BLUE, (int(x), int(y)), radius)
    pg.display.flip()

pg.quit()
