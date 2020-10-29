import json
import random
import string
from datetime import datetime
from typing import Dict, List, Union, Tuple, Optional

from bson import ObjectId
from flask import Flask, Response, request
from pymongo import MongoClient

from cards import ALL_CARD_NAMES
from config import MONGODB_HOST
from game import init_game, Board, apply_move, check_win_condition
from conversions import board_to_str, str_to_board, notation_to_pos, get_card_from_name, get_cards_from_names
from structures import Player, GameState

app = Flask(__name__)

mongodb = MongoClient(MONGODB_HOST)
matches = mongodb.litama.matches

stream_queue: Dict[str, List[Union[str, Tuple[str, datetime]]]] = {}


def generate_state_dict(match: Dict) -> Dict:
    return {
        "currentTurn": match["currentTurn"],
        "cards": match["cards"],
        "startingCards": match["startingCards"],
        "moves": match["moves"],
        "board": match["board"],
        "gameState": match["gameState"],
        "winner": match["winner"]
    }


def stream_match(match_id: str):
    queue: List[Union[str, Tuple[str, datetime]]] = stream_queue[match_id]
    latest_index = len(queue) - 1  # Only send the most recent message in the queue
    while True:
        queue_length = len(queue)
        # It's only ever a tuple if it's the final message in the queue
        # We store the datetime so that this element in the dictionary can be cleared up later
        if queue_length == latest_index:
            continue
        if type(queue[latest_index]) == tuple:
            yield queue[latest_index][0]
            break
        yield queue[latest_index]
        latest_index += 1


@app.route("/game/create", methods=["POST"])
def game_create():
    token = "".join(random.choices(string.ascii_letters + string.digits, k=32))
    color: str = "Blue"
    enemy: str = "Red"
    if random.random() < 0.5:
        color = "Red"
        enemy = "Blue"
    insert = {
        f"token{color}": token,
        f"token{enemy}": "",
        "gameState": GameState.WAITING_FOR_PLAYER.value
    }
    match_id = str(matches.insert_one(insert).inserted_id)

    return {
        "matchId": match_id,
        "token": token,
        "color": color.lower()
    }


@app.route("/game/join/<string:match_id>", methods=["POST"])
def game_join(match_id: str):
    object_id = ObjectId(match_id)
    match = matches.find_one({"_id": object_id})
    if match is None:
        return Response("Match not found", 404)
    if match["gameState"] != GameState.WAITING_FOR_PLAYER.value:
        return Response("Not allowed to join", 401)

    token = "".join(random.choices(string.ascii_letters + string.digits, k=32))
    color: str = "red" if match["tokenRed"] == "" else "blue"
    board, blue_cards, red_cards, side_card = init_game()

    matches.find_one_and_update(
        {"_id": object_id},
        {"$set": {
            f"token{color.title()}": token,
            "gameState": GameState.IN_PROGRESS.value,
            "board": board_to_str(board),
            "moves": [],
            "currentTurn": side_card.color.value,
            "cards": {
                "blue": [i.name for i in blue_cards],
                "red": [i.name for i in red_cards],
                "side": side_card.name
            },
            "startingCards": {
                "blue": [i.name for i in blue_cards],
                "red": [i.name for i in red_cards],
                "side": side_card.name
            },
            "winner": Player.NONE.value
        }}
    )

    add_state_to_stream_queue(match_id, object_id)

    return {
        "token": token,
        "color": color
    }


@app.route("/game/stream/<string:match_id>", methods=["GET"])
def game_stream(match_id: str):
    object_id = ObjectId(match_id)
    match = matches.find_one({"_id": object_id})
    if match is None:
        return Response("Match not found", 404)
    if match["gameState"] == GameState.ENDED.value:
        return game_state(match_id)
    if match_id not in stream_queue:
        stream_queue[match_id] = ["started\n"]
    return Response(stream_match(match_id))


@app.route("/game/state/<string:match_id>", methods=["GET"])
def game_state(match_id: str):
    object_id = ObjectId(match_id)
    match = matches.find_one({"_id": object_id})
    if match is None:
        return Response("Match not found", 404)
    return generate_state_dict(match)


def add_state_to_stream_queue(match_id: str, object_id: ObjectId, ended=False):
    state = generate_state_dict(matches.find_one({"_id": object_id}))
    state_message = json.dumps(state, separators=(',', ':')) + "\n"
    if ended:
        state_message = (state_message, datetime.utcnow())
    stream_queue[match_id].append(state_message)


@app.route("/game/move/<string:match_id>", methods=["POST"])
def game_move(match_id: str):
    object_id = ObjectId(match_id)
    match = matches.find_one({"_id": object_id})
    if match is None:
        return Response("Match not found", 404)
    if match["gameState"] == GameState.ENDED.value:
        return Response("Game ended", 409)

    token: str = request.form.get("token", "none", str)
    if token == match["tokenBlue"]:
        color = "blue"
    elif token == match["tokenRed"]:
        color = "red"
    else:
        return Response("Token is incorrect", 401)

    move: Optional[str] = request.form.get("move", None, str)
    card_name: Optional[str] = request.form.get("card", None, str)
    if move[0] not in "abdce" or move[1] not in "12345" or move[2] not in "abcde" or move[3] not in "12345":
        move = None
    if card_name not in ALL_CARD_NAMES:
        card_name = None
    if move is None or card_name is None:
        return Response("'move' or 'card' not given properly", 409)

    board = str_to_board(match["board"])
    piece_pos = notation_to_pos(move[:2])

    if board[piece_pos.y][piece_pos.x].color.value != color:
        return Response("Cannot move opponent's pieces or empty squares", 409)

    move_pos = notation_to_pos(move[2:])
    move_card = get_card_from_name(card_name)
    cards = get_cards_from_names(match["cards"][color])
    new_board: Optional[Board] = apply_move(piece_pos, move_pos, move_card, cards, board)

    if new_board is None:
        return Response("Invalid move", 409)

    winner = check_win_condition(new_board)
    state = GameState.ENDED.value if winner != Player.NONE else GameState.IN_PROGRESS.value

    moves = match["moves"]
    moves.append(f"{move}:{card_name}")
    side_card: str = match["cards"]["side"]
    new_cards: List[str] = match["cards"][color]
    new_cards[new_cards.index(card_name)] = side_card

    enemy = "red" if color == "blue" else "blue"
    enemy_cards = match["cards"][enemy]

    matches.find_one_and_update(
        {"_id": object_id},
        {"$set": {
            "board": board_to_str(new_board),
            "moves": moves,
            "currentTurn": "blue" if color == "red" else "red",
            "cards": {
                enemy: enemy_cards,
                color: new_cards,
                "side": card_name
            },
            "gameState": state,
            "winner": winner.value
        }}
    )

    add_state_to_stream_queue(match_id, object_id, state == GameState.ENDED.value)

    return Response("Move made", 200)


@app.route("/game")
def game():
    ret = "REST endpoints for /game/...:<br>"
    ret += '<br>'.join(str(x) for x in app.url_map._rules if x.rule.startswith("/game/"))
    return ret


# TODO: Timed clear out of finished matches from stream_queue

@app.route("/")
def index():
    return "index page"
