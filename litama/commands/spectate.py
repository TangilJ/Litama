from typing import List, Union

from pymongo.collection import Collection

from commands.command import Command
from commands.message import Message
from structures import GameState
from bson import ObjectId


class Spectate(Command):
    STARTS_WITH = "spectate "

    @staticmethod
    def apply_command(matches: Collection, query: str) -> List[Message]:
        match_id = query

        check: Union[Message, ObjectId] = Command.check_match_id(match_id, "spectate")
        if isinstance(check, Message):
            return [check]

        object_id = check
        match = matches.find_one({"_id": object_id})
        if match is None:
            return [Command.error_msg("Match not found", "spectate", match_id)]
        if match["gameState"] == GameState.ENDED.value:
            return [Command.error_msg("Game ended", "spectate", match_id)]

        return [
            Message(
                {
                    "messageType": "spectate",
                    "matchId": match_id
                },
                True,
                match_id,
                True
            ),
            Message(
                Command.generate_state_dict(matches.find_one({"_id": object_id})),  # type: ignore
                False,
                match_id
            )
        ]
