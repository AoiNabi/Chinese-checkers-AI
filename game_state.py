class GameState:
    # inicializa la clase GameState y crea el tablero del juego con la disposición inicial de las 
    # fichas para cada jugador. Define la estructura del tablero utilizando un diccionario (self.map) 
    # donde las claves son coordenadas (x, y) y los valores representan el tipo de ficha o vacío en 
    # esa posición.
    def __init__(self) -> None:
        self.map = {}
        # Color 1
        for y in range(4):
            for x in range(y + 1):
                self.map[(x - y + 8), y - 4] = 1
        # Color 2
        for y in range(4):
            for x in range(4 - y):
                self.map[(x, y)] = 0
        # Color 3
        for y in range(4):
            for x in range(y + 1):
                self.map[(x - y - 1), y + 5] = 0
        # Color 4
        for y in range(4):
            for x in range(4 - y):
                self.map[(x, y + 9)] = 2
        # Color 5
        for y in range(4):
            for x in range(y + 1):
                self.map[(x - y + 8), y + 5] = 0
        # Color 6
        for y in range(4):
            for x in range(4 - y):
                self.map[(x + 9, y)] = 0
        # Color 7
        for y in range(5):
            for x in range(y + 5):
                self.map[(x - y + 4, y)] = 0
        for y in range(4):
            for x in range(8 - y):
                self.map[(x, y + 5)] = 0

    # Este método devuelve una lista de todos los movimientos posibles que puede realizar el jugador 
    # actual en el estado de juego actual. Itera sobre las fichas del jugador actual y obtiene todos 
    # los movimientos válidos para cada una de ellas.
    def getAvailableMoves(self, currentPlayer: int) -> list[tuple['GameState', tuple[int, int], tuple[int, int]]]:
        result: list[GameState] = []
        map = self.map

        myMarbles = []
        # Get marbles
        for cord, player in map.items():
            if player == currentPlayer:
                myMarbles.append(cord)

        for cords in myMarbles:
            moveCords = self.getMarbleMoves(cords)
            result.extend([(self.moveMarble(cords, x), cords, x)
                           for x in moveCords])

        return result

    # Este método devuelve una lista de movimientos válidos para una ficha en una coordenada específica. 
    # Calcula los movimientos posibles, tanto movimientos normales como saltos (hops), verificando si las 
    # posiciones adyacentes están vacías o si se pueden realizar saltos sobre otras fichas.
    def getMarbleMoves(self, cords) -> list[tuple[int, int]]:
        result = []

        x, y = cords
        map = self.map
        # Normal moves
        if map.get((x, y - 1)) == 0:
            result.append((x, y - 1))
        if map.get((x + 1, y - 1)) == 0:
            result.append((x + 1, y - 1))
        if map.get((x - 1, y)) == 0:
            result.append((x - 1, y))
        if map.get((x + 1, y)) == 0:
            result.append((x + 1, y))
        if map.get((x - 1, y + 1)) == 0:
            result.append((x - 1, y + 1))
        if map.get((x, y + 1)) == 0:
            result.append((x, y + 1))

        # Hop moves
        visited = {(x, y)}
        toVisit = set()

        if map.get((x, y - 1), 0) != 0 and map.get((x, y - 2)) == 0:
            toVisit.add((x, y - 2))
        if map.get((x + 1, y - 1), 0) != 0 and map.get((x + 2, y - 2)) == 0:
            toVisit.add((x + 2, y - 2))
        if map.get((x - 1, y), 0) != 0 and map.get((x - 2, y)) == 0:
            toVisit.add((x - 2, y))
        if map.get((x + 1, y), 0) != 0 and map.get((x + 2, y)) == 0:
            toVisit.add((x + 2, y))
        if map.get((x - 1, y + 1), 0) != 0 and map.get((x - 2, y + 2)) == 0:
            toVisit.add((x - 2, y + 2))
        if map.get((x, y + 1), 0) != 0 and map.get((x, y + 2)) == 0:
            toVisit.add((x, y + 2))

        while len(toVisit) != 0:
            m = toVisit.pop()
            if m in visited:
                continue

            result.append(m)
            visited.add(m)
            x1, y1 = m

            if map.get((x1, y1 - 1), 0) != 0 and map.get((x1, y1 - 2)) == 0:
                toVisit.add((x1, y1 - 2))
            if map.get((x1 + 1, y1 - 1), 0) != 0 and map.get((x1 + 2, y1 - 2)) == 0:
                toVisit.add((x1 + 2, y1 - 2))
            if map.get((x1 - 1, y1), 0) != 0 and map.get((x1 - 2, y1)) == 0:
                toVisit.add((x1 - 2, y1))
            if map.get((x1 + 1, y1), 0) != 0 and map.get((x1 + 2, y1)) == 0:
                toVisit.add((x1 + 2, y1))
            if map.get((x1 - 1, y1 + 1), 0) != 0 and map.get((x1 - 2, y1 + 2)) == 0:
                toVisit.add((x1 - 2, y1 + 2))
            if map.get((x1, y1 + 1), 0) != 0 and map.get((x1, y1 + 2)) == 0:
                toVisit.add((x1, y1 + 2))

        return result

    # Este método realiza el movimiento de una ficha desde una posición inicial a una posición siguiente. 
    # Crea un nuevo estado de juego y actualiza la posición de la ficha, reflejando el movimiento realizado.
    def moveMarble(self, initial, next) -> 'GameState':
        result = GameState()
        result.map = self.map.copy()
        temp = result.map[initial]
        result.map[initial] = result.map[next]
        result.map[next] = temp

        return result

    # Calcula una heurística que evalúa la posición actual del juego. Determina una puntuación basada en 
    # la distribución de las fichas en el tablero para cada jugador, buscando favorecer la posición de un
    # jugador sobre el otro.
    def getHeuristic(self) -> int:
        HR = 0
        HG = 0
        for cords, p in self.map.items():
            if p == 1:
                mx = 0
                for y in range(4):
                    for x in range(4 - y):
                        if cords[1] > (y + 9):
                            continue
                        if self.map[(x, y + 9)] != 1:
                            mx = max(
                                mx, (x - cords[0]) * (x - cords[0]) + (y + 9 - cords[1]) * (y + 9 - cords[1]))
                HG += mx
            elif p == 2:
                mx = 0
                for y in range(4):
                    for x in range(y + 1):
                        if cords[1] < y - 4:
                            continue
                        if self.map[(x - y + 8), y - 4] != 2:
                            mx = max(mx, (x - y + 8 - cords[0]) * (x - y + 8 - cords[0]) + (y - 4 - cords[1]) * (
                                y - 4 - cords[1]))
                HR += mx

        return HR - HG

    def winCondition(self) -> int:
        # topside
        topSideFull = True
        botSideFull = True
        blueWin = False
        yellowWin = False
        for y in range(4):
            for x in range(y + 1):
                # self.map[(x - y + 8), y - 4] = 1
                if (topSideFull):
                    if (self.map[(x - y + 8), y - 4] == 0):
                        topSideFull = False
                    elif (self.map[(x - y + 8), y - 4] == 2):
                        blueWin = True
        if (topSideFull and blueWin):
            return 2

        # botside
        for y in range(4):
            for x in range(4 - y):
                # self.map[(x, y + 9)] = 2
                if (botSideFull):
                    if (self.map[(x, y + 9)] == 0):
                        botSideFull = False
                    elif (self.map[(x, y + 9)] == 1):
                        yellowWin = True
        if (botSideFull and yellowWin):
            return 1

        return 0

    def alphaBetaSearch(self, depth: int) -> tuple[tuple[int, int], tuple[int, int]]:
        def minValue(state: GameState, alpha: int, beta: int, depth: int) -> tuple[
                int, tuple[int, int], tuple[int, int]]:
            win = state.winCondition()
            if win == 1:
                return float('inf'), None, None
            elif win == 2:
                return float('-inf'), None, None
            elif depth == 0:
                return state.getHeuristic(), None, None

            v = float('inf')
            minInitial = None
            minNext = None
            for s, initial, next in state.getAvailableMoves(2):
                h, _, _ = maxValue(s, alpha, beta, depth - 1)
                if v > h:
                    v = h
                    minInitial = initial
                    minNext = next

                if v <= alpha:
                    return v, minInitial, minNext
                beta = min(v, beta)

            return v, minInitial, minNext

        def maxValue(state: GameState, alpha: int, beta: int, depth: int) -> tuple[
                int, tuple[int, int], tuple[int, int]]:
            win = state.winCondition()
            if win == 1:
                return float('inf'), None, None
            elif win == 2:
                return float('-inf'), None, None
            elif depth == 0:
                return state.getHeuristic(), None, None

            v = float('-inf')
            maxInitial = None
            maxNext = None
            for s, initial, next in state.getAvailableMoves(1):
                h, _, _ = minValue(s, alpha, beta, depth - 1)
                if v < h:
                    v = h
                    maxInitial = initial
                    maxNext = next

                if v >= beta:
                    return v, maxInitial, maxNext
                alpha = max(v, alpha)

            return v, maxInitial, maxNext

        _, initial, next = maxValue(self, float('-inf'), float('inf'), depth)

        return initial, next
