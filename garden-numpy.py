"""A whole world of rectangular gardens, calculated with NumPy."""
import argparse
import numpy as np


def build_world(fence=24, minimum=30):
    if not isinstance(fence, int) or not 4 <= fence <= 200:
        raise ValueError("Use a whole fence budget of 4–200 metres.")
    if not isinstance(minimum, int) or minimum < 1:
        raise ValueError("Use a positive whole minimum area.")

    sizes = np.arange(1, fence // 2 + 1)
    width, length = np.meshgrid(sizes, sizes, indexing="ij")

    perimeter = 2 * (width + length)
    area = width * length

    fence_ok = perimeter <= fence
    area_ok = area >= minimum
    mask = fence_ok & area_ok

    solutions = np.column_stack((
        width[mask], length[mask],
        perimeter[mask], area[mask],
    ))
    best = solutions[solutions[:, 3] == solutions[:, 3].max()] if len(solutions) else solutions.copy()

    return dict(
        width=width, length=length,
        perimeter=perimeter, area=area,
        fence_ok=fence_ok, area_ok=area_ok, mask=mask,
        solutions=solutions, best=best,
        largest_within_fence=int(area[fence_ok].max()),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fence", type=int, default=24)
    parser.add_argument("--minimum", type=int, default=30)
    args = parser.parse_args()

    world = build_world(args.fence, args.minimum)
    print("Columns: width, length, fence needed, area")
    print(world["solutions"])
    print("Number of oriented solutions:", len(world["solutions"]))
    print("Best suitable gardens:")
    print(world["best"])
    print("Largest area within the fence budget:", world["largest_within_fence"])
