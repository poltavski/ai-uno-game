import random
import requests
import json
from treelib import Node as node_p, Tree

from copy import deepcopy
from uuid import uuid4
from Card import Card, is_valid_move
from Node import Node
import logging
lg = logging.getLogger(__name__)
lg.setLevel("INFO")


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
        self.id = str(uuid4())
        self.hand = []
        self.move = False

    def set_hand(self, hand):
        for card in hand:
            if card is not None:
                self.hand.append(Card(card))

    def get_hand(self):
        return self.hand

    def print_hand(self):
        hand_str = f"{self.name} = {len(self.hand)} cards : "
        for card in self.hand:
            hand_str += f"{card} | "
        print(hand_str)

    def clear_hand(self):
        self.hand.clear()


    def make_move(self, game, verbose: bool = True):
        root = Node(
            hand=self.hand,
            deck=game.deck,
            top=game.current_card,
            parent=None,
            lvl=0,
            estimation=0,
        )
        root.set_estimation()

        lvl_1 = []
        if verbose:
            print("lvl1 cards:")
            cur_card = f"+{game.current_card.__str__()} / est: {root.estimation}"
            # print(cur_card)
            tree = Tree()
            tree.create_node(cur_card, cur_card)
            # tree.show()
            tree_dict = {}
        hand_copy = deepcopy(self.hand)
        for i, card in enumerate(hand_copy):
            current_hand = deepcopy(self.hand)
            current_hand.remove(card)
            if is_valid_move(game.current_card, card):
                n = Node(current_hand, game.deck, card, root, 1, root.estimation)
                n.set_estimation()

                # print(f"{game.current_card}")
                if verbose:
                    main_card = f"{i}] {card.__str__()} / est: {n.estimation}"
                    tree.create_node(main_card, main_card, parent=cur_card)
                    if tree_dict.get(card.__str__()):
                        tree_dict[card.__str__()].append(main_card)
                    tree_dict[card.__str__()] = [main_card]
                lvl_1.append(n)
                root.children.append(n)
        lvl_2 = []
        # lg.info("lvl1 cards")
        tree_met = {}
        for node in lvl_1:
            top_card = node.top.__str__()
            for j, card in enumerate(game.deck):
                current_deck = game.deck
                current_deck.remove(card)
                if is_valid_move(node.top, card):
                    n = Node(hand=current_deck, deck=node.hand, top=card, parent=node, lvl=2, estimation=node.estimation)
                    n.set_estimation()
                    if verbose:
                        if not tree_met.get(top_card):
                            tree_met[top_card] = 0
                        else:
                            tree_met[top_card] = 1
                        tree.create_node(f"{j}) {card.__str__()}", f"{j}) {card.__str__()}", parent=tree_dict[top_card][tree_met[top_card]])

                    # print(f"{card}")
                    lvl_2.append(n)
                    node.children.append(n)

        if verbose:
            tree.show()
        cards = [get_max_estimation_card(lvl_2)] if len(lvl_2) > 0 else []
        current_color = None
        status = 0
        if cards:
            print(f"max estimated card: {cards[0].__str__()}")
            if cards[0].type == 4 or cards[0].type == 5:
                current_color = self.get_max_valuable_color()
            self.check_identity(cards)
            status = 1 if self.hand == [] else 0
        return cards, current_color, status

    def check_identity(self, cards):
        for card in self.hand:
            if cards[0] == card:
                cards.append(card)
                self.hand.remove(card)


    def get_max_valuable_color(self):
        colors = {0: 0, 1: 0, 2: 0, 3: 0}

        for card in self.hand:
            colors[card.color] += 1

        values = [colors[0], colors[1], colors[2], colors[3]]
        value = max(values)
        for i in range(len(colors)):
            if value == colors[i]:
                return i

def get_max_estimation_card(leafs):
    node = leafs[0]
    for leaf in leafs:
        if leaf.estimation > node.estimation:
            node = leaf
    return node.parent.top




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
