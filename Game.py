import requests
import json

from typing import List

import Player
from Card import Card, Color, is_valid_move
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
        self.match_id = str(uuid4())
        self.status = 0
        self.current_color = 0
        self.move_id = player.id
        self.history = []

    def pick_card(self, first: bool = False):
        deck_cards_left = len(self.deck)
        print(f"Deck cards left: {deck_cards_left}")
        if deck_cards_left == 0:
            print("FULLFIL DECK WITH HISTORY")
            self.deck = self.history
            self.history = []
        picked_card = self.deck[random.randint(0, len(self.deck)-1)]
        try:
            self.deck.remove(picked_card)
            self.history.append(picked_card)
            self.current_deck = self.deck
            if first:
                self.current_card = picked_card
                self.current_color = picked_card.color
            else:
                return picked_card
        except Exception as e:
            print(e)

    def step(self, player: Player, passive_player: Player, cards: List[Card], color):
        card_to_beat = self.current_card
        # process case where card_to_beat is None
        self.move_id = passive_player.id
        if cards:
            # Card can be beaten
            self.current_card = cards[0]
            self.current_color = color
            # picked_card = self.pick_card()
            # player.hand.append(picked_card)
        else:
            print(f"Can't beat {card_to_beat.__str__()} with hand cards.")
            # Analyze card which cannot be beaten
            picked_card = self.pick_card()
            print(f"Picking: {picked_card.__str__()}")
            beaten = is_valid_move(card_to_beat, picked_card)
            if beaten:
                print(f"Card Changed: {card_to_beat.__str__()} -> {picked_card.__str__()}")
                self.current_card = picked_card
                self.current_color = picked_card.color
            else:
                print(f"Can't beat {card_to_beat.__str__()}")
                player.hand.append(picked_card)
                if card_to_beat.type == 2:
                    # «Пропусти ход» — следующий игрок пропускает свой ход
                    self.move_id = player.id
                    # Reset card type to process infinite loop
                    self.current_card.type = 0
                elif card_to_beat.type == 3:
                    print("Picking 1 more card")
                    picked_card = self.pick_card()
                    player.hand.append(picked_card)
                    # Reset card type to process infinite loop
                    self.current_card.type = 0
                elif card_to_beat.type == 4:
                    print("Picking 3 more cards")
                    for i in range(3):
                        picked_card = self.pick_card()
                        player.hand.append(picked_card)
                    # Reset card type to process infinite loop
                    self.current_card.type = 0


    def get_match_id(self):
        return self.match_id
