from random import random
from secrets import token_hex
from typing import List
from cards import ALL_BASE_CARD_NAMES
from conversions import get_card_from_name

from pymongo.collection import Collection

from commands.command import Command
from commands.message import Message
from structures import GameState


class CreateCustom(Command):
    STARTS_WITH = "create_custom "

    @staticmethod
    def apply_command(matches: Collection, query: str) -> List[Message]:
        split = query.split(" ", 1)
        chosen_player_color = split[0]
        color: str = "Blue"
        enemy: str = "Red"
        if chosen_player_color not in ["blue", "red"]:
            if random() < 0.5:
                color = "Red"
                enemy = "Blue"
            split = split[1].split(" ", 5)
        else:
            if chosen_player_color == "red":
                color = "Red"
                enemy = "Blue"
            split = query.split(" ", 5)

        card_names = split[0:5]
        username = split[5]

        card_names_checked = []
        for card_name in card_names:
            if card_name not in ALL_BASE_CARD_NAMES:
                return [Command.error_msg(f"Invalid card name '{card_name}'", "create_custom", match_id)]
            for existing_card in card_names_checked:
                if existing_card == card_name:
                    return [Command.error_msg(f"Duplicate card '{card_name}'", "create_custom", match_id)]
            card_names_checked.append(get_card_from_name(card_name))
        blue_cards, red_cards, side_card = card_names_checked[0:2], card_names_checked[2:4], card_names_checked[4]
                    

        token: str = token_hex(32)

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
            "cards": {
                "blue": [i.name for i in blue_cards],
                "red": [i.name for i in red_cards],
                "side": side_card.name
            },
            f"token{color}": token,
            f"token{enemy}": "",
            "gameState": GameState.WAITING_FOR_PLAYER.value
        }
        match_id = str(matches.insert_one(insert).inserted_id)

        return [
            Message(
                {
                    "messageType": "create_custom",
                    "matchId": match_id,
                    "token": token,
                    "index": 0
                },
                True,
                match_id
            )
        ]


if __name__ == "__main__":
    print(Create.command_matches("create_custom "))
