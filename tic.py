import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import math

# -------------------- Main Window --------------------
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.geometry("500x600")
root.configure(bg="#1e1e1e")

# -------------------- Game Variables --------------------
board = []
buttons = []
grid_size = 3  # default grid size

player_symbol = 'X'
computer_symbol = 'O'

# -------------------- Game Functions --------------------
def start_game():
    global board, buttons, grid_size
    grid_size_input = simpledialog.askinteger("Grid Size", "Enter grid size (3-5 recommended):", minvalue=3, maxvalue=5)
    if grid_size_input:
        grid_size = grid_size_input
    board[:] = [' ' for _ in range(grid_size * grid_size)]
    
    # Clear previous buttons if any
    for widget in game_frame.winfo_children():
        widget.destroy()
    buttons.clear()
    
    # Create buttons
    for i in range(grid_size * grid_size):
        b = tk.Button(game_frame, text=' ', font=('Arial', 24, 'bold'), width=4, height=2,
                      bg="#2e2e2e", fg="white",
                      command=lambda i=i: player_move(i))
        b.grid(row=i//grid_size, column=i%grid_size, padx=5, pady=5, sticky="nsew")
        buttons.append(b)
    
    # Make grid cells expand evenly
    for i in range(grid_size):
        game_frame.grid_rowconfigure(i, weight=1)
        game_frame.grid_columnconfigure(i, weight=1)

def player_move(pos):
    if board[pos] != ' ':
        return
    board[pos] = player_symbol
    buttons[pos].config(text=player_symbol, fg="#00ff00")
    
    if check_winner(player_symbol):
        messagebox.showinfo("Tic-Tac-Toe", "Congratulations! You won!")
        reset_game()
        return
    if ' ' not in board:
        messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
        reset_game()
        return
    
    # Computer move
    root.after(300, computer_move)

# -------------------- AI Functions --------------------
def computer_move():
    if grid_size == 3:
        best_score = -math.inf
        best_move = None
        for i in range(9):
            if board[i] == ' ':
                board[i] = computer_symbol
                score = minimax(board, 0, False)
                board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
    else:
        # For larger grids, simple strategy: win/block
        best_move = find_best_move()
    
    board[best_move] = computer_symbol
    buttons[best_move].config(text=computer_symbol, fg="#ff4444")
    
    if check_winner(computer_symbol):
        messagebox.showinfo("Tic-Tac-Toe", "Computer Wins! Better luck next time.")
        reset_game()
        return
    if ' ' not in board:
        messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
        reset_game()
        return

def minimax(b, depth, is_maximizing):
    if check_winner_static(b, computer_symbol):
        return 1
    elif check_winner_static(b, player_symbol):
        return -1
    elif ' ' not in b:
        return 0
    
    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if b[i] == ' ':
                b[i] = computer_symbol
                score = minimax(b, depth+1, False)
                b[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if b[i] == ' ':
                b[i] = player_symbol
                score = minimax(b, depth+1, True)
                b[i] = ' '
                best_score = min(score, best_score)
        return best_score

def find_best_move():
    # Simple AI for larger grids
    empty = [i for i, spot in enumerate(board) if spot == ' ']
    # Try winning move
    for move in empty:
        board[move] = computer_symbol
        if check_winner(computer_symbol):
            board[move] = ' '
            return move
        board[move] = ' '
    # Try block player's winning move
    for move in empty:
        board[move] = player_symbol
        if check_winner(player_symbol):
            board[move] = ' '
            return move
        board[move] = ' '
    # Otherwise random
    return random.choice(empty)

# -------------------- Check Winner --------------------
def check_winner(symbol):
    return check_winner_static(board, symbol)

def check_winner_static(b, symbol):
    # Check rows
    for r in range(grid_size):
        if all(b[r*grid_size + c] == symbol for c in range(grid_size)):
            return True
    # Check columns
    for c in range(grid_size):
        if all(b[r*grid_size + c] == symbol for r in range(grid_size)):
            return True
    # Check diagonals
    if all(b[i*(grid_size+1)] == symbol for i in range(grid_size)):
        return True
    if all(b[(i+1)*(grid_size-1)] == symbol for i in range(grid_size)):
        return True
    return False

# -------------------- Reset Game --------------------
def reset_game():
    global board
    board = [' ' for _ in range(grid_size * grid_size)]
    for b in buttons:
        b.config(text=' ', fg="white")

# -------------------- UI Layout --------------------
title_label = tk.Label(root, text="Tic-Tac-Toe", font=("Arial", 28, "bold"), bg="#1e1e1e", fg="white")
title_label.pack(pady=20)

game_frame = tk.Frame(root, bg="#1e1e1e")
game_frame.pack(expand=True, fill="both", padx=20, pady=20)

start_btn = tk.Button(root, text="Start New Game", font=("Arial", 18), bg="#00aaff", fg="white",
                      command=start_game)
start_btn.pack(pady=20)

root.mainloop()
