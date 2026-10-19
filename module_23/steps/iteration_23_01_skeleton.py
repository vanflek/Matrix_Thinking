import pygame as pg
import numpy as np


WIDTH, HEIGHT = 1000, 1000
FPS = 60
COLORS = {
    "background": (20, 23, 30),
    "white": (235, 239, 246),
    "muted": (132, 144, 163),
}


class Camera:
    def __init__(self):
        self.position = np.array([1.5, 1.2, -5.0, 1.0])


class GameModel:
    def __init__(self):
        self.objects = {}


class InputController:
    def get_actions(self):
        actions = {"quit": False}

        for event in pg.event.get():
            if event.type == pg.QUIT:
                actions["quit"] = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    actions["quit"] = True

        return actions


class GameLogic:
    pass


class GameView:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Module 23 - 3D wireframe")
        self.font = pg.font.Font(None, 30)

    def draw(self, model):
        self.screen.fill(COLORS["background"])

        title = self.font.render(
            "Module 23 | 3D wireframe", True, COLORS["white"]
        )
        self.screen.blit(title, (20, 20))

        help_text = self.font.render(
            "Esc: quit", True, COLORS["muted"]
        )
        self.screen.blit(help_text, (20, HEIGHT - 40))
        pg.display.flip()


class GameApp:
    def __init__(self):
        pg.init()
        self.model = GameModel()
        self.controller = InputController()
        self.logic = GameLogic()
        self.view = GameView()
        self.camera = Camera()
        self.clock = pg.time.Clock()

    def run(self):
        while True:
            self.clock.tick(FPS)
            actions = self.controller.get_actions()
            if actions["quit"]:
                break

            self.view.draw(self.model)

        pg.quit()


if __name__ == "__main__":
    game = GameApp()
    game.run()
