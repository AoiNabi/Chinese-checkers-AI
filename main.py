from threading import Thread
from time import sleep
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk

from checker_frame import CheckerFrame
from game_state import GameState


def centerWindow(window: tk.Tk, width=None, height=None) -> None:
    if width is None:
        width = window.winfo_reqwidth()
    if height is None:
        height = window.winfo_reqheight()

    positionRight = int(window.winfo_screenwidth()/2 - width/2)
    positionDown = int(window.winfo_screenheight()/2 - height/2)

    window.geometry("+{}+{}".format(positionRight, positionDown))


class MainProgram:
    def __init__(self) -> None:
        self.window = None
        self.newGameAsked = True
        self.initializeProgram()

    def initializeProgram(self) -> None:
        self.turn = 2

    def run(self) -> None:
        while self.newGameAsked:
            self.newGameAsked = False

            self.openLevelDialog()
            if self.levelDiff == 0:
                return

            self.window = tk.Tk()
            self.window.title("Chinese Checker")
            self.window.eval('tk::PlaceWindow . center')

            self.window.minsize(800, 600)

            self.checkers = CheckerFrame(self.window, background="white")

            self.checkers.canvas.gameState = GameState()
            self.checkers.canvas.playerCallback = self.playerCallback

            self.checkers.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

            self.turnLabel = ttk.Label(self.window)
            self.turnLabel.pack(side=tk.TOP, padx=28, pady=(28, 0))

            self.difficultyLabel = ttk.Label(self.window)
            self.difficultyLabel.pack(side=tk.TOP, padx=28, pady=10)

            newGameButton = ttk.Button(
                self.window, text="New game", command=self.newGame)
            newGameButton.pack(side=tk.TOP, padx=10, pady=(28, 0))

            centerWindow(self.window, 800, 600)
            self.updateDifficulty()
            self.updateTurn()
            self.window.mainloop()

    def newGame(self) -> None:
        self.initializeProgram()
        self.newGameAsked = True
        self.window.destroy()

    def openLevelDialog(self) -> None:
        dialog = tk.Tk()
        dialog.title("Choose a difficulty")

        dialog.minsize(200, 0)

        self.levelDiff = 0

        def close(r):
            self.levelDiff = r
            dialog.destroy()

        easy = ttk.Button(dialog, text="Easy", command=lambda: close(1))
        easy.pack(padx=10, pady=(10, 5))

        medium = ttk.Button(dialog, text="Medium", command=lambda: close(3))
        medium.pack(padx=10, pady=(10, 5))

        hard = ttk.Button(dialog, text="Hard", command=lambda: close(5))
        hard.pack(padx=10, pady=10)

        dialog.resizable(False, False)
        dialog.attributes('-toolwindow', True)
        centerWindow(dialog)
        dialog.mainloop()

    def updateDifficulty(self) -> None:
        if self.levelDiff == 1:
            self.difficultyLabel.config(text="Difficulty: Easy")
        elif self.levelDiff == 3:
            self.difficultyLabel.config(text="Difficulty: Medium")
        elif self.levelDiff == 5:
            self.difficultyLabel.config(text="Difficulty: Hard")

    def updateTurn(self) -> None:
        if self.turn == 1:
            self.turnLabel.config(text="AI turn")
            self.checkers.canvas.isClickable = False
        elif self.turn == 2:
            self.turnLabel.config(text="Your turn")
            self.checkers.canvas.isClickable = True

    def playerCallback(self) -> None:
        self.turn = 1
        self.updateTurn()
        self.checkWins()
        AiThread = Thread(target=self.AiThread)
        AiThread.start()

    def AiThread(self) -> None:
        gameState = self.checkers.canvas.gameState
        initial, next = gameState.alphaBetaSearch(self.levelDiff)
        if initial is not None and next is not None:
            self.checkers.canvas.gameState = gameState.moveMarble(
                initial, next)
            self.checkers.canvas.updateCircles()

        self.turn = 2
        self.updateTurn()
        self.checkWins()

    def checkWins(self) -> None:
        gameState = self.checkers.canvas.gameState
        win = gameState.winCondition()

        if win == 1:
            msg.showinfo("Lost", "The AI has won!")
            self.newGame()
        elif win == 2:
            msg.showinfo("Won", "You won!")
            self.newGame()


if __name__ == "__main__":
    MainProgram().run()
