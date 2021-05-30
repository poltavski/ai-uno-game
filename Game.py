import requests
import json
from Card import Card, Color
import random
from uuid import uuid4

URL = "https://unoserver20210524144013.azurewebsites.net/api/"
headers = {
    "Content-type": "application/json",
    "Accept": "text/plain",
    "Content-Encoding": "utf-8",
}


def generate_deck():
    deck = []
    for color in Color:
        for i in range(10):
            card = Card({"type": 0, "numberValue": i, "color": color.value})
            deck.append(card)
            if i != 0:
                deck.append(card)

        reverse = Card({"type": 1, "numberValue": 0, "color": color.value})
        deck.append(reverse)
        deck.append(reverse)

        skip = Card({"type": 2, "numberValue": 0, "color": color.value})
        deck.append(skip)
        deck.append(skip)

        take_two = Card({"type": 3, "numberValue": 0, "color": color.value})
        deck.append(take_two)
        deck.append(take_two)

    choose_color = Card({"type": 4, "numberValue": 0, "color": 0})
    take_four = Card({"type": 5, "numberValue": 0, "color": 0})

    for i in range(4):
        deck.append(choose_color)
        deck.append(take_four)

    return deck


class Game:
    def __init__(self, player, opponent):
        self.deck = generate_deck()
        self.current_deck = []
        self.player = player
        self.opponent = opponent
        self.current_card = None
        self.__match_id = None
        self.status = 0
        self.current_color = 0

    def start(self, local: bool = False):
        if not local:
            req = requests.post(
                URL + "Match/start",
                data=json.dumps(
                    {"token": self.player.get_token(), "opponent": self.opponent}
                ),
                headers=headers,
            )
            self.__match_id = req.json()["matchId"]
        else:
            self.__match_id = str(uuid4())

    def get_board(self, local: bool = False):
        if self.__match_id is not None:
            if not local:
                req = requests.get(
                    URL + "Game/board",
                    params={"token": self.player.get_token(), "matchId": self.__match_id},
                )
                board = req.json()
                self.current_card = Card(board["currentCard"])
            else:
                self.current_card = self.deck[random.randint(0, 107)]

            try:
                self.deck.remove(self.current_card)
            except ValueError:
                pass
            self.current_deck = self.deck
            self.player.set_hand(board["hand"])
            for card in self.player.get_hand():
                try:
                    self.current_deck.remove(card)
                except ValueError:
                    pass
            self.status = board["status"]
            self.player.move = board["myMove"]
            self.current_color = board["currentColor"]
        else:
            print("Match not started")

    def verify_move(self, card: Card):
        pass

    def get_match_id(self):
        return self.__match_id
