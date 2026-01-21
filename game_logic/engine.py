import tkinter as tk
from tkinter import messagebox
import random

class MemoryGame:
    """
    The main controller for the Memory Match game logic and UI.
    """

    def __init__(self, root):
        """
        Initialize the game state and build the UI.
        :param root: The Tkinter root window.
        """
        self.root = root
        self.root.configure(bg="#0f0f0f")

        self.flipped_indices = []

        # Game State Data
        self.player_turn = 1
        self.scores = {1: 0, 2: 0}
        self.cards = self._setup_cards()
        self.buttons = []

        self._build_ui()

    def _setup_cards(self):
        """Creates and shuffles the emoji pairs."""
        emojis = ['🍎', '🍎', '🚀', '🚀', '💎', '💎', '👾', '👾'] * 2
        random.shuffle(emojis)
        return emojis

    def _build_ui(self):
        """Constructs the visual grid of buttons and the side scoreboard."""
        # Main container using grid
        self.root.columnconfigure(0, weight=3) # Game area
        self.root.columnconfigure(1, weight=1) # Side panel

        # 1. Game Grid (left side)
        grid_frame = tk.Frame(self.root, bg="#0f0f0f")
        grid_frame.grid(row=0, column=0, padx=20, pady=20)

        for i in range(16):
            btn = tk.Button(grid_frame, text="?", width=6, height=3,
                            bg="#2c2c2c", fg="white", font=("Arial", 14, "bold"),
                            command=lambda i=i: self.on_card_click(i))
            btn.grid(row=i//4, column=i%4, padx=8, pady=8)
            self.buttons.append(btn)

        # 2. Side panel (right side)
        self.side_panel = tk.Frame(self.root, bg="#1a1a1a", width=200)
        self.side_panel.grid(row=0, column=1, sticky="nsew")

        self.score_label_1 = tk.Label(self.side_panel, text="P1: 0",
                                      fg="#4CC9FE", bg="#1a1a1a", font=("Arial", 16, "bold"))
        self.score_label_1.pack(pady=20)

        self.score_label_2 = tk.Label(self.side_panel, text="P2: 0", fg="white",
                                      bg="#1a1a1a", font=("Arial", 16, "bold"))
        self.score_label_2.pack(pady=20)

        self.turn_indicator = tk.Label(self.side_panel, text="Current Turn:\nPlayer 1", fg="#FFD700", bg="#1a1a1a")
        self.turn_indicator.pack(side="bottom", pady=20)

        # Add Reset Button
        self.reset_btn = tk.Button(self.side_panel, text="RESET GAME",
                                   command=self.reset_game, bg="#ff4e4e", fg="white",
                                   font=("Arial", 10, "bold"))
        self.reset_btn.pack(side="bottom", pady=20)

    def _update_score_ui(self):
        """Updates the labels to reflect current scores and turns."""
        self.score_label_1.config(text=f"P1: {self.scores[1]}", fg="#4CC9FE" if self.player_turn == 1 else "gray")
        self.score_label_2.config(text=f"P2: {self.scores[2]}", fg="#4CC9FE" if self.player_turn == 2 else "gray")
        self.turn_indicator.config(text=f"Current Turn:\nPlayer {self.player_turn}")


    def on_card_click(self, index):
        """Handles logic for flipping cards and checking matches."""
        # 1. Ignore if 2 cards are already being processed or if this card is already flipped
        if len(self.flipped_indices) >= 2 or self.buttons[index]["state"] == "disabled":
            return

        # 2. Reveal card
        self.buttons[index].config(text=self.cards[index], state="disabled", disabledforeground="white")
        self.flipped_indices.append(index)

        # 3. If two cards are flipped, check for a match
        if len(self.flipped_indices) == 2:
            self.root.after(600, self.check_match) # Wait 0.6 seconds so user can see the emoji


    def check_match(self):
        """Compares two flipped cards.

        If the cards match, increment the current player's score.
        Otherwise, flip the cards back and switch the turn.
        """
        idx1, idx2 = self.flipped_indices

        if self.cards[idx1] == self.cards[idx2]:
            # if Match!
            self.scores[self.player_turn] += 1
            # Keep buttons disabled but maybe change color to show they're 'done'
            self.buttons[idx1].config(bg="#005f00")
            self.buttons[idx2].config(bg="#005f00")
            # print(f"Match! Player {self.player_turn} score: {self.scores[self.player_turn]}")
        else:
            # Not a match - flip them back
            self.buttons[idx1].config(text="?", state="normal")
            self.buttons[idx2].config(text="?", state="normal")

            # Switch turns
            self.player_turn = 2 if self.player_turn == 1 else 1

        # Clear the "memory" for the next turn
        self.flipped_indices = []
        self._update_score_ui() # update the side panel

        # Check if all matches are found
        total_score = self.scores[1] + self.scores[2]
        if total_score == 8:
            self._announce_winner()


    def _announce_winner(self):
        """Determines the winner and shows a popup message"""
        if self.scores[1] > self.scores[2]:
            winner_text = f"Player 1 Wins! ({self.scores[1]}-{self.scores[2]}"
        elif self.scores[2] > self.scores[1]:
            winner_text = f"Player 2 Wins! ({self.scores[2]}-{self.scores[1]})"
        else:
            winner_text = f"It's a tie! ({self.scores[1]}-{self.scores[2]})"

        messagebox.showinfo("Game Over", winner_text)
        self.root.destroy() #close the game


    def reset_game(self):
        """Resets the game state to start a new round."""
        # 1. Reset data
        self.player_turn = 1
        self.scores = {1: 0, 2: 0}
        self.flipped_indices = []
        self.cards = self._setup_cards() # Re-shuffle

        # 2. Reset UI Buttons
        for btn in self.buttons:
            btn.config(text="?", state="normal", bg="#2c2c2c")

        # 3. Refresh Scoreboard
        self._update_score_ui()
