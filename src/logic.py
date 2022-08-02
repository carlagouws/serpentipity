import random
from typing import List


def get_info() -> dict:
    """
    Controls Battlesnake appearance and author permissions.
    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    return {
        "apiversion": "1",
        "author": "cgouws",
        "color": "#A569BD",
        "head": "evil",
        "tail": "small-rattle",
    }


def choose_move(data: dict) -> str:
    # Output input data
    print(f"~~~ Turn: {data['turn']} ~~~")
    print(data)

    my_snake = data["you"]
    my_head = my_snake["head"]
    my_body = my_snake["body"]
    board = data["board"]
    board_height = board["height"]
    board_width = board["width"]
    snakes = board["snakes"]

    possible_moves = ["left", "right", "down", "up"]

    possible_moves = _avoid_my_neck(my_body, possible_moves)
    print(f"Avoid neck: {possible_moves}")
    possible_moves = _avoid_the_wall(my_head, board_height, board_width, possible_moves)
    print(f"Avoid wall: {possible_moves}")
    possible_moves = _avoid_snakes(my_head, snakes, possible_moves)
    print(f"Avoid snakes: {possible_moves}")

    food = data["board"]["food"]
    food_moves = food_options_in_best_order(my_head, food)
    print(f"Food options: {food_moves}")

    valid_food_moves = eliminate_poor_food_choices(food_moves, possible_moves)
    print(f"Valid food options: {food_moves}")

    possible_moves = combine_all_possible_moves(valid_food_moves, possible_moves)
    print(f"Possible moves: {possible_moves}")

    move = possible_moves[0]
    print(f"Chosen move: {move}")
    return move


def food_options_in_best_order(my_head: dict, food: List[dict]) -> List[str]:
    closest_food_asc = sort_by_closest_coord(my_head, food)
    moves_to_food = []
    for food in closest_food_asc:
        directions = best_directions_to_coord(my_head, food)
        random.shuffle(directions)
        moves_to_food.extend(directions)
    return list(dict.fromkeys(moves_to_food))


def sort_by_closest_coord(location: dict, list_of_coords: List[dict]) -> List[dict]:
    indexed_coords = {}
    for i in range(len(list_of_coords)):
        indexed_coords[
            abs(list_of_coords[i]["x"] - location["x"])
            + abs(list_of_coords[i]["y"] - location["y"])
        ] = list_of_coords[i]
    order = sorted(indexed_coords)
    ordered_coords = []
    for i in order:
        ordered_coords.append(indexed_coords[i])
    return ordered_coords


def best_directions_to_coord(my_head: dict, coord: dict) -> List[str]:
    directions = []
    if coord["x"] < my_head["x"]:
        directions.append("left")
    if coord["x"] > my_head["x"]:
        directions.append("right")
    if coord["y"] < my_head["y"]:
        directions.append("down")
    if coord["y"] > my_head["y"]:
        directions.append("up")

    return directions


def eliminate_poor_food_choices(
    food_moves: List[str], possible_moves: List[str]
) -> List[str]:
    valid_food_moves = []
    for move in food_moves:
        if move in possible_moves:
            valid_food_moves.append(move)
    return valid_food_moves


def combine_all_possible_moves(
    valid_food_moves: List[str], possible_moves: List[str]
) -> List[str]:
    valid_food_moves.extend(possible_moves)
    return list(dict.fromkeys(valid_food_moves))


def _avoid_my_neck(my_body: dict, possible_moves: List[str]) -> List[str]:
    my_head = my_body[0]
    my_neck = my_body[1]

    if my_neck["x"] < my_head["x"]:
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:
        possible_moves.remove("up")

    return possible_moves


def _avoid_the_wall(
    my_head: dict, board_height: int, board_width: int, possible_moves: List[str]
) -> List[str]:
    if "left" in possible_moves and my_head["x"] == 0:
        possible_moves.remove("left")
    if "right" in possible_moves and my_head["x"] == board_width - 1:
        possible_moves.remove("right")
    if "down" in possible_moves and my_head["y"] == 0:
        possible_moves.remove("down")
    if "up" in possible_moves and my_head["y"] == board_height - 1:
        possible_moves.remove("up")

    return possible_moves


def _avoid_snakes(
    my_head: dict, snakes: List[dict], possible_moves: List[str]
) -> List[str]:
    for snake in snakes:
        body = snake["body"]
        # Remove last part of the body since it won't be there in the next move
        body.pop()

        if (
            "left" in possible_moves
            and {"x": my_head["x"] - 1, "y": my_head["y"]} in body
        ):
            possible_moves.remove("left")
        if (
            "right" in possible_moves
            and {"x": my_head["x"] + 1, "y": my_head["y"]} in body
        ):
            possible_moves.remove("right")
        if (
            "down" in possible_moves
            and {"x": my_head["x"], "y": my_head["y"] - 1} in body
        ):
            possible_moves.remove("down")
        if (
            "up" in possible_moves
            and {"x": my_head["x"], "y": my_head["y"] + 1} in body
        ):
            possible_moves.remove("up")

    return possible_moves
