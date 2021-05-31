from Card import Card
from Game import Game
from Player import Player
from copy import deepcopy
import logging
lg = logging.getLogger(__name__)
lg.setLevel("INFO")

colors = ["Red", "Green", "Blue", "Yellow"]

if __name__ == "__main__":
    name1 = "Albert Einstein"
    name2 = "Richard Feinman"
    player = Player(name1)
    opponent = Player(name2)
    print(f"Players created {name1} vs {name2}")

    game = Game(player, opponent)
    player.hand = [game.pick_card() for i in range(7)]
    # cards = [f"{p_card.type}-{p_card.color}-{p_card.number_value}" for p_card in player.hand]
    # print(cards)
    opponent.hand = [game.pick_card() for i in range(7)]
    # cards = [f"{p_card.type}-{p_card.color}-{p_card.number_value}" for p_card in opponent.hand]
    # print(cards)
    game.pick_card(first=True)
    print(f"Game started, id: {game.match_id}")
    player.print_hand()
    opponent.print_hand()
    steps = 0
    while True:
        steps += 1
        active_player, passive_player = (player, opponent) if game.move_id == player.id else (opponent, player)
        game_copy = deepcopy(game)
        game_copy.deck.extend(passive_player.hand)
        print(f"________________ \n {steps}: active is - {active_player.name}")
        print(f"Current card = {game.current_card}")
        cards, color, status = active_player.make_move(game_copy)
        player.print_hand()
        opponent.print_hand()
        if cards:
            current_move_str = f"Played card {cards[0].__str__()}"
            if color:
                current_move_str += f": {colors[color]}"
            print(current_move_str)
        else:
            if color:
                current_move_str = f"Player picked color card = {colors[color]}"
                print(current_move_str)
        # print(color, status)
        if len(active_player.hand) + len(passive_player.hand) == 108:
            print("All cards has been deployed in a game. Game over")
            break
        if status or len(active_player.hand) == 0:
            print(f"Winner name: {active_player.name}")
            break
        elif len(passive_player.hand) == 0:
            print(f"Winner name: {passive_player.name}")
            break
        game.step(active_player, passive_player, cards, color)
        print(f"player cards left: {len(player.hand)} vs {len(opponent.hand)}")
        # if game.status:
        #     winner = player if player.id == game.status else opponent
        #     print(f"Winner name: {winner.name}")
        #     break
