import numpy as np


class GameLogic:
    def choose_shooter(self, enemies):
        enemy_rows = np.where(np.any(enemies, axis=1))[0]
        lowest_row = enemy_rows.max() if enemy_rows.size > 0 else None
        if lowest_row is None:
            return None
        enemy_cols = np.where(enemies[lowest_row])[0]
        col = enemy_cols[len(enemy_cols) // 2]
        return lowest_row, col


enemies = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
], dtype=np.uint8)

occupied_rows = np.any(enemies, axis=1)
enemy_rows = np.where(occupied_rows)[0]
print("Occupied rows:", occupied_rows)
print("Row indices:", enemy_rows)

logic = GameLogic()
row, col = logic.choose_shooter(enemies)
print("Shooter:", row, col)
print("Empty formation:", logic.choose_shooter(np.zeros_like(enemies)))
