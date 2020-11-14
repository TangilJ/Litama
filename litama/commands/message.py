from dataclasses import dataclass


@dataclass
class Message:
    message: dict
    reply_to_only_sender: bool
    match_id: str
    add_sender_to_spectate_map: bool = False
