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

    def make_move(self, move) -> None:
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

    def inCheck(self):
        """
        Function to determine if the current player is in check
        """
        if self.whiteToMove:
            return self.squareUnderAttack(
                self.whiteKingLocation[0], self.whiteKingLocation[1]
            )
        else:
            return self.squareUnderAttack(
                self.blackKingLocation[0], self.blackKingLocation[1]
            )

    def getValidMoves(self):
        """
        Function to get all valid moves for the current player.
        Valid moves are moves that don't leave the player in check
        """
        moves = []
        # tempEnpassantPossible = self.enpassantPossible
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        tempCastleRights = CastleRights(
            self.currentCastlingRights.wks,
            self.currentCastlingRights.bks,
            self.currentCastlingRights.wqs,
            self.currentCastlingRights.bqs,
        )  # copy the current castling rights
        # moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        # self.getCastleMoves(kingRow, kingCol, moves)
        if self.inCheck:
            if len(self.checks) == 1:  # only 1 check, block check or move king
                moves = self.getAllPossibleMoves()
                # to block a check you must move a piece into one of
                # the squares between the enemy piece and king
                check = self.checks[0]  # check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][
                    checkCol
                ]  # enemy piece causing the check
                validSquares = []  # squares that pieces can move to
                # if knight, must capture the knight ot move king,
                # other pieces can be blocked
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (
                            kingRow + check[2] * i,
                            kingCol + check[3] * i,
                        )  # check[2] and check[3] are check directions
                        validSquares.append(validSquare)
                        if (
                            validSquare[0] == checkRow and validSquare[1] == checkCol
                        ):  # once you get to piece and checks
                            break
                # get rid ot any moves that don't block check or move king
                for i in range(
                    len(moves) - 1, -1, -1
                ):  # go through backwards when you are removing
                    # from a list as iterating
                    if (
                        moves[i].pieceMoved[1] != "K"
                    ):  # move doesn't move king so it must block or capture
                        if (
                            not (moves[i].endRow, moves[i].endCol) in validSquares
                        ):  # move doesn't block check or capture piece
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else:  # not in check so all moves are fine
            moves = self.getAllPossibleMoves()
            if self.whiteToMove:
                self.getCastleMoves(
                    self.whiteKingLocation[0], self.whiteKingLocation[1], moves
                )
            else:
                self.getCastleMoves(
                    self.blackKingLocation[0], self.blackKingLocation[1], moves
                )

        if len(moves) == 0:  # either checkMate or staleMate
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        self.currentCastlingRights = tempCastleRights
        return moves

    def getAllPossibleMoves(self):
        """
        Function to get all possible moves for a given player
        """
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of cols in the given row
                turn = self.board[r][c][0]

                if (turn == "w" and self.whiteToMove) or (
                    turn == "b" and not self.whiteToMove
                ):
                    # print("Hail Science")
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](
                        r, c, moves
                    )  # calls the appropriate move function
                    # based on piece type
        return moves

    def getPawnMoves(self, r, c, moves):
        """
        Function to get all the pawn moves for the pawn located at row, col
        and add these moves to the list

        Parameters:
        -----------
        r: int - row number of the pawn
        c: int - column number of the pawn
        moves: list[Move] - list of moves
        """
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
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

        if self.board[r + moveAmount][c] == "--":  # 1 square move
            if (not piecePinned) or pinDirection == (moveAmount, 0):
                if (
                    r + moveAmount == backRow
                ):  # if piece gets to back rank then it is a pawn promotion
                    isPawnPromotion = True
                moves.append(
                    Move(
                        (r, c),
                        (r + moveAmount, c),
                        self.board,
                        isPawnPromotion=isPawnPromotion,
                    )
                )
                if (
                    r == startRow and self.board[r + 2 * moveAmount][c] == "--"
                ):  # 2 square moves
                    moves.append(Move((r, c), (r + 2 * moveAmount, c), self.board))
        if c - 1 >= 0:  # capture to left
            if (not piecePinned) or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor:
                    if (
                        r + moveAmount == backRow
                    ):  # if piece gets to back rank then it is a pawn promotion
                        isPawnPromotion = True
                    moves.append(
                        Move(
                            (r, c),
                            (r + moveAmount, c - 1),
                            self.board,
                            isPawnPromotion=isPawnPromotion,
                        )
                    )
                if (r + moveAmount, c - 1) == self.enpassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:  # king is left of pawn
                            #inside - between king and pawn; outside - between pawn and border
                            insideRange = range(kingCol + 1, c-1)
                            outsideRange = range(c + 1, 8)
                        else: #king is right of pawn
                            insideRange = range(kingCol - 1, c, -1)
                            outsideRange = range(c-2, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--": # some other piece is in the way
                                blockingPiece = True
                                break
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                                break
                    if not attackingPiece or blockingPiece:
                        moves.append(
                            Move(
                                (r, c),
                                (r + moveAmount, c - 1),
                                self.board,
                                isEnpassantMove=True,
                            )
                        )
        if c + 1 <= 7:  # capture to right
            if (not piecePinned) or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:
                    if (
                        r + moveAmount == backRow
                    ):  # if piece gets to back rank then it is a pawn promotion
                        isPawnPromotion = True
                    moves.append(
                        Move(
                            (r, c),
                            (r + moveAmount, c + 1),
                            self.board,
                            isPawnPromotion=isPawnPromotion,
                        )
                    )
                if (r + moveAmount, c + 1) == self.enpassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:  # king is left of pawn
                            #inside - between king and pawn; outside - between pawn and border
                            insideRange = range(kingCol + 1, c)
                            outsideRange = range(c + 2, 8)
                        else: #king is right of pawn
                            insideRange = range(kingCol - 1, c+1, -1)
                            outsideRange = range(c-1, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--": # some other piece is in the way
                                blockingPiece = True
                                break
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                                break
                    if not attackingPiece or blockingPiece:
                        moves.append(
                            Move(
                                (r, c),
                                (r + moveAmount, c + 1),
                                self.board,
                                isEnpassantMove=True,
                            )
                        )

    def getRookMoves(self, r, c, moves):
        """
        Function to get all the rook moves for the rook located at row, col
        and add these moves to the list

        Parameters:
        -----------
        r: int - row number of the rook
        c: int - column number of the rook
        moves: list[Move] - list of moves
        """
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if (
                    self.board[r][c][1] != "Q"
                ):  # can't remove queen from pin on rook moves,
                    # only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
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

    def getKnightMoves(self, r, c, moves):
        """
        Function to get all the knight moves for the knight located at row, col
        and add these moves to the list

        Parameters:
        -----------
        r: int - row number of the knight
        c: int - column number of the knight
        moves: list[Move] - list of moves
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
        Function to get all the bishop moves for the bishop located at row, col
        and add these moves to the list

        Parameters:
        -----------
        r: int - row number of the bishop
        c: int - column number of the bishop
        moves: list[Move] - list of moves
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

    def getQueenMoves(self, r, c, moves):
        """
        Function to get all the queen moves for the queen located at row, col
        and add these moves to the list

        Parameters:
        -----------
        r: int - row number of the queen
        c: int - column number of the queen
        moves: list[Move] - list of moves
        """
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        """
        Function to get all the king moves for the king located at row, col
        and add these moves to the list

        Parameters:
        -----------
        r: int - row number of the king
        c: int - column number of the king
        moves: list[Move] - list of moves
        """
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
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
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    # place king back to original location
                    if allyColor == "w":
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)

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

    def getKingsideCastleMoves(self, row, col, moves):
        """
        Function to get all the valid kingside castle moves for the king at (row, col)
        and add them to the list of moves

        Parameters:
        -----------
        row: int - row number of the king
        col: int - column number of the king
        moves: list[Move] - list of moves
        """
        if self.board[row][col + 1] == "--" and self.board[row][col + 2] == "--":
            if not self.squareUnderAttack(row, col + 1) and not self.squareUnderAttack(
                row, col + 2
            ):
                moves.append(
                    Move((row, col), (row, col + 2), self.board, isCastleMove=True)
                )

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
    Class to keep track of the castling rights of the players.
    It keeps track of whether the kingside or queenside castling is possible for both players.

    Attributes:
    -----------
    wks: bool - White king side castle possible
    bks: bool - Black king side castle possible
    wqs: bool - White queen side castle possible
    bqs: bool - Black queen side castle possible
    """

    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
        pass


class Move:
    """
    Class to represent a move made by a player.

    Attributes:
    -----------
    startRow: int - Row number of the start square
    startCol: int - Column number of the start square
    endRow: int - Row number of the end square
    endCol: int - Column number of the end square
    pieceMoved: str - Piece moved
    pieceCaptured: str - Piece captured
    moveID: int - ID of the move
    isPawnPromotion: bool - If the move is a pawn promotion
    isEnpassantMove: bool - If the move is an en passant move
    isCastleMove: bool - If the move is a castle move
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
        Initializes the Move object with the start and end square,
        the piece moved, the piece captured, and the move ID.
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
        # self.isCapture = self.pieceCaptured != "--"
        # print(self.moveID)
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
        Overriding the equality operator to compare two Move objects.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        """
        A basic function to get the chess notation of the move.
        """
        # you can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(
            self.endRow, self.endCol
        )

    def getRankFile(self, r, c):
        """
        Function to get the rank and file of the square.
        """
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
    def __str__(self) -> str:
        '''
        Overriding the string representation of the Move object.
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

        