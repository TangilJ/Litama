from typing import List, Dict, Union

import bson
from bson import ObjectId

from commands.message import Message
from structures import GameState


class Command:
    STARTS_WITH = ""

    @classmethod
    def command_matches(cls, query: str) -> bool:
        return query.startswith(cls.STARTS_WITH)

    @staticmethod
    def apply_command(matches, query: str) -> List[Message]:
        pass

    @staticmethod
    def error_msg(error: str, attempted_query: str, match_id="") -> Message:
        return Message(
            {
                "messageType": "error",
                "matchId": match_id,
                "error": error,
                "command": attempted_query
            },
            True,
            match_id
        )

    @staticmethod
    def check_match_id(match_id: str, message_type: str) -> Union[Message, ObjectId]:
        try:
            return ObjectId(match_id)
        except bson.errors.InvalidId:
            return Command.error_msg("matchId was in an incorrect format", message_type, match_id)

    @staticmethod
    def generate_state_dict(match: Dict) -> Dict:
        if match["gameState"] == GameState.WAITING_FOR_PLAYER.value:
            return {
                "messageType": "state",
                "matchId": str(match["_id"]),
                "gameState": match["gameState"],
                "usernames": match["usernames"]
            }

        return {
            "messageType": "state",
            "usernames": match["usernames"],
            "indices": match["indices"],
            "matchId": str(match["_id"]),
            "currentTurn": match["currentTurn"],
            "cards": match["cards"],
            "startingCards": match["startingCards"],
            "moves": match["moves"],
            "board": match["board"],
            "gameState": match["gameState"],
            "winner": match["winner"]
        }
