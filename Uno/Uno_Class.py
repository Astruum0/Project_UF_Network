from random import shuffle
from copy import deepcopy


class Deck:
    def __init__(self):
        self.couleurs = ["Jaune", "Vert", "Rouge", "Bleu"]
        self.valeurs = [i for i in range(1, 10)]
        self.valeur_spec = ["+2", "Inversement", "Stop"]
        self.valeur_unique = ["Joker", "+4"]
        self.current_card = None
        self.current_color = None
        self.defausse = []
        self.turn = 1
        self.Make_Deck()

    def Make_Deck(self):
        self.deck = [
            (couleur, valeur)
            for couleur in self.couleurs
            for valeur in self.valeurs
            for i in range(2)
        ]
        self.deck += [
            (couleur, valeur)
            for couleur in self.couleurs
            for valeur in self.valeur_spec
            for i in range(2)
        ]
        self.deck += [
            (valeur,)
            for valeur in self.valeur_unique
            for i in range(4)
        ]
        shuffle(self.deck)

        while (
            self.deck[0][len(self.deck[0]) - 1]
            not in self.valeurs
        ):
            shuffle(self.deck)
        self.current_card = self.deck.pop(0)


class Player:
    def __init__(self, deck, id):
        self.id = id
        self.hand = [deck.deck.pop(0) for i in range(2)]
        self.play = False
        self.blocked = False

    def Play(self, card, deck, players):
        if self.Check(
            card, deck.current_card, deck.current_color
        ):
            if len(card) == 2:
                print(
                    f"\n{carte[1]} {carte[0]} a ete joué\n"
                )
                if deck.current_card != None:
                    deck.defausse.append(deck.current_card)
                if card[1] not in deck.valeurs:
                    self.Effect(
                        card[1], players, self.id, deck
                    )
                deck.current_card = self.hand.pop(
                    self.hand.index(card)
                )
            else:
                choosen_color = None
                while choosen_color == None:
                    couleur = (
                        input("Couleur choisi ? ")
                        .lower()
                        .capitalize()
                    )
                    if couleur in deck.couleurs:
                        choosen_color = couleur
                deck.current_color = choosen_color
                if deck.current_card != None:
                    deck.defausse.append(deck.current_card)
                if card[0] == "+4":
                    self.Effect(
                        "+4", players, self.id, deck
                    )
                deck.current_card = self.hand.pop(
                    self.hand.index(card)
                )
        else:
            print(f"{carte} n'a pas pu etre joué")

    def Check(self, card, current_card, current_color):
        if len(card) == 2:
            if len(current_card) == 2:
                if (
                    card[0] == current_card[0]
                    or card[1] == current_card[1]
                ):
                    return True
                else:
                    return False
            else:
                if card[0] == current_color:
                    return True
                else:
                    return False
        else:
            return True

    def Draw(self, number):
        for i in range(number):
            self.hand.append(deck.deck.pop(0))
            if len(deck.deck) == 0:
                deck.deck = deepcopy(deck.defausse)
                deck.defausse = []

    def Effect(self, effect, players, id, deck):
        next_player = players[Turn(id, deck.turn)]
        if effect == "+4":
            next_player.Draw(4)
            next_player.blocked = True
            print(
                f"Joueur {next_player.id} pioche 4 cartes"
            )
        if effect == "+2":
            next_player.Draw(2)
            next_player.blocked = True
            print(
                f"Joueur {next_player.id} pioche 2 cartes"
            )
        if effect == "Inversement":
            print("L'ordre de jeu est inversé !")
            deck.turn *= -1
        if effect == "Stop":
            next_player.blocked = True
