
from tkinter import *

import random

def gameDimensions(): # sets up how large the window can be
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows,cols,cellSize,margin)

def playTetris(): #creates data values for tetris
    (rows,cols,cellSize,margin) = gameDimensions()
    width = cols*cellSize + 50
    height = rows*cellSize + 50
    run(width,height)
    
def init(data):
    (data.rows, data.cols, data.cellSize, data.margin) = gameDimensions()
    data.board = [ (['blue'] * data.cols) for row in range(data.rows) ]
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]]
    data.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    data.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]
    data.fallingPiece = []
    data.fallingPieceColor = ''
    data.fallingPieceRow = 0
    data.fallingPieceCol = 0
    data.timerDelay = 400
    data.isGameOver = False
    data.fullRowScore = 0
    newFallingPiece(data)

def newFallingPiece(data): # creates a new piece randomly from list of tetris pieces
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[randomIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex]
    data.fallingPieceRow = 0
    data.fallingPieceCol = ((data.cols//2) - (len(data.fallingPiece[0])//2))
    
def drawFallingPiece(canvas,data): # draws that random piece created from newFallingPiece
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if data.fallingPiece[row][col] == True:
                drawCell(canvas, data, data.fallingPieceRow + row, data.fallingPieceCol + col, data.fallingPieceColor)
            else: pass

def fallingPieceIsLegal(data): # makes sure the piece being created is going out of board
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if data.fallingPiece[row][col] == True:
                if data.fallingPieceRow + row < 0 or data.fallingPieceRow + row >= data.rows:
                    return False
                elif data.fallingPieceCol + col < 0 or data.fallingPieceCol + col >= data.cols:
                    return False
                elif data.board[data.fallingPieceRow + row][data.fallingPieceCol + col] != 'blue':
                        return False
    return True

def moveFallingPiece(data, drow, dcol): # when called in keypressed, moves the row and col 
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    if fallingPieceIsLegal(data) == False:
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    return True
    
def rotateFallingPiece(data): # allows the piece to be rotated when "up" is called
    tempPiece = data.fallingPiece + []
    tempPieceRow = data.fallingPieceRow
    tempPieceCol = data.fallingPieceCol
    newRow = len(data.fallingPiece[0])
    newCol = len(data.fallingPiece)
    newPiece = [ ([None] * newCol) for row in range(newRow)]
    for col in range(len(data.fallingPiece[0])):
        for row in range(len(data.fallingPiece)):
            newPiece[col][row] = data.fallingPiece[row][len(data.fallingPiece[0])-1-col]
    centerRow = data.fallingPieceRow + len(data.fallingPiece)/2
    oldCenterRow = data.fallingPieceRow + len(data.fallingPiece)/2
    newCenterRow = data.fallingPieceRow + len(newPiece)/2
    data.fallingPieceRow = data.fallingPieceRow + len(data.fallingPiece)//2 - len(newPiece)//2
    data.fallingPieceCol = data.fallingPieceCol + len(data.fallingPiece[0])//2 - len(newPiece[0])//2
    data.fallingPiece = newPiece
    if fallingPieceIsLegal(data) == False: # if the piece rotates but leaves the board, we stop the rotation 
        data.fallingPiece = tempPiece
        data.fallingPieceRow = tempPieceRow
        data.fallingPieceCol = tempPieceCol
    
def placeFallingPiece(data): # if the piece can't go down further, make it part of the board
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col] == True:
                data.board[row + data.fallingPieceRow][col + data.fallingPieceCol] = data.fallingPieceColor
    removeFullRows(data)

def removeFullRows(data): # checks through each row of board to see if no blue is within a row
    fullRows = 0
    newBoard = list()
    for row in range(len(data.board)):
        if 'blue' not in data.board[row]:
            fullRows += 1
        else:
            newBoard.append(data.board[row])
    for extraRow in range(fullRows):
        newBoard.insert(0,['blue']*data.cols)
    data.fullRowScore += (fullRows)**2
    data.board = newBoard

def drawScore(canvas,data): # creates the score on top of the game
    textWidth = data.width/2
    textHeight = data.margin/2
    string = 'Score: ' + str(data.fullRowScore)
    canvas.create_text(textWidth, textHeight, text = string, font = 'Arial 13 bold', anchor = 'center', fill= 'blue')

def keyPressed(event, data):
    if event.keysym == "Left": 
        moveFallingPiece(data,0,-1)
    elif event.keysym == "Right":
        moveFallingPiece(data,0,1)
    elif event.keysym == "Down":
        moveFallingPiece(data,1,0)
    elif event.keysym == "Up":
        rotateFallingPiece(data) # resets game
    if event.keysym == "r":
        init(data)
    
def timerFired(data):
    if data.isGameOver == False: # works while game is not over
        if moveFallingPiece(data, 1, 0) == False: # deals with case in which it is immediately legal
            placeFallingPiece(data)
            newFallingPiece(data)
            if fallingPieceIsLegal(data) == False:  
                data.isGameOver = True
        else: moveFallingPiece(data,1,0) # continues if there is no illegal move immediately
    else: pass
 
def drawCell(canvas, data, row, col, color): # when called, draws the piece seperately from board
    leftX = col * data.cellSize + data.margin
    leftY = row * data.cellSize + data.margin
    rightX = (col * data.cellSize) + data.cellSize + data.margin
    rightY = (row * data.cellSize) + data.cellSize + data.margin
    canvas.create_rectangle(leftX, leftY, rightX, rightY, fill = color, width = 4)
    
    
def drawBoard(canvas,data): # creates the board and is called when updated after row is destroye
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas,data,row,col,data.board[row][col])
    
def redrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width,data.height,fill = 'orange', width = 0)
    drawBoard(canvas,data)
    if data.isGameOver == False:
        drawFallingPiece(canvas,data)
    if data.isGameOver == True:
        leftX = data.margin
        leftY = data.margin + data.cellSize
        rightX = data.width - leftX
        rightY = data.cellSize*2 + leftY
        canvas.create_rectangle(leftX, leftY, rightX, rightY,fill = 'black')
        canvas.create_text((leftX+rightX)/2,(leftY+rightY)/2,anchor = 'center',text = 'Game Over!',fill = 'yellow',font = 'Arial 16 bold')
    drawScore(canvas,data) # calls the score every time to be drawn


def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

playTetris()