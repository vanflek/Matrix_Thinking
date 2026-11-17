"""Matrix Thinking: two whole camera frames, one difference, one Boolean mask.

Run: python motion_numpy.py
Console only: python motion_numpy.py --check
"""
import argparse
import numpy as np

ROWS, COLS = 24, 32
DUCK = np.array([
    [0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 0, 0],
    [1, 0, 0, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
], dtype=bool)


def make_frame(row=8, col=8, brightness=210, light=0, noise=0, seed=1):
    """Synthetic grayscale camera, no hardware required. Brightness is 0..255."""
    if not (0 <= row <= ROWS - 8 and 0 <= col <= COLS - 8):
        raise ValueError("The duck must fit inside the frame.")
    yy, xx = np.indices((ROWS, COLS))
    frame = 32 + ((yy // 4 + xx // 4) % 2) * 6
    patch = frame[row:row + 8, col:col + 8]
    patch[DUCK] = brightness
    # Deterministic noise: the website and Python use this same expression.
    indices = np.arange(ROWS * COLS).reshape(ROWS, COLS)
    perturbation = (((indices * 37 + seed * 101) % 17 - 8) * noise) // 8
    return np.clip(frame + light + perturbation, 0, 255).astype(np.uint8)


def detect_changes(previous, current, threshold=30):
    """Calculate the whole field at once, with no loop over individual pixels."""
    previous = np.asarray(previous)
    current = np.asarray(current)
    if previous.shape != current.shape or previous.ndim != 2:
        raise ValueError("Use two grayscale matrices with the same shape.")
    if not 0 <= threshold <= 255:
        raise ValueError("Threshold must be between 0 and 255.")
    # Convert BEFORE subtraction: uint8 cannot represent negative differences.
    difference = np.abs(current.astype(np.int16) - previous.astype(np.int16))
    motion_mask = difference > threshold
    changed_pixels = int(np.count_nonzero(motion_mask))
    changed_fraction = float(np.mean(motion_mask))
    return difference, motion_mask, changed_pixels, changed_fraction


def run():
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((1000, 900))
    pygame.display.set_caption("Matrix Thinking — whole-frame change detection")
    font = pygame.font.SysFont("consolas", 18)
    small = pygame.font.SysFont("consolas", 15)
    clock = pygame.time.Clock()
    row, col, brightness, light, noise, seed, threshold = 8, 12, 210, 0, 0, 1, 30
    previous = make_frame(8, 8)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    col = max(0, col - 1)
                elif event.key == pygame.K_RIGHT:
                    col = min(COLS - 8, col + 1)
                elif event.key == pygame.K_UP:
                    row = max(0, row - 1)
                elif event.key == pygame.K_DOWN:
                    row = min(ROWS - 8, row + 1)
                elif event.key == pygame.K_SPACE:
                    previous = make_frame(row, col, brightness, light, noise, seed)
                elif event.key == pygame.K_n:
                    noise = 8 if noise == 0 else 0
                    seed += 1
                elif event.key == pygame.K_l:
                    light = 55 if light == 0 else 0
                elif event.key == pygame.K_c:
                    brightness = 55 if brightness == 210 else 210
                    previous = make_frame(8, 8, brightness)
                elif event.key == pygame.K_PAGEUP:
                    threshold = min(255, threshold + 5)
                elif event.key == pygame.K_PAGEDOWN:
                    threshold = max(0, threshold - 5)
                elif event.key == pygame.K_r:
                    row, col, brightness, light, noise, seed, threshold = 8, 12, 210, 0, 0, 1, 30
                    previous = make_frame(8, 8)
        current = make_frame(row, col, brightness, light, noise, seed)
        difference, mask, count, fraction = detect_changes(previous, current, threshold)
        screen.fill((250, 251, 248))
        # Rendering adapts whole matrices to RGB surfaces. It does not calculate
        # the change mask; detect_changes above performs that calculation.
        for i, (title, data) in enumerate([
            ("01 / Previous frame", previous), ("02 / Current frame", current),
            ("03 / Absolute difference", difference), ("04 / Boolean mask", mask * 255),
        ]):
            x, y = 24 + (i % 2) * 490, 50 + (i // 2) * 380
            screen.blit(font.render(title, True, (19, 45, 69)), (x, y - 27))
            rgb = np.repeat(data.astype(np.uint8)[..., None], 3, axis=2)
            surface = pygame.surfarray.make_surface(rgb.swapaxes(0, 1))
            screen.blit(pygame.transform.scale(surface, (448, 336)), (x, y))
        lines = [
            f"threshold = {threshold}    changed = {count}/{ROWS * COLS} ({fraction:.1%})",
            "Arrows: move duck | Space: current -> previous | Page Up/Down: threshold",
            "N: noise | L: lighting | C: contrast (resets previous) | R: reset | Esc: exit",
            "Both the old and new duck positions can be marked. This detects change, not objects.",
        ]
        for i, line in enumerate(lines):
            screen.blit(small.render(line, True, (19, 45, 69)), (24, 805 + i * 23))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Run a console example without a window")
    args = parser.parse_args()
    if args.check:
        previous = make_frame(8, 8)
        current = make_frame(8, 12)
        difference, mask, count, fraction = detect_changes(previous, current)
        print("Frame shape:", current.shape)
        print("Changed pixels:", count)
        print("Changed fraction:", fraction)
        print("Difference range:", int(difference.min()), int(difference.max()))
    else:
        run()
