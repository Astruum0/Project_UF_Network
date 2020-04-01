from Uno_Class import Deck, Player


def Turn(current_player, turn):
    if current_player == 3 and turn == 1:
        return 0
    if current_player == 0 and turn == -1:
        return 3
    else:
        return current_player + turn


deck = Deck()
players = [Player(deck, i) for i in range(4)]
id_player = 0

while True:
    current_player = players[id_player]
    if current_player.blocked == False:
        print(f"\nPlayer {id_player+1} turn :\n")
        for i, carte in enumerate(current_player.hand):
            if len(carte) == 2:
                print(f"{i+1} : {carte[1]} {carte[0]}")
            else:
                print(f"{i+1} : {carte[0]}")
        if len(deck.current_card) == 2:
            print(
                f"\nCurrent card : {deck.current_card[1]} {deck.current_card[0]}"
            )
        else:
            print(
                f"\nCurrent card : {deck.current_card[0]}"
            )
        if len(deck.current_card) == 1:
            print(f"( Couleur : {deck.current_color} )")
        carte = input("\nCarte ? ")
        try:
            carte = current_player.hand[(int(carte) - 1)]
            current_player.Play(carte, deck, players)
            if len(current_player.hand) == 1:
                print(f"\nUno pour Joueur {id_player} !")
            elif len(current_player.hand) == 0:
                print(f"\nJoueur {id_player} a gagné !")
                break
            id_player = Turn(id_player, deck.turn)
        except:
            if carte == "":
                current_player.Draw(1)
                print(
                    f"\nPlayer {id_player+1} pioche 1 carte"
                )
                id_player = Turn(id_player, deck.turn)
            else:
                print("Rentrez un nombre valide")
    else:
        print(f"\nPlayer {id_player+1} est bloqué\n")
        current_player.blocked == False
        id_player = Turn(current_player, deck.turn)
