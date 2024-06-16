import random
import os

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0


'''
Picks and returns a random move
'''
def findRandomMove(gs, validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

#Assuming balck is the computer
def greedyKillerMachine(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        opponentMaxScore = -CHECKMATE
        for opponentsMove in opponentsMoves:
            gs.makeMove(opponentsMove)
            if gs.checkMate:
                score = -turnMultiplier * CHECKMATE
            elif gs.staleMate:
                score = STALEMATE
            else:
                score = -turnMultiplier*scoreMaterial(gs.board)
            if score > opponentMaxScore:
                opponentMaxScore = score
            gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

'''
Find the best move based on material alone
'''
def findBestMove(gs, validMoves):
    return greedyKillerMachine(gs, validMoves)
    pass

'''
Score the board based on material    
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score

# from ChessEngine import GameState, Move, CastleRights
# gx = GameState()
# moves = gx.getAllPossibleMoves()
# print(moves)

# move = greedyKillerMachine(gx, moves)
# print(move.getChessNotation())