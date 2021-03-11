from random import random
from secrets import token_hex
from typing import List

from pymongo.collection import Collection

from commands.command import Command
from commands.message import Message
from structures import GameState


class Create(Command):
    STARTS_WITH = "create "

    @staticmethod
    def apply_command(matches: Collection, query: str) -> List[Message]:
        username = query

        token: str = token_hex(32)
        color: str = "Blue"
        enemy: str = "Red"
        if random() < 0.5:
            color = "Red"
            enemy = "Blue"

        insert = {
            # Set both players to the same username while the second player connects.
            # This is to prevent the first player from bruteforcing matches to get the color
            # they want while still allowing spectators to see who the first player is.
            "usernames": {
                "blue": username,
                "red": username
            },
            # To keep track of which side they will be on without name-checking, we need to
            # send their index as well.
            "indices": {
                "blue": 0,
                "red": 0
            },
            f"token{color}": token,
            f"token{enemy}": "",
            "gameState": GameState.WAITING_FOR_PLAYER.value
        }
        match_id = str(matches.insert_one(insert).inserted_id)

        return [
            Message(
                {
                    "messageType": "create",
                    "matchId": match_id,
                    "token": token,
                    "index": 0
                },
                True,
                match_id
            )
        ]


if __name__ == "__main__":
    print(Create.command_matches("create "))
