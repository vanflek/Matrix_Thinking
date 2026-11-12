"""Ten fruits, 72 coins: whole-world rules with NumPy.

Assumptions: positive whole-number prices, at least one apple and one banana.
Each position in the 9 x 63 grid represents one candidate purchase.
Columns in the answer: apples, bananas, apple price, banana price.
"""
import numpy as np


def build_world():
    # Rows choose the apple count; columns choose the apple price.
    apples, apple_price = np.meshgrid(
        np.arange(1, 10),
        np.arange(1, 64),
        indexing="ij",
    )

    # These rules act on all 567 candidates at once.
    bananas = 10 - apples
    apple_cost = apples * apple_price
    remaining = 72 - apple_cost

    # A valid basket leaves a positive, whole-number price for each banana.
    enough_money = remaining > 0
    whole_price = remaining % bananas == 0
    mask = enough_money & whole_price

    # Integer division is exact for the cells selected by the mask.
    banana_price = remaining // bananas
    solutions = np.column_stack((
        apples[mask],
        bananas[mask],
        apple_price[mask],
        banana_price[mask],
    ))

    return {
        "apples": apples,
        "apple_price": apple_price,
        "bananas": bananas,
        "apple_cost": apple_cost,
        "remaining": remaining,
        "enough_money": enough_money,
        "whole_price": whole_price,
        "mask": mask,
        "banana_price": banana_price,
        "solutions": solutions,
    }


if __name__ == "__main__":
    world = build_world()
    solutions = world["solutions"]

    print("Columns: apples, bananas, apple price, banana price")
    print(solutions)
    print("Solution matrix shape:", solutions.shape)
    print("Possible apple prices:", np.unique(solutions[:, 2]))
    print("Number of possible apple prices:", np.unique(solutions[:, 2]).size)
