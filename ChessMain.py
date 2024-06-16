"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine
import myBot

p.init()
WIDTH = HEIGHT = 512 #400 is another option
DIMENSION = 8 #8x8 board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations later on
IMAGES = {}

"""
Initialize a global dictionary of images/ This will be called exactly once in the main.
"""
def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bP", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR", "wP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("pieces/" + piece + ".png"),(SQ_SIZE, SQ_SIZE))
    #Note: we can access an image by saying 'IMAGES['wp']'

"""
The main driver for code. This will handle user input and updating the graphics.
"""

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made 
    animate = False #flag variable for when we should animate a move
    loadImages() #Only do this once, before while loop
    running = True
    sqSelected = () #no square is selected, kepp track of last click of the user (tuple: (row, col))
    playerClicks = [] #keep track og player clicks (two tuples: [(6, 4), (4, 4)])
    print("White"*gs.whiteToMove + "Black"*(not gs.whiteToMove))
    gameOver = False
    playerOne = False #If a human is playing white, then this will be True. If an AI is playing then this will be False
    playerTwo = False #Same as above but for black
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                print("Bye!")
                running = False
            
            #mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() #(x, y) location of the mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    
                    if sqSelected == (row, col): #the user clicked the same square twicce
                        sqSelected = () #deselect
                        playerClicks = [] #clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) #append for both 1st and 2nd clicks 
                    
                    if len(playerClicks) == 2: #after 2nd click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board) 
                        # print("Valid moves: ",len(validMoves), "To move: ", end="")
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                moveMade = True
                                animate = True
                                gs.makeMove(validMoves[i])
                                # print("White"*gs.whiteToMove + "Black"*(not gs.whiteToMove))
                                sqSelected = () #reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #Undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: #Reset the board when 'r' is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    
        #AI move finder
        if not gameOver and not humanTurn:
            AIMove = myBot.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = myBot.findRandomMove(gs, validMoves)
            print(AIMove.getChessNotation())
            gs.makeMove(AIMove)
            moveMade = True
            animate = True
                    
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        # rev = False
        # if not gs.whiteToMove:
        #     rev = True
            # gs.board.reverse()
        drawGameState(screen, gs, validMoves=validMoves, sqSelected=sqSelected)
        
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")
        elif gs.staleMate:
            gameOver = True
            drawEndGameText(screen, "Stalemate")
        clock.tick(MAX_FPS)
        p.display.flip()
        # if rev:
        #     gs.board.reverse()
        #     rev = False

'''
Highlight the square selected and moves for piece selected
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transparency value -> 0 = transparent, 255 = opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight moves form them square
            s.fill(p.Color('yellow'))
            colored = []
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
                    colored.append((move.endRow, move.endCol))
            k = p.Surface((SQ_SIZE, SQ_SIZE))
            k.set_alpha(200)
            for square in colored:
                if gs.board[square[0]][square[1]] != "--":
                    k.fill(p.Color('red'))
                    screen.blit(k, (square[1]*SQ_SIZE, square[0]*SQ_SIZE))

"""
Responsible for all the graphics withing a ccurrent game state.
"""
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) # draw squares on the board
    highlightSquares(screen, gs, gs.getValidMoves(), sqSelected)
    drawPieces(screen, gs.board) # draw pieces on top of those squares
    
"""
Draw the dquares on the board. The top left square is always light.
"""
def drawBoard(screen):   
    global colors 
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
"""
Draw the pieces on the board using the current GameState.board
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Animating a move
'''
def animateMove(move, screen, board, clock):
    global colors
    coords = [] #list of coordinates that the animation will mvoe through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
        
def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('yellow'))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()