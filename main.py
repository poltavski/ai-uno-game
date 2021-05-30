from Card import Card
from Game import Game
from Player import Player
import logging
lg = logging.getLogger(__name__)
lg.setLevel("INFO")

if __name__ == "__main__":
    name1 = "Arch"
    name2 = "Alex"
    player = Player("Arch")
    opp = Player("Alex")
    lg.info(f"Players created {name1} vs {name2}")
    # print('My token: ', player.get_token())
    # opp = input('Input UID of your opponent: ')
    game = Game(player, opp.get_token())
    game.start()
    lg.info(f"Game started")
    while True:
        player.clear_hand()

        game.get_board()

        curr_card = game.current_card
        curr_color = game.current_color
        if game.status == 1:
            print("Congrats! You win!")
            break
        if game.status == 2:
            print("Not today :(")
            break
        if player.move:
            print(player.print_hand())
            print("--------------------------------------")
            print("Current card: ", curr_card)
            print("--------------------------------------")
            print("Current color: ", curr_color)
            print("--------------------------------------")
            print("My turn: ", player.move)
            print("--------------------------------------")
            player.make_move(
                curr_card, curr_color, game.get_match_id(), game.current_deck
            )
        # elif opp.move:
        #     print(opp.print_hand())
        #     print("--------------------------------------")
        #     print("Current card: ", curr_card)
        #     print("--------------------------------------")
        #     print("Current color: ", curr_color)
        #     print("--------------------------------------")
        #     print("My turn: ", player.move)
        #     print("--------------------------------------")
        #     player.make_move(
        #         curr_card, curr_color, game.get_match_id(), game.current_deck
        #     )
