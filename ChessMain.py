"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine

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
    
    loadImages() #Only do this once, before while loop
    running = True
    sqSelected = () #no square is selected, kepp track of last click of the user (tuple: (row, col))
    playerClicks = [] #keep track og player clicks (two tuples: [(6, 4), (4, 4)])
    print("White"*gs.whiteToMove + "Black"*(not gs.whiteToMove))
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                print("Bye!")
                running = False
            
            #mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
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
                    print("Valid moves: ",len(validMoves), "To move: ", end="")
                    # print(move.getChessNotation())
                    if move in validMoves:
                        moveMade = True
                        gs.makeMove(move)
                        # print("White"*gs.whiteToMove + "Black"*(not gs.whiteToMove))
                    sqSelected = () #reset user clicks
                    playerClicks = []
                    
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #Undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
                        
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        

"""
Responsible for all the graphics withing a ccurrent game state.
"""
def drawGameState(screen, gs):
    drawBoard(screen) # draw squares on the board
    #add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board) # draw pieces on top of those squares
    
"""
Draw the dquares on the board. The top left square is always light.
"""
def drawBoard(screen):    
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

                

if __name__ == "__main__":
    main()