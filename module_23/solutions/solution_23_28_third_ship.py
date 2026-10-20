import numpy as np
from wireframe_scene import GameApp, COLORS

if __name__ == "__main__":
    game = GameApp()
    model = game.model
    model.objects["cobra_3"] = {
        "vertices": model.cobra_vertices,
        "edges": model.cobra_edges,
        "position": np.array([0.0, 3.0, 3.0]),
        "initial_angles": np.array([0.2, 0.4, -0.2]),
        "scale": np.array([0.012, 0.012, 0.012]),
        "color": COLORS["green"],
        "show_axes": True,
        "axis_lines": [],
        "angular_speed": np.array([0.0, 0.4, 0.2]),
        "screen_lines": np.empty((0, 2, 2)),
    }
    # Initialize the added object before the first frame.
    game.logic.initialize_orientations(model)
    game.run()
