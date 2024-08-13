import itertools
import random
import streamlit as st
import pandas as pd

# Snakes and ladders mapping
SNAKESANDLADDERS = {
    27: 7,
    35: 5,
    39: 3,
    50: 34,
    59: 46,
    66: 24,
    73: 12,
    76: 63,
    89: 67,
    97: 86,
    99: 26,
    2: 23,
    8: 29,
    22: 41,
    28: 77,
    30: 32,
    44: 58,
    54: 69,
    70: 90,
    80: 83,
    87: 93,
}

# Mapping for pawns (using different emoji for each player)
PAWNS = ["🔴", "🔵", "🟢", "🟡", "🟠", "🟣", "⚪", "⚫", "🟤", "🔶"]

class Dice:
    @staticmethod
    def roll():
        return random.randint(1, 6)

class Player:
    def __init__(self, name, pawn):
        self.name = name.capitalize()
        self.pawn = pawn
        self.position = 0
        self.born = False
        self.last_three_moves = [0, 0, 0]

    def has_won(self):
        return self.position == 100

    def update_position(self, dicevalue):
        self.last_three_moves.pop(0)
        self.last_three_moves.append(dicevalue)

        if self.last_three_moves == [6, 6, 6]:
            self.position = 0
            self.born = False
            return

        new_pos = self.position + dicevalue

        if new_pos >= 100:
            self.position = 100
            return
        else:
            self.position = new_pos

        while self.position in SNAKESANDLADDERS:
            self.position = SNAKESANDLADDERS[self.position]

    def play(self):
        dicevalue = Dice.roll()
        st.write(f"{self.name}: DICE SHOWS {dicevalue}")

        if dicevalue == 1:
            self.born = True

        if not self.born:
            st.write(f"{self.name}: player is not born yet")
        else:
            while True:
                self.update_position(dicevalue)
                st.write(f"{self.name} POSITION ==> {self.position}")
                if dicevalue != 6:
                    break
                else:
                    dicevalue = Dice.roll()

class Game:
    def __init__(self, players):
        self.players = itertools.cycle(players)
        self.num_players = len(players)
        self.mutable_players = itertools.cycle(players)

    def has_finished(self):
        for _ in range(self.num_players):
            player = next(self.mutable_players)
            if player.has_won():
                return True
        return False

    def next_player(self):
        return next(self.players)

def create_board():
    board = [str(i) for i in range(1, 101)]
    for key, value in SNAKESANDLADDERS.items():
        board[key - 1] = f"🐍{key}->{value}"
        board[value - 1] = f"🔼{value}<-{key}"
    return board

def display_board(players):
    board = create_board()

    # Place players' pawns on the board
    for player in players:
        if player.position > 0:
            board[player.position - 1] = player.pawn

    # Format the board into a 10x10 grid
    board_df = pd.DataFrame([board[i:i + 10] for i in range(0, 100, 10)])
    st.table(board_df)

def main():
    st.title("Snake and Ladder Game Simulation")

    if 'game' not in st.session_state:
        no_of_players = st.number_input("Enter the number of players:", min_value=1, max_value=10, value=2)
        player_names = st.text_input("Enter the names of players (separated by commas):").split(',')

        if st.button("Start Game"):
            players = [Player(name.strip(), PAWNS[i % len(PAWNS)]) for i, name in enumerate(player_names)]
            st.session_state.game = Game(players)
            st.session_state.players = players
            st.session_state.turns = []

    if 'game' in st.session_state:
        game = st.session_state.game
        players = st.session_state.players
        display_board(players)

        if st.button("Roll Dice"):
            player = game.next_player()
            player.play()
            display_board(players)
            if game.has_finished():
                st.write("Game Over!")
                for player in players:
                    if player.has_won():
                        st.write(f"{player.name} has won the game!")
                del st.session_state['game']
                del st.session_state['players']
                del st.session_state['turns']

if __name__ == "__main__":
    main()
