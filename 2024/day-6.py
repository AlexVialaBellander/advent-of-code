import numpy as np
from collections import defaultdict

with open("day-6.txt") as file:
    data = file.read().strip()


def find_next_pos(
    current_pos, direction, vertical_obstacles, horizontal_obstacles, height, width
):
    in_same_column = vertical_obstacles[current_pos[1]]
    in_same_row = horizontal_obstacles[current_pos[0]]
    r, c = current_pos

    # Add an artificial obstacle at the edge of the universe, allowing
    # one to move beyond the 'natural' edge.
    if direction == "north":
        # Obstacles above current row
        candidates = [x for x in in_same_column if x < r] + [-2]
        return (max(candidates) + 1, c), "east"
    elif direction == "east":
        # Obstacles to the right in the current row
        candidates = [x for x in in_same_row if x > c] + [width + 1]
        return ((r, min(candidates) - 1), "south")
    elif direction == "south":
        # Obstacles below current row
        candidates = [x for x in in_same_column if x > r] + [height + 1]
        return (min(candidates) - 1, c), "west"
    elif direction == "west":
        # Obstacles to the left in the current row
        candidates = [x for x in in_same_row if x < c] + [-2]
        return (r, max(candidates) + 1), "north"


def points_between(point_a, point_b, direction):
    if direction == "north":
        return [(x, point_a[1]) for x in range(point_b[0], point_a[0] + 1)]
    elif direction == "east":
        return [(point_a[0], y) for y in range(point_a[1], point_b[1] + 1)]
    elif direction == "south":
        return [(x, point_a[1]) for x in range(point_a[0], point_b[0] + 1)]
    elif direction == "west":
        return [(point_a[0], y) for y in range(point_b[1], point_a[1] + 1)]


def traverse(universe) -> int | bool:
    visited = set()
    legs = set()

    height, width = universe.shape

    original_starting_pos = data.replace("\n", "").find("^")
    starting_pos = (original_starting_pos // width, original_starting_pos % width)

    horizontal_obstacles = defaultdict(list)
    vertical_obstacles = defaultdict(list)

    for i, row in enumerate(universe):
        for j, cell in enumerate(row):
            if cell == "#":
                horizontal_obstacles[i].append(j)

    for j, col in enumerate(universe.T):
        for i, cell in enumerate(col):
            if cell == "#":
                vertical_obstacles[j].append(i)

    current_pos = starting_pos
    current_direction = "north"

    hash_leg = lambda x: str(", ".join([f"{point[0]}:{point[1]}" for point in x]))

    while True:
        next_pos, new_direction = find_next_pos(
            current_pos,
            current_direction,
            vertical_obstacles,
            horizontal_obstacles,
            height,
            width,
        )
        traversed_points = points_between(current_pos, next_pos, current_direction)
        visited.update(traversed_points)
        current_pos, current_direction = next_pos, new_direction
        if next_pos[0] in [-1, height] or next_pos[1] in [-1, width]:
            # Remove the artificially added allowed point that is beyond the 'natural' edge.
            visited.remove(next_pos)
            return visited
        elif hash_leg(traversed_points) in legs:
            return True
        legs.add(
            str(", ".join([f"{point[0]}:{point[1]}" for point in traversed_points]))
        )


# Part 1
universe = np.array([list(x) for x in data.split("\n") if x])
visited = traverse(universe)
assert type(visited) == set
print(f"Unique points traversed: {len(visited)}")

# Part 2
loops_found = 0
for i, (row, col) in enumerate(visited):
    print(f"Checking {row}, {col}, {i}/{len(visited)}")
    new_universe = universe.copy()
    new_universe[row, col] = "#"
    did_find_loop = traverse(new_universe)
    if did_find_loop == True:
        loops_found += 1
print(f"Loops found: {loops_found}")
