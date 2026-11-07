"""Matrix Thinking sandbox: complete whole-array NumPy reference.

Run: python sandbox-numpy.py  (requires NumPy)
analyze(W, ...) implements the same priority policy as the browser bit-plane
engine. The simulation loops over at most nine directional masks, never cells.
Rendering and importing an edited grid are separate from the simulation step.
W: 2-D array of IDs: 0 empty, 1 sand, 2 water, 3 wall. Zero exterior; no wrapping.
"""

import numpy as np

GRAVITY = {"down": (1, 0), "left": (0, -1), "up": (-1, 0), "right": (0, 1)}


def shift(mask, dr, dc):
    """Move a whole matrix; fill the exposed exterior with False."""
    height, width = mask.shape
    out = np.zeros_like(mask)
    if abs(dr) >= height or abs(dc) >= width:
        return out
    sr = slice(max(0, -dr), min(height, height - dr))
    sc = slice(max(0, -dc), min(width, width - dc))
    tr = slice(max(0, dr), min(height, height + dr))
    tc = slice(max(0, dc), min(width, width + dc))
    out[tr, tc] = mask[sr, sc]
    return out


def analyze(W, *, gravity="down", diagonals=True, spread=True, tick=0):
    W = np.asarray(W)
    if W.ndim != 2 or min(W.shape) < 1 or not np.isin(W, [0, 1, 2, 3]).all():
        raise ValueError("W must be a nonempty 2-D matrix of IDs 0, 1, 2, 3")
    sand, water, wall, empty = W == 1, W == 2, W == 3, W == 0
    mobile = sand | water
    rows, cols = np.indices(W.shape)
    plus = ((rows + cols + tick) % 2) == 0
    minus = ~plus
    dy, dx = GRAVITY.get(gravity, GRAVITY["down"])
    py, px = -dx, dy
    full = np.ones(W.shape, dtype=bool)
    directions = [(dy, dx, full, 1)]
    if diagonals:
        directions += [
            (dy + py, dx + px, plus, 2),
            (dy - py, dx - px, minus, 2),
            (dy + py, dx + px, minus, 2),
            (dy - py, dx - px, plus, 2),
        ]
    if spread:
        directions += [
            (py, px, plus & water, 3),
            (-py, -px, minus & water, 3),
            (py, px, minus & water, 3),
            (-py, -px, plus & water, 3),
        ]
    remaining = mobile.copy()
    claimed = np.zeros_like(full)
    requested = np.zeros_like(full)
    targets = np.zeros_like(full)
    moves = np.zeros(W.shape, dtype=np.uint8)
    next_W = W.copy()
    groups = []

    # Fixed directional passes. Every expression acts on an ENTIRE matrix.
    for dr, dc, scope, kind in directions:
        empty_ahead = shift(empty, -dr, -dc)
        swap_eligible = sand & shift(water, -dr, -dc) if kind != 3 else np.zeros_like(full)
        allowed = full
        if kind == 2:
            corner = shift(wall, -dy, -dx) & shift(wall, -(dr - dy), -(dc - dx))
            allowed = ~corner
        proposed = remaining & scope & allowed & (empty_ahead | swap_eligible)
        remaining &= ~proposed
        requested |= proposed

        # Within a direction, translations have unique destinations. A swap
        # claims both cells before water may use its own source proposal.
        free = ~claimed
        swaps = proposed & swap_eligible & free & shift(free, -dr, -dc)
        swap_targets = shift(swaps, dr, dc)
        claimed |= swaps | swap_targets
        free = ~claimed
        ordinary = proposed & empty_ahead & free & shift(free, -dr, -dc)
        accepted = swaps | ordinary
        destinations = shift(accepted, dr, dc)
        claimed |= ordinary | shift(ordinary, dr, dc)
        targets |= destinations

        # All writes select Boolean masks; all values come from the old W.
        source_for_destination = shift(W, dr, dc)
        next_W[ordinary] = 0
        next_W[destinations] = source_for_destination[destinations]
        next_W[swaps] = 2
        moves[ordinary] = kind
        moves[swaps] = 4
        groups.append({"dr": dr, "dc": dc, "kind": kind,
                       "proposed": proposed, "accepted": accepted,
                       "swaps": swaps, "rejected": proposed & ~accepted})

    return {"next": next_W, "moves": moves, "requested": requested,
            "targets": targets, "claimed": claimed, "groups": groups,
            "counts": np.bincount(W.ravel(), minlength=4)}


if __name__ == "__main__":
    world = np.zeros((12, 18), dtype=np.uint8)
    world[[0, -1], :] = 3
    world[:, [0, -1]] = 3
    world[2:5, 7:11] = 1
    world[8:11, 2:16] = 2
    initial_counts = np.bincount(world.ravel(), minlength=4)
    for step in range(100):  # Time steps, not cells.
        world = analyze(world, tick=step)["next"]
        assert np.array_equal(np.bincount(world.ravel(), minlength=4), initial_counts)
    print(world)
    print("100 whole-array steps; sand and water counts conserved.")
