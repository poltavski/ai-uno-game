import random
import requests
import json
from uuid import uuid4
from Card import Card, is_valid_move
from Node import Node

URL = "https://unoserver20210524144013.azurewebsites.net/api/"
headers = {
    "Content-type": "application/json",
    "Accept": "text/plain",
    "Content-Encoding": "utf-8",
}


def print_cards(cards):
    for card in cards:
        print(card)
    print("--------------------------------------")


class Player:
    def __init__(self, name, local: bool = False):
        self.name = name
        if not local:
            req = requests.post(
                URL + "Match/token", data=json.dumps({"name": name}), headers=headers
            )
            token = req.json()["token"]
        else:
            token = str(uuid4())
        self._token = token
        self.hand = []
        self.move = False

    def get_token(self):
        return self._token

    def set_hand(self, hand):
        for card in hand:
            if card is not None:
                self.hand.append(Card(card))

    def get_hand(self):
        return self.hand

    def print_hand(self):
        for card in self.hand:
            print(card)

    def clear_hand(self):
        self.hand.clear()

    def make_move(self, current_card, current_color, match_id, deck):
        root = Node(
            hand=self.hand,
            deck=deck,
            top=current_card,
            parent=None,
            lvl=0,
            estimation=0,
        )
        root.set_estimation()

        lvl_1 = []
        for card in self.hand:
            current_hand = self.hand
            current_hand.remove(card)
            if is_valid_move(current_card, card):
                n = Node(current_hand, deck, card, root, 1, root.estimation)
                n.set_estimation()
                lvl_1.append(n)
                root.children.append(n)
                print(f"lvl_1 cards {' | '.join(lvl_1)}")
        lvl_2 = []
        for node in lvl_1:
            for card in deck:
                current_deck = deck
                current_deck.remove(card)
                if is_valid_move(node.top, card):
                    n = Node(hand=current_deck, deck=node.hand, top=card, parent=node, lvl=2, estimation=node.estimation)
                    n.set_estimation()
                    lvl_2.append(n)
                    node.children.append(n)
                    print(f"lvl_2 cards {' | '.join(lvl_2)}")

        cards = [get_max_estimation_card(lvl_2) if len(lvl_2) > 0 else []]
        try:
            if cards[0].type == 4 or cards[0].type == 5:
                current_color = get_max_valuable_color(self.hand)
            self.check_identity(cards)
            self.send_cards(cards, match_id, current_color)
            print_cards(cards)
        except AttributeError:
            self.send_cards([], match_id, current_color)

    def check_identity(self, cards):
        for card in self.hand:
            if cards[0] == card:
                cards.append(card)
                self.hand.remove(card)

    def send_cards(self, cards, match_id, color):
        sending_cards = []
        for card in cards:
            sending_cards.append(card.to_json())
        requests.post(
            URL + "Game/move",
            data=json.dumps(
                {
                    "token": self._token,
                    "matchId": match_id,
                    "cards": sending_cards,
                    "color": color,
                }
            ),
            headers=headers,
        )


def get_max_estimation_card(leafs):
    node = leafs[0]
    for leaf in leafs:
        if leaf.estimation > node.estimation:
            node = leaf
    return node.parent.top


def get_max_valuable_color(hand):
    colors = {0: 0, 1: 0, 2: 0, 3: 0}

    for card in hand:
        colors[card.color] += 1

    values = [colors[0], colors[1], colors[2], colors[3]]
    value = max(values)
    for i in range(len(colors)):
        if value == colors[i]:
            return i

    # def make_move(self, current_card, current_color, match_id):
    #     cards = []
    #     number = current_card.number_value
    #     color = current_card.color
    #     if self.check_number(cards, number):
    #         self.check_identity(cards)
    #         self.send_cards(cards, match_id, current_color)
    #         print_cards(cards)
    #         return
    #     if self.check_color(cards, color):
    #         self.check_identity(cards)
    #         self.send_cards(cards, match_id, current_color)
    #         print_cards(cards)
    #         return
    #     if self.check_action(cards):
    #         self.check_identity(cards)
    #         self.send_cards(cards, match_id, random.randint(0, 3))
    #         print_cards(cards)
    #         return
    #     self.send_cards(cards, match_id, current_color)
    #
    # def check_number(self, cards, number):
    #     for card in self.hand:
    #         if card.number_value == number and card.type == 0:
    #             cards.append(card)
    #             self.hand.remove(card)
    #             return True
    #     return False
    #
    # def check_color(self, cards, color):
    #     for card in self.hand:
    #         if card.color == color and card.type != 4 and card.type != 5:
    #             cards.append(card)
    #             self.hand.remove(card)
    #             return True
    #     return False
    #
    # def check_action(self, cards):
    #     for card in self.hand:
    #         if card.type == 4 or card.type == 5:
    #             cards.append(card)
    #             self.hand.remove(card)
    #             return True
    #     return False
    #
