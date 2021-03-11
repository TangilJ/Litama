from typing import List, Union

from pymongo.collection import Collection

from commands.command import Command
from commands.message import Message
from bson import ObjectId


class State(Command):
    STARTS_WITH = "state "

    @staticmethod
    def apply_command(matches: Collection, query: str) -> List[Message]:
        match_id = query

        check: Union[Message, ObjectId] = Command.check_match_id(match_id, "state")
        if isinstance(check, Message):
            return [check]

        object_id = check
        match = matches.find_one({"_id": object_id})
        if match is None:
            return [Command.error_msg("Match not found", "state", match_id)]

        return [
            Message(
                Command.generate_state_dict(match),
                True,
                match_id
            )
        ]
