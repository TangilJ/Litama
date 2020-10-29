from typing import List

from structures import Card, Pos, Player

# From https://uploads.johnhqld.com/uploads/20180926171936/Onitama-Cards-1024x576.jpg

RABBIT = Card("rabbit", Player.BLUE, [Pos(-1, -1), Pos(1, 1), Pos(2, 0)])
MONKEY = Card("monkey", Player.BLUE, [Pos(-1, -1), Pos(-1, 1), Pos(1, -1), Pos(1, 1)])
BOAR = Card("boar", Player.RED, [Pos(1, 0), Pos(-1, 0), Pos(0, 1)])
GOOSE = Card("goose", Player.BLUE, [Pos(-1, 0), Pos(-1, 1), Pos(1, 0), Pos(1, -1)])
COBRA = Card("cobra", Player.RED, [Pos(-1, 0), Pos(1, 1), Pos(1, -1)])
CRAB = Card("crab", Player.BLUE, [Pos(0, 1), Pos(-2, 0), Pos(2, 0)])
HORSE = Card("horse", Player.RED, [Pos(0, 1), Pos(-1, 0), Pos(0, -1)])
DRAGON = Card("dragon", Player.RED, [Pos(-1, -1), Pos(1, -1), Pos(-2, 1), Pos(2, 1)])
ROOSTER = Card("rooster", Player.RED, [Pos(-1, 0), Pos(1, 0), Pos(1, 1), Pos(-1, -1)])
CRANE = Card("crane", Player.BLUE, [Pos(-1, -1), Pos(1, -1), Pos(0, 1)])
ELEPHANT = Card("elephant", Player.RED, [Pos(-1, 0), Pos(1, 0), Pos(-1, 1), Pos(1, 1)])
MANTIS = Card("mantis", Player.RED, [Pos(-1, 1), Pos(1, 1), Pos(0, -1)])
TIGER = Card("tiger", Player.BLUE, [Pos(0, 2), Pos(0, -1)])
FROG = Card("frog", Player.RED, [Pos(-1, 1), Pos(1, -1), Pos(-2, 0)])
OX = Card("ox", Player.BLUE, [Pos(0, 1), Pos(0, -1), Pos(1, 0)])
EEL = Card("eel", Player.BLUE, [Pos(1, 0), Pos(-1, 1), Pos(-1, -1)])

ALL_CARDS: List[Card] = [RABBIT, MONKEY, BOAR, GOOSE, COBRA, CRAB, HORSE, DRAGON, ROOSTER,
                         CRANE, ELEPHANT, MANTIS, TIGER, FROG, OX, EEL]
ALL_CARD_NAMES: List[str] = [i.name for i in ALL_CARDS]
