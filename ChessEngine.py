class GameState:
    """
    Represents the current state of the game.

    Attributes
    ----------
    board : list[list[str]]
        A 2d list to represent the board.
    moveFunctions : dict
        A dictionary to map piece types to their move functions.
    whiteToMove : bool
        True if white is to move, False if black is to move.
    moveLog : list[Move]
        A list to store the moves made in the game.
    whiteKingLocation : tuple[int]
        The location of the white king.
    blackKingLocation : tuple[int]
        The location of the black king.
    inCheck : bool
        True if the current player is in check.
    checkMate : bool
        True if the current player is in checkMate.
    staleMate : bool
        True if the current player is in staleMate.
    pins : list[tuple[int]]
        A list of pinned pieces.
    checks : list[tuple[int]]
        A list of squares where the enemy is applying a check.
    enpassantPossible : tuple[int]
        The square where enpassant is possible.
    enpassantPossibleLog : list[tuple[int]]
        A list to store the enpassant possible squares.
    currentCastlingRights : CastleRights
        The current castling rights.
    """

    def __init__(self):
        """
        The chess board is represented as an 8x8 two-dimensional list.
        
        Each element in the list consists of a two-character string:
        
        - The first character indicates the color of the piece: 'b' for black or 'w' for white.
        - The second character denotes the type of the piece:
            - 'K' for King
            - 'Q' for Queen
            - 'R' for Rook
            - 'B' for Bishop
            - 'N' for Knight
            - 'P' for Pawn

        An element with "--" represents an empty square with no piece.
        """
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        # self.board = [ #trainer
        #     ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        # ]
        self.moveFunctions = {
            "P": self.getPawnMoves,
            "R": self.getRookMoves,
            "N": self.getKnightMoves,
            "B": self.getBishopMoves,
            "Q": self.getQueenMoves,
            "K": self.getKingMoves,
        }

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.checkMate = False
        self.staleMate = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = ()
        # coordinated for the square where enpassant is possible
        self.enpassantPossibleLog = [self.enpassantPossible]
        # castle move
        #is a capture move
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [
            CastleRights(
                self.currentCastlingRights.wks,
                self.currentCastlingRights.bks,
                self.currentCastlingRights.wqs,
                self.currentCastlingRights.bqs,
            )
        ]

    def makeMove(self, move) -> None:
        """
        Make a move given a Move object.

        This function updates the board to reflect the move, updates the move log,
        and swaps the current player. It also updates the king's location if the
        move is a king move, and updates the en passant possible square if the move
        is a pawn move.

        Parameters
        ----------
        move : Move
            The move to be made.

        Returns
        -------
        None
        """
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later or
        # maybe show the game history later

        self.whiteToMove = not self.whiteToMove  # swap players
        # update the king's location if moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        # if pawn moves twice next move can capture enpassant
        if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.endRow + move.startRow) // 2, move.endCol)
        else:
            self.enpassantPossible = ()
        # if enpassant move, must update the board to capture the pawn
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"

        # if pawn promotion, change piece
        if move.isPawnPromotion:
            # promotedPiece = (
            #     input("Promote to Q, R, B or N: ").strip().upper()
            # )  # we can make this part of UI later
            # if promotedPiece not in "QRBN":
            promotedPiece = "Q"
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece

        # castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # king-side castle move
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][
                    move.endCol + 1
                ]  # moves the rook to its new square
                self.board[move.endRow][move.endCol + 1] = "--"  # erase old rook
            else:  # queen-side castle move
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][
                    move.endCol - 2
                ]  # moves the rook to its new square
                self.board[move.endRow][move.endCol - 2] = "--"  # erase old rook

        self.enpassantPossibleLog.append(self.enpassantPossible)

        # update castling rights - whenever it is a rook or king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(
            CastleRights(
                self.currentCastlingRights.wks,
                self.currentCastlingRights.bks,
                self.currentCastlingRights.wqs,
                self.currentCastlingRights.bqs,
            )
        )

    def undoMove(self):
        """
        Reverts the board to the state before the move was made, and resets the
        move log.
        """
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back
            # update the king's location if undo-ed
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            # undo enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][
                    move.endCol
                ] = "--"  # leave the landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                # self.enpassantPossible = (move.endRow, move.endCol)

                self.enpassantPossibleLog.pop()
                self.enpassantPossible = self.enpassantPossibleLog[-1]

            # undo a 2 square pawn advance
            if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            # undo castle rights
            self.castleRightsLog.pop()
            # get rid of the new castle rights from the move we are undoing
            self.currentCastlingRights = self.castleRightsLog[-1]
            # set the current castle rights to the last one in the list

            # undo the castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # king-side
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][
                        move.endCol - 1
                    ]
                    self.board[move.endRow][move.endCol - 1] = "--"
                else:  # queen-side
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][
                        move.endCol + 1
                    ]
                    self.board[move.endRow][move.endCol + 1] = "--"
            
            self.checkMate = False
            self.staleMate = False

    def updateCastleRights(self, move):
        """
        Updates the castling rights based on the given move.

        This method modifies the current castling rights if the move involves
        a king or a rook, as these moves impact the ability to castle.

        Parameters
        ----------
        move : Move
            The move that was made, affecting the castling rights.
        """
        if move.pieceCaptured == "wR":
            if move.endCol == 0:  # left rook
                self.currentCastlingRights.wqs = False
            elif move.endCol == 7:  # right rook
                self.currentCastlingRights.wks = False
        elif move.pieceCaptured == "bR":
            if move.endCol == 0:  # left rook
                self.currentCastlingRights.bqs = False
            elif move.endCol == 7:  # right rook
                self.currentCastlingRights.bks = False

        if move.pieceMoved == "wK":
            self.currentCastlingRights.wqs = False
            self.currentCastlingRights.wks = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRights.bqs = False
            self.currentCastlingRights.bks = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRights.bks = False

    def squareUnderAttack(self, r: int, c: int) -> bool:
        """
        Determines if a square is under attack by the opponent.

        The function temporarily switches the turn to the opponent
        to calculate all possible moves they can make. It then checks
        if any of these moves can reach the specified square.

        Parameters
        ----------
        r : int
            The row index of the square.
        c : int
            The column index of the square.

        Returns
        -------
        bool
            True if the square is under attack by the opponent, 
            False otherwise.
        """
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        return any(move.endRow == r and move.endCol == c for move in oppMoves)

    def inCheck(self) -> bool:
        """
        Determines if the current player's king is in check.

        This function checks if the king of the current player is 
        under attack by any opponent piece.

        Returns
        -------
        bool
            True if the current player's king is in check, False otherwise.
        """
        kingLocation = (
            self.whiteKingLocation if self.whiteToMove else self.blackKingLocation
        )
        return self.squareUnderAttack(kingLocation[0], kingLocation[1])

    def getValidMoves(self):
        """
        Generates a list of valid moves for the current player.

        This function determines all possible moves for the current player 
        and filters out any that would leave the player's king in check.

        Returns
        -------
        list[Move]
            A list of valid moves for the current player.
        """
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        tempCastleRights = CastleRights(
            self.currentCastlingRights.wks,
            self.currentCastlingRights.bks,
            self.currentCastlingRights.wqs,
            self.currentCastlingRights.bqs,
        )
        
        kingRow, kingCol = self.whiteKingLocation if self.whiteToMove else self.blackKingLocation
        
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow, checkCol = check[0], check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = [(checkRow, checkCol)] if pieceChecking[1] == 'N' else [
                    (kingRow + check[2] * i, kingCol + check[3] * i)
                    for i in range(1, 8)
                    if (kingRow + check[2] * i, kingCol + check[3] * i) != (checkRow, checkCol)
                ]
                moves = [move for move in moves if move.pieceMoved[1] == 'K' or (move.endRow, move.endCol) in validSquares]
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()
            self.getCastleMoves(kingRow, kingCol, moves)

        if not moves:
            self.checkMate = self.inCheck
            self.staleMate = not self.inCheck
        else:
            self.checkMate = False
            self.staleMate = False

        self.currentCastlingRights = tempCastleRights
        return moves

    def getAllPossibleMoves(self):
        """
        Generates a list of all possible moves for the current player.

        This function iterates over the entire board and calls the 
        appropriate move function for each piece on the board. It 
        filters out any moves that are not valid for the current player.

        Returns
        -------
        list[Move]
            A list of all possible moves for the current player.
        """
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of cols in the given row
                turn = self.board[r][c][0]

                if (turn == "w" and self.whiteToMove) or (
                    turn == "b" and not self.whiteToMove
                ):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, row: int, col: int, moves: list) -> None:
        """
        Function to get all the pawn moves for the pawn located at row, col
        and add these moves to the list.

        Parameters:
        -----------
        row: int
            Row number of the pawn.
        col: int
            Column number of the pawn.
        moves: list[Move]
            List of moves to append to.

        Returns
        -------
        None
        """
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:  # white pawm moves
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = "b"
            kingRow, kingCol = self.whiteKingLocation
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = "w"
            kingRow, kingCol = self.blackKingLocation
        isPawnPromotion = False

        if self.board[row + moveAmount][col] == "--":  # 1 square move
            if (not piecePinned) or pinDirection == (moveAmount, 0):
                if (row + moveAmount == backRow):  # if piece gets to back rank then it is a pawn promotion
                    isPawnPromotion = True
                moves.append(
                    Move(
                        (row, col),
                        (row + moveAmount, col),
                        self.board,
                        isPawnPromotion=isPawnPromotion,
                    )
                )
                if (row == startRow and self.board[row + 2 * moveAmount][col] == "--"):
                    # 2 square moves
                    moves.append(Move((row, col), (row + 2 * moveAmount, col), self.board))
        if col - 1 >= 0:  # capture to left
            if (not piecePinned) or pinDirection == (moveAmount, -1):
                if self.board[row + moveAmount][col - 1][0] == enemyColor:
                    if (row + moveAmount == backRow):
                        # if piece gets to back rank then it is a pawn promotion
                        isPawnPromotion = True
                    moves.append(
                        Move(
                            (row, col),
                            (row + moveAmount, col - 1),
                            self.board,
                            isPawnPromotion=isPawnPromotion,
                        )
                    )
                if (row + moveAmount, col - 1) == self.enpassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == row:
                        if kingCol < col:  # king is left of pawn
                            # inside - between king and pawn; outside - between pawn and border
                            insideRange = range(kingCol + 1, col - 1)
                            outsideRange = range(col + 1, 8)
                        else:  # king is right of pawn
                            insideRange = range(kingCol - 1, col, -1)
                            outsideRange = range(col - 2, -1, -1)
                        for i in insideRange:
                            if self.board[row][i] != "--":  # some other piece is in the way
                                blockingPiece = True
                                break
                        for i in outsideRange:
                            square = self.board[row][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                                break
                    if not attackingPiece or blockingPiece:
                        moves.append(
                            Move(
                                (row, col),
                                (row + moveAmount, col - 1),
                                self.board,
                                isEnpassantMove=True,
                            )
                        )
        if col + 1 <= 7:  # capture to right
            if (not piecePinned) or pinDirection == (moveAmount, 1):
                if self.board[row + moveAmount][col + 1][0] == enemyColor:
                    if (row + moveAmount == backRow):
                        # if piece gets to back rank then it is a pawn promotion
                        isPawnPromotion = True
                    moves.append(
                        Move(
                            (row, col),
                            (row + moveAmount, col + 1),
                            self.board,
                            isPawnPromotion=isPawnPromotion,
                        )
                    )
                if (row + moveAmount, col + 1) == self.enpassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == row:
                        if kingCol < col:  # king is left of pawn
                            # inside - between king and pawn; outside - between pawn and border
                            insideRange = range(kingCol + 1, col)
                            outsideRange = range(col + 2, 8)
                        else:  # king is right of pawn
                            insideRange = range(kingCol - 1, col + 1, -1)
                            outsideRange = range(col - 1, -1, -1)
                        for i in insideRange:
                            if self.board[row][i] != "--":  # some other piece is in the way
                                blockingPiece = True
                                break
                        for i in outsideRange:
                            square = self.board[row][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                                break
                    if not attackingPiece or blockingPiece:
                        moves.append(
                            Move(
                                (row, col),
                                (row + moveAmount, col + 1),
                                self.board,
                                isEnpassantMove=True,
                            )
                        )

    def getRookMoves(self, r, c, moves):
        """
        Generate all valid rook moves for the rook located at the specified position 
        and append these moves to the provided list.

        The function considers the rook's movement in all four orthogonal directions 
        (up, down, left, right) until an obstacle is encountered.

        Parameters
        ----------
        r : int
            The row index of the rook's current position.
        c : int
            The column index of the rook's current position.
        moves : list[Move]
            A list to which valid rook moves will be appended.
        """
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q":  # can't remove queen from pin on rook moves
                    self.pins.remove(self.pins[i])
                break

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:  # enemy piece is valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # friendly piece invalid
                            break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        """
        Generate all valid knight moves for the knight located at the specified position 
        and append these moves to the provided list.

        Parameters
        ----------
        r : int
            The row index of the knight's current position.
        c : int
            The column index of the knight's current position.
        moves : List[Move]
            A list to which valid knight moves will be appended.
        """
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        knightMoves = (
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        )
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if (
                        endPiece[0] != allyColor
                    ):  # not an ally piece (empty or enemy piece)
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        

    def getBishopMoves(self, r, c, moves):
        """
        Generate all valid bishop moves for the bishop located at the specified position 
        and append these moves to the provided list.

        The function considers the bishop's diagonal movement in all four directions 
        until an obstacle is encountered.

        Parameters
        ----------
        r : int
            The row index of the bishop's current position.
        c : int
            The column index of the bishop's current position.
        moves : list[Move]
            A list to which valid bishop moves will be appended.

        Returns
        -------
        None
        """
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    if (
                        (not piecePinned)
                        or (pinDirection == d)
                        or pinDirection == (-d[0], -d[1])
                    ):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:  # enemy piece is valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # friendly piece invalid
                            break
                else:  # off board
                    break

    def getQueenMoves(self, r: int, c: int, moves) -> None:
        """
        Generates all valid moves for the queen located at (r, c) and appends them to the moves list.

        Parameters:
        ----------
        r : int
            The row index of the queen's current position.
        c : int
            The column index of the queen's current position.
        moves : List[Move]
            A list to which valid queen moves will be appended.

        Returns
        -------
        None
        """
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getKingMoves(self, row: int, col: int, moves) -> None:
        """
        Generates all valid moves for the king located at (row, col) and appends them to the moves list.

        Parameters:
        ----------
        row : int
            The row index of the king's current position.
        col : int
            The column index of the king's current position.
        moves : List[Move]
            A list to which valid king moves will be appended.

        Returns
        -------
        None
        """
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = row + rowMoves[i]
            endCol = col + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece (enemy or empty piece)
                    # place king on end square and check for checks
                    if allyColor == "w":
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    # place king back to original location
                    if allyColor == "w":
                        self.whiteKingLocation = (row, col)
                    else:
                        self.blackKingLocation = (row, col)

    def getCastleMoves(self, row, col, moves):
        """
        Function to get all the castle moves for the king located at row, col
        and add these moves to the list

        Parameters:
        -----------
        row: int - row number of the king
        col: int - column number of the king
        moves: list[Move] - list of moves
        """
        if self.squareUnderAttack(row, col):
            return  # can't castle while in check
        if (self.whiteToMove and self.currentCastlingRights.wks) or (
            not self.whiteToMove and self.currentCastlingRights.bks
        ):
            self.getKingsideCastleMoves(row, col, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (
            not self.whiteToMove and self.currentCastlingRights.bqs
        ):
            self.getQueensideCastleMoves(row, col, moves)

    def getKingsideCastleMoves(self, row: int, col: int, moves) -> None:
        """
        Generates all valid kingside castle moves for the king located at (row, col)
        and appends them to the moves list.

        Parameters
        ----------
        row : int
            The row index of the king's current position.
        col : int
            The column index of the king's current position.
        moves : List[Move]
            A list to which valid kingside castle moves will be appended.

        Returns
        -------
        None
        """
        if self.board[row][col + 1] == "--" and self.board[row][col + 2] == "--":
            if not self.squareUnderAttack(row, col + 1) and not self.squareUnderAttack(row, col + 2):
                moves.append(Move((row, col), (row, col + 2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self, row, col, moves):
        """
        Function to get all the valid queenside castle moves for the king at (row, col)
        and add them to the list of moves

        Parameters:
        -----------
        row: int - row number of the king
        col: int - column number of the king
        moves: list[Move] - list of moves
        """
        if (
            self.board[row][col - 1] == "--"
            and self.board[row][col - 2] == "--"
            and self.board[row][col - 3] == "--"
        ):
            if not self.squareUnderAttack(row, col - 1) and not self.squareUnderAttack(
                row, col - 2
            ):
                moves.append(
                    Move((row, col), (row, col - 2), self.board, isCastleMove=True)
                )

    def checkForPinsAndChecks(self):
        """
        Returns if the player is in check, a list of pins, and a list of checks

        Return:
        ---------
        inCheck: bool - If the player is in check
        pins: list[int] - `[pinnedOnRow, pinnedOnColumn, direction1, direction2]`
        checks: list[tuple[int]] - tuple:```(checkFromRow, checkFromCol, direction1, direction2)```
        """
        pins = []  # squares where the allied pinned piece is and direction pinned from
        checks = []  # squares where enemy piece is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        # check outward from king for pins and checks, keep track of pins
        directions = (
            (-1, 0),
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        )
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()  # reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][
                        endCol
                    ]  # piece on board 'w*', 'b*', '--'
                    if endPiece[0] == allyColor and endPiece[1] != "K":
                        if not possiblePin:  # 1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            # 2nd allied piece, so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 possibilities here in this complex conditional
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and the piece is a king
                        # (this is necessary to prevent a king from moving to a
                        # square controlled by another king)
                        if (
                            (0 <= j <= 3 and type == "R")
                            or (4 <= j <= 7 and type == "B")
                            or (
                                i == 1
                                and type == "P"
                                and (
                                    (enemyColor == "w" and 6 <= j <= 7)
                                    or (enemyColor == "b" and 4 <= j <= 5)
                                )
                            )
                            or (type == "Q")
                            or (i == 1 and type == "K")
                        ):
                            if not possiblePin:  # no piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  # a piece is blocking so pin
                                pins.append(possiblePin)
                                break
                        else:  # enemy piece not applyimg check
                            break
        # check knight checks
        knightMoves = (
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        )
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if (
                    endPiece[0] == enemyColor and endPiece[1] == "N"
                ):  # enemy knight attacking king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks


class CastleRights:
    """
    Manages the castling rights for both players in a chess game.

    This class tracks the availability of kingside and queenside castling 
    for both the white and black players.

    Attributes
    ----------
    wks : bool
        Indicates if white kingside castling is possible.
    bks : bool
        Indicates if black kingside castling is possible.
    wqs : bool
        Indicates if white queenside castling is possible.
    bqs : bool
        Indicates if black queenside castling is possible.
    """

    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
        pass


class Move:
    """
    Represents a move made by a player in a chess game.

    Parameters
    ----------
    startRow : int
        Row number of the start square.
    startCol : int
        Column number of the start square.
    endRow : int
        Row number of the end square.
    endCol : int
        Column number of the end square.
    pieceMoved : str
        The piece moved.
    pieceCaptured : str
        The piece captured.
    moveID : int
        The ID of the move.
    isPawnPromotion : bool
        If the move is a pawn promotion.
    isEnpassantMove : bool
        If the move is an en passant move.
    isCastleMove : bool
        If the move is a castle move.

    """
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(
        self,
        startSq,
        endSq,
        board,
        isEnpassantMove=False,
        isPawnPromotion=False,
        isCastleMove=False,
    ):
        """
        Initializes the Move object with the start and end squares,
        the piece moved, the piece captured, and the move ID.

        Parameters
        ----------
        start_sq : tuple[int, int]
            The start square of the move.
        end_sq : tuple[int, int]
            The end square of the move.
        board : list[list[str]]
            The current state of the chess board.
        is_enpassant_move : bool, optional
            If the move is an en passant move. Defaults to False.
        is_pawn_promotion : bool, optional
            If the move is a pawn promotion. Defaults to False.
        is_castle_move : bool, optional
            If the move is a castle move. Defaults to False.
        """
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = (
            self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        )
        # pawn promotion
        self.isPawnPromotion = isPawnPromotion
        # en passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "wP" if self.pieceMoved == "bP" else "bP"
        # castle move
        self.isCastleMove = isCastleMove
        self.isCaptureMove = self.pieceCaptured != "--"


    def __eq__(self, other):
        """
        Compares two Move objects for equality.

        Parameters
        ----------
        other : object
            The object to compare to.

        Returns
        -------
        bool
            True if the two Move objects are equal, False otherwise.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self) -> str:
        """
        Gets the chess notation of the move.

        Returns
        -------
        str
            The chess notation of the move.
        """
        # you can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(
            self.endRow, self.endCol
        )

    def getRankFile(self, row: int, col: int) -> str:
        """
        Gets the rank and file of the square.

        Parameters
        ----------
        row : int
            The row number of the square.
        col : int
            The column number of the square.

        Returns
        -------
        str
            The rank and file of the square in standard algebraic notation.
        """
        return self.colsToFiles[col] + self.rowsToRanks[row]
    
    def __str__(self) -> str:
        '''
        Generates a string representation of the move in standard algebraic notation (SAN).

        Parameters
        ----------
        None

        Returns
        -------
        str
            The move in SAN.
        '''
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"
        
        endSquare = self.getRankFile(self.endRow, self.endCol)
        #pawn moves
        if self.pieceMoved[1] == "P":
            if self.isCaptureMove:
                if self.isEnpassantMove:
                    return self.colsToFiles[self.startCol] + "x" + endSquare + "e.p."
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                #pawn promotion
                if self.isPawnPromotion:
                    return endSquare + "=" + self.pieceMoved[1].upper()
                else:
                    return endSquare
        #Two of the same type of piece moving to s asquare, Nbd2 if both knights can move to d2
        
        #add + for a check move and # for a checkmate move
        
        #piece moves
        moveString = self.pieceMoved[1]
        if self.isCaptureMove:
            moveString += "x"
        return moveString + endSquare

        