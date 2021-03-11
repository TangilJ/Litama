from dataclasses import dataclass

from typing import Dict, Any


@dataclass
class Message:
    message: Dict[str, Any]
    reply_to_only_sender: bool
    match_id: str
    add_sender_to_spectate_map: bool = False
