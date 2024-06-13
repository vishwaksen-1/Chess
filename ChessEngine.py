
class GameState():
    def __init__(self):
        """
        The board is an 8x8 2d list, each element of the list has 2 characters.
        
        The first character represents the color of the piece, 'b' or 'w'
        
        The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N', 'P'
        
        "--" represents an empty space with no piece.
        """
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'P': self.getPawnMoves, "R": self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        
        
        self.whiteToMove = True
        self.moveLog = []
        
        
    '''
    Takes a move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant)
    '''    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later or maybe show the game history later
        self.whiteToMove = not self.whiteToMove #swap players
        
    """
    Undo the last move made
    """
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch turns back
        
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()
        
    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of cols in the given row
                turn = self.board[r][c][0]
                
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    # print("Hail Science")
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # calls the appropriate move function based on piece type
        return moves
        
    '''
    Get all the pawn moves 
    ''' 
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == '--': #one square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            #captures 
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 < len(self.board):
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        
        else: #black pawn moves
            if self.board[r+1][c] == "--": # one square pawn advance
                moves.append(Move((r,c),(r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == '--': # 2 square pawn advance
                    moves.append(Move((r, c), (r+2, c), self.board))
                    
            #captures
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w': #enemy piece to capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 < len(self.board):
                if self.board[r+1][c+1][0] == 'w': #enemy piece to capture
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                
    '''
    Get all the rook moves
    '''
    def getRookMoves(self, r, c, moves):
        x = 'w'
        if self.whiteToMove:
            x = 'b'
            
        #up
        if r > 0:
            next_up = [r-1, c]
            while next_up[0] >= 0 and self.board[next_up[0]][next_up[1]] == "--":
                moves.append(Move((r, c),(next_up[0], next_up[1]), self.board))
                next_up[0] -= 1
            if next_up[0] >= 0 and self.board[next_up[0]][next_up[1]][0] == x:
                moves.append(Move((r, c),(next_up[0], next_up[1]), self.board))
        
        #down
        if r < 7:
            next_down = [r+1, c]
            while next_down[0] <= 7 and self.board[next_down[0]][next_down[1]] == "--":
                moves.append(Move((r, c),(next_down[0], next_down[1]), self.board))
                next_down[0] += 1
            if next_down[0] <= 7 and self.board[next_down[0]][next_down[1]][0] == x:
                moves.append(Move((r, c),(next_down[0], next_down[1]), self.board))
        
        #left
        if c > 0:
            next_left = [r, c-1]
            while next_left[1] >= 0 and self.board[next_left[0]][next_left[1]] == "--":
                moves.append(Move((r, c),(next_left[0], next_left[1]), self.board))
                next_left[1] -= 1
            if next_left[1] >= 0 and self.board[next_left[0]][next_left[1]][0] == x:
                moves.append(Move((r, c),(next_left[0], next_left[1]), self.board))
                
        #right
        if c < 7:
            next_right = [r, c+1]
            while next_right[1] <= 7 and self.board[next_right[0]][next_right[1]] == "--":
                moves.append(Move((r, c),(next_right[0], next_right[1]), self.board))
                next_right[1] += 1
            if next_right[1] <= 7 and self.board[next_right[0]][next_right[1]][0] == x:
                moves.append(Move((r, c),(next_right[0], next_right[1]), self.board))

    '''
    Get all the knight moves
    '''
    def getKnightMoves(self, r, c, moves):
        x = 'b'
        if self.whiteToMove:
            x = 'w'
        if r > 1: #up 2
            if c > 0 and self.board[r-2][c-1][0] != x:
                moves.append(Move((r,c),(r-2,c-1), self.board))
            if c < 7 and self.board[r-2][c+1][0] != x:
                moves.append(Move((r,c),(r-2,c+1), self.board))
        if r > 0:#up 1
            if c > 1 and self.board[r-1][c-2][0] != x:
                moves.append(Move((r,c),(r-1,c-2), self.board))
            if c < 6 and self.board[r-1][c+2][0] != x:
                moves.append(Move((r,c),(r-1,c+2), self.board))
        if r < 7:#down 1
            if c > 1 and self.board[r+1][c-2][0] != x:
                moves.append(Move((r,c),(r+1,c-2), self.board))
            if c < 6 and self.board[r+1][c+2][0] != x:
                moves.append(Move((r,c),(r+1,c+2), self.board))
        if r < 6:#down 2
            if c > 0 and self.board[r+2][c-1][0] != x:
                moves.append(Move((r,c),(r+2,c-1), self.board))
            if c < 7 and self.board[r+2][c+1][0] != x:
                moves.append(Move((r,c),(r+2,c+1), self.board))
            
        
        pass
    
    '''
    Get all the bishop moves
    '''
    def getBishopMoves(self, r, c, moves):
        x = 'w'
        if self.whiteToMove:
            x = 'b'
            
        #top-right -+
        if r > 0 and c < 7:
            next_step = [r-1, c+1]
            while next_step[0] >= 0 and next_step[1] <= 7 and self.board[next_step[0]][next_step[1]] == "--":
                moves.append(Move((r, c),(next_step[0], next_step[1]), self.board))
                next_step[0] -= 1
                next_step[1] += 1
            if next_step[0] >= 0 and next_step[1] <= 7 and self.board[next_step[0]][next_step[1]][0] == x:
                moves.append(Move((r, c),(next_step[0], next_step[1]), self.board))
        
        #top-left --
        if r > 0 and c > 0:
            next_step = [r-1, c-1]
            while next_step[0] >= 0 and next_step[1] >= 0 and self.board[next_step[0]][next_step[1]] == "--":
                moves.append(Move((r, c),(next_step[0], next_step[1]), self.board))
                next_step[0] -= 1
                next_step[1] -= 1
            if next_step[0] >= 0 and next_step[1] >= 0 and self.board[next_step[0]][next_step[1]][0] == x:
                moves.append(Move((r, c),(next_step[0], next_step[1]), self.board))
        
        #bottom-left +-
        if r < 7 and c > 0:
            next_step = [r+1, c-1]
            while next_step[0] <= 7 and next_step[1] >= 0 and self.board[next_step[0]][next_step[1]] == "--":
                moves.append(Move((r, c),(next_step[0], next_step[1]), self.board))
                next_step[0] += 1
                next_step[1] -= 1
            if next_step[0] <= 7 and next_step[1] >= 0 and self.board[next_step[0]][next_step[1]][0] == x:
                moves.append(Move((r, c),(next_step[0], next_step[1]), self.board))
        
        #bottom-right ++
        if r < 7 and c < 7:
            next_step = [r+1, c+1]
            while next_step[0] <= 7 and next_step[1] <= 7 and self.board[next_step[0]][next_step[1]] == "--":
                moves.append(Move((r, c),(next_step[0], next_step[1]), self.board))
                next_step[0] += 1
                next_step[1] += 1
            if next_step[0] <= 7 and next_step[1] <= 7 and self.board[next_step[0]][next_step[1]][0] == x:
                moves.append(Move((r, c),(next_step[0], next_step[1]), self.board))
    
    '''
    Get all the queen moves
    '''
    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)
    
    '''
    Get all the king moves
    '''
    def getKingMoves(self, r, c, moves):
        x = 'b'
        if self.whiteToMove:
            x = 'w'
        if r > 0: #up
            if self.board[r-1][c][0] != x:
                moves.append(Move((r,c),(r-1,c), self.board))
            if c > 0 and self.board[r-1][c-1][0] != x:
                moves.append(Move((r,c),(r-1,c-1),self.board))
            if c < 7 and self.board[r-1][c+1][0] != x:
                moves.append(Move((r,c),(r-1,c+1), self.board))
                
        if r < 7:
            if self.board[r+1][c][0] != x: 
                moves.append(Move((r,c),(r+1,c), self.board))
            if c > 0 and self.board[r+1][c-1][0] != x:
                moves.append(Move((r,c),(r+1,c-1),self.board))
            if c < 7 and self.board[r+1][c+1][0] != x:
                moves.append(Move((r,c),(r+1,c+1), self.board))
                
        if c > 0 and self.board[r][c-1][0] != x:
            moves.append(Move((r,c),(r,c-1), self.board))
        if c < 7 and self.board[r][c+1][0] != x:
            moves.append(Move((r,c),(r,c+1), self.board))
        
    
class Move():
    # maps keys to values
    # key : value
    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    
    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    
    colsToFiles = {v:k for k,v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        # print(self.moveID)
        
    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
        
    def getChessNotation(self):
        # you can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
        