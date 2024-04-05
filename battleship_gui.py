import tkinter as tk
import random

GRID_SIZE = 9

# Defining classes for different types of ships
class Ship:
    def __init__(self, size):
        self.size = size
        self.hits = 0

    def is_sunk(self):
        return self.hits == self.size

class Battleship(Ship):
    def __init__(self):
        super().__init__(4)

class Cruiser(Ship):
    def __init__(self):
        super().__init__(3)

class Destroyer(Ship):
    def __init__(self):
        super().__init__(2)

class Submarine(Ship):
    def __init__(self):
        super().__init__(1)

# Defining the game board
class GameBoard:
    def __init__(self):
        self.grid = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.remaining_ships = 0

    def is_valid_position(self, x, y):
        return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE

    def place_ship(self, ship, x, y, direction):
        if not self.is_valid_position(x, y):
            return False
        if direction == 'horizontal':
            if x + ship.size > GRID_SIZE:
                return False  
            for i in range(ship.size):
                if self.grid[y][x + i] is not None:
                    return False  
            for i in range(ship.size):
                self.grid[y][x + i] = ship
        elif direction == 'vertical':
            if y + ship.size > GRID_SIZE:
                return False  
            for i in range(ship.size):
                if self.grid[y + i][x] is not None:
                    return False  
            for i in range(ship.size):
                self.grid[y + i][x] = ship
        self.remaining_ships += 1
        return True

    def attack(self, x, y):
        if not self.is_valid_position(x, y):
            return False  
        if self.grid[y][x] is None:
            return False 
        else:
            ship = self.grid[y][x]
            ship.hits += 1
            if ship.is_sunk():
                print("You sunk a ship!")
                self.remaining_ships -= 1
            return True  

    def game_over(self):
        return self.remaining_ships == 0

# Defining the graphical user interface for the game
class BattleshipGUI:
    def __init__(self, master):
        self.master = master
        self.game_board = GameBoard()
        self.place_ships()
        self.create_board()

    def create_board(self):
        # To create buttons for each cell in the grid
        button_size = 40 
        self.buttons = []
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                button = tk.Button(self.master, width=button_size, height=button_size, command=lambda x=i, y=j: self.attack(x, y))
                button.grid(row=i, column=j, sticky='nsew')
                row.append(button)
            self.buttons.append(row)
        for i in range(GRID_SIZE):
            self.master.grid_rowconfigure(i, weight=1)
            self.master.grid_columnconfigure(i, weight=1)

    def place_ships(self):
        ships = [Battleship(), Cruiser(), Cruiser(), Destroyer(), Destroyer(), Submarine(), Submarine(), Submarine()]
        directions = ['horizontal', 'vertical']
        for ship in ships:
            placed = False
            while not placed:
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                direction = random.choice(directions)
                placed = self.game_board.place_ship(ship, x, y, direction)

    def attack(self, x, y):
        # Handling player's attack on the grid
        if self.game_board.attack(x, y):
            self.buttons[x][y].config(bg='red')
        else:
            self.buttons[x][y].config(bg='blue')

        if self.game_board.game_over():
            if self.game_board.remaining_ships == 0:
                print("Congratulations! You won the game!")
            else:
                print("Game over! You lost the game.")

    def start_game(self):
        self.master.mainloop()


# Main function to start the game
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Battleship")

    window_size = GRID_SIZE * 40  
    root.geometry(f"{window_size}x{window_size}")
    
    game = BattleshipGUI(root)
    root.mainloop()