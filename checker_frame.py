import tkinter as tk

from game_state import GameState


def getPlayerColor(color: int) -> str:
    if color == 0:
        return 'white'
    elif color == 1:
        return '#FFB92A'
    elif color == 2:
        return '#1f2041'


class CheckerCanvas(tk.Canvas):
    gameState: GameState

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.gameState = None
        self.isClickable = False
        self.selected = None
        self.availableMoves = []
        self.circleMap = {}
        self.playerCallback = lambda: None
        self.bind("<Configure>", self.redraw)

    def redraw(self, event) -> None:
        self.delete("all")

        width = event.width
        height = event.height

        wInterval = width / 3
        hInterval = height / 4

        self.create_polygon(
            width / 2, 0,
            wInterval, hInterval,
            wInterval * 2, hInterval,
            fill="#FFD98E"
        )

        self.create_polygon(
            0, hInterval,
            wInterval, hInterval,
            wInterval / 2, hInterval * 2,
            fill="#4B3F72"
        )

        self.create_polygon(
            wInterval / 2, hInterval * 2,
            0, hInterval * 3,
            wInterval, hInterval * 3,
            fill="#119DA4"
        )

        self.create_polygon(
            wInterval, hInterval * 3,
            wInterval * 2, hInterval * 3,
            width / 2, height,
            fill="#4C4F9D"
        )

        self.create_polygon(
            wInterval * 2, hInterval * 3,
            width, hInterval * 3,
            wInterval * 5/2, hInterval * 2,
            fill="#4AAD52"
        )

        self.create_polygon(
            wInterval * 2, hInterval,
            width, hInterval,
            wInterval * 5/2, hInterval * 2,
            fill="#19647E"
        )

        self.create_line(
            width / 2, 0,
            0, hInterval * 3,
            width, hInterval * 3,
            width / 2, 0,
        )

        self.create_line(
            width / 2, height,
            0, hInterval,
            width, hInterval,
            width / 2, height,
        )

        linesY = height / 18
        linesX = width / 14

        for i in range(3):
            self.create_line(
                linesX * (7 - (i + 1) * 0.5), linesY * (i + 2),
                linesX * (7 + (i + 1) * 0.5), linesY * (i + 2)
            )

        for i in range(5):
            self.create_line(
                linesX * (1 + i * 0.5), linesY * (i + 5),
                linesX * (13 - i * 0.5), linesY * (i + 5)
            )

        for i in range(4):
            self.create_line(
                linesX * (1 + i * 0.5), linesY * (13 - i),
                linesX * (13 - i * 0.5), linesY * (13 - i)
            )

        for i in range(3):
            self.create_line(
                linesX * (7 - (i + 1) * 0.5), linesY * (16 - i),
                linesX * (7 + (i + 1) * 0.5), linesY * (16 - i)
            )

        for i in range(3):
            self.create_line(
                linesX * (i + 2), linesY * 5,
                linesX * (2 + (i - 1) * 0.5), linesY * (i + 6)
            )

        for i in range(5):
            self.create_line(
                linesX * (i * 0.5 + 7), linesY * (i + 1),
                linesX * (i + 1), linesY * 13
            )

        for i in range(4):
            self.create_line(
                linesX * (i + 10), linesY * 5,
                linesX * ((i * 0.5) + 5.5), linesY * (14 + i)
            )

        for i in range(3):
            self.create_line(
                linesX * (i + 10), linesY * 13,
                linesX * (12 + (i - 1) * 0.5), linesY * (10 + i)
            )

        for i in range(3):
            self.create_line(
                linesX * (12 - i), linesY * 5,
                linesX * (12 - (i - 1) * 0.5), linesY * (i + 6)
            )

        for i in range(5):
            self.create_line(
                linesX * (7 - i * 0.5), linesY * (i + 1),
                linesX * (13 - i), linesY * 13
            )

        for i in range(4):
            self.create_line(
                linesX * (i + 1), linesY * 5,
                linesX * ((i * 0.5) + 7), linesY * (17 - i)
            )

        for i in range(3):
            self.create_line(
                linesX * (i + 2), linesY * 13,
                linesX * (2 + (i - 1) * 0.5), linesY * (12 - i)
            )

        for i in range(4):
            for j in range(i + 1):
                self.circleMap[(j - i + 8, i - 4)] = self.create_oval(
                    linesX * (7 + j - i * 0.5) - linesX /
                    4, linesY * (i + 1) - linesX / 4,
                    linesX * (7 + j - i * 0.5) + linesX /
                    4, linesY * (i + 1) + linesX / 4,
                    fill=getPlayerColor(self.gameState.map[(j - i + 8, i - 4)])
                )

        for i in range(5):
            for j in range(13 - i):
                self.circleMap[(j, i)] = self.create_oval(
                    linesX * (1 + j + i * 0.5) - linesX /
                    4, linesY * (i + 5) - linesX / 4,
                    linesX * (1 + j + i * 0.5) + linesX /
                    4, linesY * (i + 5) + linesX / 4,
                    fill=getPlayerColor(self.gameState.map[(j, i)])
                )

        for i in range(4):
            for j in range(10 + i):
                self.circleMap[(j - i - 1, i + 5)] = self.create_oval(
                    linesX * (2.5 + j - i * 0.5) - linesX /
                    4, linesY * (i + 10) - linesX / 4,
                    linesX * (2.5 + j - i * 0.5) + linesX /
                    4, linesY * (i + 10) + linesX / 4,
                    fill=getPlayerColor(self.gameState.map[(j - i - 1, i + 5)])
                )

        for i in range(4):
            for j in range(4 - i):
                self.circleMap[(j, i + 9)] = self.create_oval(
                    linesX * (5.5 + j + i * 0.5) - linesX /
                    4, linesY * (14 + i) - linesX / 4,
                    linesX * (5.5 + j + i * 0.5) + linesX /
                    4, linesY * (14 + i) + linesX / 4,
                    fill=getPlayerColor(self.gameState.map[(j, i + 9)])
                )

        self.circles2Cords = {}
        for cords, circle in self.circleMap.items():
            self.circles2Cords[circle] = cords
            self.tag_bind(circle, '<Button-1>', self.click)

    def updateCircles(self) -> None:
        for cords, circle in self.circleMap.items():
            self.itemconfig(circle, fill=getPlayerColor(
                self.gameState.map[cords]))

    def click(self, event) -> None:
        if not self.isClickable:
            return

        clickedId = self.find_withtag("current")[0]
        cords = self.circles2Cords[clickedId]

        if self.selected is None or self.gameState.map[cords] == 2:
            if self.gameState.map[cords] != 2:
                return

            self.selected = cords
            self.availableMoves = self.gameState.getMarbleMoves(cords)
            self.updateCircles()
            for moveCords in self.availableMoves:
                self.itemconfig(self.circleMap[moveCords], fill='#9697bf')

        else:
            moved = False
            if cords in self.availableMoves:
                self.gameState = self.gameState.moveMarble(
                    self.selected, cords)
                moved = True

            self.selected = None
            self.availableMoves.clear()
            self.updateCircles()
            if moved:
                self.playerCallback()


class CheckerFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bind("<Configure>", self.redraw)

        self.canvasPadding = 25
        self.canvas = CheckerCanvas(
            self, borderwidth=0, highlightthickness=0, **kwargs)

    def redraw(self, event) -> None:
        padding = self.canvasPadding
        width = event.width - padding * 2
        height = event.height - padding * 2
        x = 0
        y = 0

        if(width * 4 / 3 < height):
            y = (height - width * 4 / 3) / 2 + padding
            x = padding
            height = width * 4 / 3
        else:
            x = (width - height * 3 / 4) / 2 + padding
            y = padding
            width = height * 3 / 4

        self.canvas.place(x=x, y=y, width=width, height=height)
