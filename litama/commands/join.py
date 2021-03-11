from secrets import token_hex
from typing import List, Union

from pymongo.collection import Collection

from commands.command import Command
from commands.message import Message
from conversions import board_to_str
from game import init_game
from structures import GameState, Player
from bson import ObjectId


class Join(Command):
    STARTS_WITH = "join "

    @staticmethod
    def apply_command(matches: Collection, query: str) -> List[Message]:
        split = query.split(" ")
        match_id = split[0]

        check: Union[Message, ObjectId] = Command.check_match_id(match_id, "join")
        if isinstance(check, Message):
            return [check]

        object_id = check
        username = " ".join(split[1:])
        match = matches.find_one({"_id": object_id})
        if match is None:
            return [Command.error_msg("Match not found", "join", match_id)]
        if match["gameState"] != GameState.WAITING_FOR_PLAYER.value:
            return [Command.error_msg("Not allowed to join", "join", match_id)]

        token: str = token_hex(32)
        color: str = "red" if match["tokenRed"] == "" else "blue"
        board, blue_cards, red_cards, side_card = init_game()
        usernames = match["usernames"]
        usernames[color] = username
        indices = match["indices"]
        indices[color] = 1

        matches.find_one_and_update(
            {"_id": object_id},
            {"$set": {
                f"token{color.title()}": token,
                "usernames": usernames,
                "indices": indices,
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

        return [
            Message(
                {
                    "messageType": "join",
                    "matchId": match_id,
                    "token": token,
                    "index": 1
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
