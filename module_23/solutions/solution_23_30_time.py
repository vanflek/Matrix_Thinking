import numpy as np
from wireframe_scene import GameLogic

logic = GameLogic()
initial = logic.get_rotation_matrix(0.3, 0.5, -0.2).T
angular_speed = np.array([0.0, 0.0, 0.6])
expected = logic.get_rotation_matrix(0.0, 0.0, 0.6 * 2.0).T @ initial
results = []

for fps in (30, 60, 144):
    obj = {"orientation": initial.copy()}
    dt = 1.0 / fps
    for _ in range(2 * fps):
        ax, ay, az = angular_speed * dt
        logic.rotate_object(obj, ax, ay, az)
    orientation = obj["orientation"]
    results.append(orientation)
    basis = orientation[:3, :3]
    assert np.allclose(orientation, expected)
    assert np.allclose(np.linalg.norm(basis, axis=1), np.ones(3))
    assert np.allclose(basis @ basis.T, np.eye(3))
    print(fps, np.allclose(orientation, expected))

assert np.allclose(results[0], results[1])
assert np.allclose(results[1], results[2])

wrong_results = []
for fps in (30, 60, 144):
    obj = {"orientation": initial.copy()}
    for _ in range(2 * fps):
        ax, ay, az = angular_speed
        logic.rotate_object(obj, ax, ay, az)
    wrong_results.append(obj["orientation"])
print("Without dt:", np.allclose(wrong_results[0], wrong_results[1]))
