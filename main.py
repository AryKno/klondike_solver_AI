from Window import Window
from Game import Game
from tkinter import *
import time


global game
global fen
iteration = 0
    

def playCallBack():
    game.play()
    #print("available moves : ",end="")
    #print(game.available_moves)
    fen.buildGame()
    if game.isOver():
        fen.endGame(True)
        print("Game won !!!")
    if game.defeat(game.moves_history):
        fen.endGame(False)
        print("GAME LOST")
    print("MOVES HISTORY : ")
    print(game.moves_history)
    print("newCard HISTORY : ")
    print(game.newCard_history)

def playRolloutCallBack():
    game.playRollout(30)
    #print("available moves : ",end="")
    #print(game.available_moves)
    fen.buildGame()
    if game.isOver():
        fen.endGame(True)
        print("Game won !!!")
    if game.defeat(game.moves_history):
        fen.endGame(False)
        print("GAME LOST")






game = Game()
print("€€€€€€€€€€€€€€€€€€€€€€€€€")
#game.game[0][-3] = (1,'H',1)
#game.game[0][-2] = (2,'H',1)
#game.game[0][-1] = (3,'H',1)

fen = Window(playRolloutCallBack,game.game)

print("################ We get available moves ###########")
#print("################ We evaluate ###########")
#print("################ We play ###########")
#game.play()
#print("################ New game ################")
#print(game.game)
#print(game.moveIsLegal((0,6,0,7,1)))
#print("############### Window \"game\" value")
#print(game.game)
#print(fen.game == game.game)
fen.buildGame()

fen.window.mainloop()
