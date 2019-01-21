from tkinter import *

class Window:

    imgList = []
    symbDic = { 'S': "\u2660", 'H': "\u2665", 'D': "\u2666", 'C': "\u2663"}
    __characters = {1:"A",11:"J",12:"Q",13:"K"}

    #content of the game. game[0]=pile, game[1]=stack, game[2-5]=suits stacks game[6-12] = build stacks
    #the content of the build stack array is from the most covered card to the uncovered
    #same for the others

    game=[]





    

    def __init__(self,callBackButton,game=None):
        self.window = Tk()
        
        self.window.geometry("1000x700")
        self.window.resizable(width=False,height=False) #On bloque la redimension de la fenetre
        self.B = Button(self.window, text ="Next move",command=callBackButton)
        self.B.pack()
        self.createGame()
        #self.drawCard((50,10),(1,'S')) 
        #self.drawCard((50,30),(5,'C'))
        #self.drawCard((50,50),(5,'H'))
        #self.drawCard((50,70),(5,'D'))
        if game==None:
            self.game.append([(3,"D",0),(5,"H",0),(5,"H",0),(2,"S",0),(3,"D",0),(5,"H",0),(2,"S",0),(3,"D",0),(5,"H",0),(5,"H",0),(2,"S",0),(3,"D",0),(5,"H",0),(2,"S",0),(3,"D",0),(5,"H",0),(2,"S",0),(3,"D",0),(5,"H",0),(5,"H",0),(2,"S",0),(3,"D",0),(5,"H",0),(2,"S",0)]) #24
            self.game.append([(3,"D",1),(3,"D",1),(3,"D",1)])
            self.game.append([(3,"D",1)])
            self.game.append([(3,"D",1)])
            self.game.append([(3,"D",1)])
            self.game.append([(3,"D",1)])

            self.game.append([(2,"S",1)])
            self.game.append([(3,"D",0),(5,"H",1)])
            self.game.append([(3,"D",0),(5,"H",0),(5,"H",1)])
            self.game.append([(3,"D",0),(5,"H",0),(2,"S",0),(3,"D",1)])
            self.game.append([(3,"D",0),(5,"H",0),(5,"H",0),(2,"S",0),(3,"D",1),])
            self.game.append([(3,"D",0),(5,"H",0),(3,"D",0),(5,"H",0),(2,"S",0),(2,"S",1)])
            self.game.append([(3,"D",0),(5,"H",0),(5,"H",0),(2,"S",0),(3,"D",0),(5,"H",0),(2,"S",1)]) #28
        else:
            self.game = game
        
        self.buildGame()

    

    def createGame(self):
        self.canvas = Canvas(self.window,bg="green",borderwidth=5)
        self.canvas.pack(fill="both",expand="yes")
    
    def drawCard(self,pos,card):
        #draw the card "card" at the position "pos"
        #card are of type (number,symbol)
        assert(type(card) == type((1,'a',1)) and type(pos) == type((1,1)) and len(card)==3 and len(pos)==2)
        fill = "white"
        outline = "black"
        if card[2] == 0:
            fill = "blue"
            outline = "white"

        self.canvas.create_rectangle(pos[0], pos[1], pos[0]+100, pos[1]+140, fill=fill,outline=outline)
        if card[2] == 0:
            return
        if card[1] == 'D' or card[1] == 'H':
            color = "Red"
        else:
            color = "Black"
        nbr = ""
        if card[0] == 1 or card[0] > 10:
            nbr = self.__characters[card[0]]
        else:
            nbr = card[0]


        self.canvas.create_text(pos[0]+15,pos[1]+15,fill=color,font="Arial 12 bold",text=nbr)

        #self.imgList.append(PhotoImage(file=self.symbDic[card[1]])) #Utiliser les caractères unicode!!!

        #self.canvas.create_image(pos[0]+80, pos[1]+15, image=self.imgList[-1])
        self.canvas.create_text(pos[0]+80,pos[1]+15,fill=color,font="Arial 14 bold",text=self.symbDic[card[1]])
        self.canvas.create_text(pos[0]+15,pos[1]+30,fill=color,font="Arial 14 bold",text=self.symbDic[card[1]])

        self.window.update()
    
    def buildGame(self):
        #draw the entire game
        self.canvas.delete("all")
        color = "blue"
        if not self.game[0]:
            color = "black"

        #we create the card of the pile
        if len(self.game[0]) >= 1:
            self.canvas.create_rectangle(10, 10, 110, 150, fill=color,outline="white") #we draw an empty slot
        else:
            self.canvas.create_rectangle(10, 10, 110, 20, fill="green",outline="white") #we draw an empty slot
            self.canvas.create_oval(35,45,85,95,fill="green", outline="forestgreen",width=4)
            print("No card")
        
        #we create the talon
        if len(self.game[1]) == 0:
            self.canvas.create_rectangle(130, 10, 230, 150, fill='green',outline="white") #we draw an empty slot
            #we draw an empty card
        else:
            i=1
            for each in self.game[1]:
                self.drawCard((130+i*25,10),each)
                i+=1

        
        #We create the cards of the suits stacks
        for i in range(2,6): #display the last card of the first stacks
            if len(self.game[i])==0: #if there's no card ?
                self.canvas.create_rectangle(i*120+130, 10, i*120+230, 150, fill='green',outline="white") #we draw an empty slot
            else:
                self.drawCard((120*i+120,10),self.game[i][-1])

        #we create the cards of the build stacks
        for i in range (6,len(self.game)):
            if len(self.game[i])> 0:
                for j in range (0,len(self.game[i])):
                    self.drawCard((10+120*(i-6),200+j*25),self.game[i][j])
            else:
                self.canvas.create_rectangle(10+120*(i-6), 200, 110+120*(i-6), 340, fill='green',outline="white") #we draw an empty slot


    def endGame(self,isVictory):
        if isVictory:
            color = "green3"
            text = "GAME OVER : VICTORY !"
        else:
            color = 'orange'
            text = "GAME OVER : DEFEAT."
        
        #we remove the button
        self.B.pack_forget()

        self.canvas.create_text(500,350,fill=color,font="Arial 30 bold",text=text)


        



        



    
