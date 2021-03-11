from typing import List, Optional, Union

from pymongo.collection import Collection

from cards import ALL_BASE_CARD_NAMES
from commands.command import Command
from commands.message import Message
from conversions import board_to_str, str_to_board, notation_to_pos, get_card_from_name, get_cards_from_names
from game import Board, apply_move, check_win_condition
from structures import GameState, Player
from bson import ObjectId


class Move(Command):
    STARTS_WITH = "move "

    @staticmethod
    def apply_command(matches: Collection, query: str) -> List[Message]:
        # Command format: move [match_id] [token] [card] [move]
        # Example: move 5f9c394ee71e1740c218587b iq2V39W9WNm0EZpDqEcqzoLRhSkdD3lY boar a1a2
        split = query.split(" ")
        match_id, token, card_name, move = split

        check: Union[Message, ObjectId] = Command.check_match_id(match_id, "move")
        if isinstance(check, Message):
            return [check]

        object_id = check
        match = matches.find_one({"_id": object_id})
        if match is None:
            return [Command.error_msg("Match not found", "move", match_id)]
        if match["gameState"] == GameState.ENDED.value:
            return [Command.error_msg("Game ended", "move", match_id)]

        if token == match["tokenBlue"]:
            color = "blue"
        elif token == match["tokenRed"]:
            color = "red"
        else:
            return [Command.error_msg("Token is incorrect", "move", match_id)]

        if move[0] not in "abdce" or move[1] not in "12345" or move[2] not in "abcde" or move[3] not in "12345":
            move = "none"
        if card_name not in ALL_BASE_CARD_NAMES:
            card_name = "none"
        if move == "none" or card_name == "none":
            return [Command.error_msg("'move' or 'card' not given properly", "move", match_id)]

        board = str_to_board(match["board"])
        piece_pos = notation_to_pos(move[:2])

        if match["currentTurn"] != color:
            return [Command.error_msg("Cannot move when it is not your turn", "move", match_id)]

        if board[piece_pos.y][piece_pos.x].color.value != color:
            return [Command.error_msg("Cannot move opponent's pieces or empty squares", "move", match_id)]

        move_pos = notation_to_pos(move[2:])
        move_card = get_card_from_name(card_name)
        cards = get_cards_from_names(match["cards"][color])
        new_board: Optional[Board] = apply_move(piece_pos, move_pos, move_card, cards, board)

        if new_board is None:
            return [Command.error_msg("Invalid move", "move", match_id)]

        winner = check_win_condition(new_board)
        state = GameState.ENDED.value if winner != Player.NONE else GameState.IN_PROGRESS.value

        moves = match["moves"]
        moves.append(f"{card_name}:{move}")
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

        return [
            Message(
                {
                    "messageType": "move",
                    "matchId": match_id
                },
                True,
                match_id
            ),
            Message(
                Command.generate_state_dict(matches.find_one({"_id": object_id})),  # type: ignore
                False,
                match_id
            )
        ]
