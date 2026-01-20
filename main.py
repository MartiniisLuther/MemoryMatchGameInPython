from game_logic.engine import MemoryGame
import tkinter as tk

def main():
    """Starts the application."""
    root = tk.Tk()
    root.title("Memory Battle")
    root.geometry("800x800")

    # Initialize the game class
    app = MemoryGame(root)

    root.mainloop()

# Ensures game only starts if main.py is run directly
if __name__ == "__main__":
    main()