import random
import os
from ChessEngine import GameState, Move

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

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
        if gs.staleMate:
            opponentMaxScore = STALEMATE
        elif gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else:    
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score = CHECKMATE
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
def findBestMoveGKM(gs, validMoves):
    return greedyKillerMachine(gs, validMoves)
    pass

'''
Helper method to make the first recursive call
'''
def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    counter = 0
    # dL = [1]*3 + [2]*7
    # DEPTH = random.choice(dL)
    # findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1, -CHECKMATE, CHECKMATE)
    print(counter)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if random.randint(1, 10) <= 3:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            random.shuffle(nextMoves)
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            random.shuffle(nextMoves)
            score = findMoveMinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore
            
  
def findMoveNegaMax(gs: GameState, validMoves: list[Move], depth: int, turnMultiplier: int):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier*scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

def findMoveNegaMaxAlphaBeta(gs: GameState, validMoves: list[Move], depth: int, turnMultiplier: int, alpha: int, beta: int):
    global nextMove, counter
    counter += 1 
    if depth == 0:
        return turnMultiplier*scoreBoard(gs)
    
    #move ordering - implement later
    maxScore = -CHECKMATE
    for move in validMoves: 
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: #pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

'''
A positive score is good for the white player and a negative score is good for the black player
'''
def scoreBoard(gs: GameState):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins
    
    elif gs.staleMate:
        return STALEMATE
    
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score

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