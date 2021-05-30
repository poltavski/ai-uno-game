class Node:
    def __init__(self, hand, deck, top, parent, lvl, estimation):
        self.hand = hand
        self.deck = deck
        self.top = top
        self.parent = parent
        self.lvl = lvl
        self.children = []
        self.estimation = estimation

    def set_estimation(self):
        h = 0
        top = self.top
        hand = self.hand

        for card in hand:
            if card.type == 0 and (
                card.number_value == top.number_value or card.color == top.color
            ):
                h += 1
            if (card.type == 1 or card.type == 2 or card.type == 3) and (
                top.color == card.color or top.type == card.type
            ):
                h += 2
            if card.type == 4 or card.type == 5:
                h += 3

        self.estimation += h if self.lvl % 2 == 1 else -h
