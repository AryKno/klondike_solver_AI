from random import randint

class Game:

    #content of the game. game[0]=pile, game[1]=talon, game[2-5]=suits stacks game[6-12] = build stacks
    #the content of the build stack array is from the most covered card to the uncovered
    #same for the others
    game=[[] for i in range(13)]
    game_history = []
    moves_history = []
    newCard_history = [] #save if a card has been faced up or picked up from the talon

    rollout_moves_lists = []


    __color = ["S","H","C","D"]

    available_moves = [] #represent the doable moves, the moves are stored as a tuple (priority,source stack,source card number, destination stack, destination card number)

    def __init__(self):
        self.generateStart()
        self.game_history.append(self.game)
        #print(self.game)


    def generateStart(self): #generate the card and store them in self.game
        index = 0
        nbrCard = 0
        for i in range(6,len(self.game)):
            index +=1
            for j in range(0,index):
                (nbr,color) = self.randomCard()
                faceup = 0
                if j == index - 1:
                    faceup = 1
                self.game[i].append((nbr,color,faceup))
                nbrCard += 1
        #pile
        for i in range(nbrCard,52):
            (nbr,color) = self.randomCard()
            self.game[0].append((nbr,color,1))
    
    def randomCard(self): #return a random card that is not in the game
        exists1 = True
        exists2 = True
        color = 0
        nbr = 0
        while not (exists1 == False and exists2 == False) :
            color = self.__color[randint(0,3)]
            nbr = randint(1,13)
            exists1 = any((nbr,color,0) in x for x in self.game) #check if the value already exist
            exists2 = any((nbr,color,1) in x for x in self.game) #check if the value already exist
        return (nbr,color)

    def isOver(self):
        #the game is over if the 4 suit stacks are full with the same color
        for i in range(2,6): #we check the suit stacks
            l = len(self.game[i])
            if l != 13: #if there is not 13 cards
                return False
            for j in range(0,l):
                if j+1 != self.game[i][j][0]: #if the index of the cart is different from the number of it
                    return False
        return True

    def heuristic(self,move):
        #return the heuristic of a move
        #the moves are stored as a tuple (source stack,source card number, destination stack, destination card number)
        #move between build or talon to suit = 5pt
        if move[2] >= 2 and move[2] <= 5 and ( move[0] >= 6 and move[0] <= 13 or move[0] == 1):
            return 5
        #move between talon to build = 5 pts
        if move [0] == 1 and move[2] >= 6 and move[2] <= 13:
            return 5
        #move between suit stack and build stack
        if move[0] >= 2 and move[0] <= 5 and move[2] >= 6 and move[2] <= 13:
            return -10
        #any moves that don't suits with the startegy above = 0
        return 0

    def differentiateHeuristic(self,move):
        #called if several moves have the highest score, decide between the moves, which one is the best
        #move between build to build
        if move[0] >= 6 and move[0] <= 13 and move[2] >= 6 and move[2] <= 13:
            #if the move empties a stack, priority = 1
            if len(self.game[move[0]][:-1]):
                return 1
            #if the move turn a face-down card, over
            if self.game[move[0]][move[1]-1][2] == 0:
                return len(self.game[move[0]][:-1])+1 #return the number of face down card
        #if the move is between talon and builds
        if move[0] == 1 and move[2] >= 6 and move[2] <= 13:
            #if the move is not a king
            if self.game[move[0]][move[1]][0] != 13:
                return 1
            #if the move is a king and the matching queen is knowned
            if self.game[move[0]][move[1]][0] == 13 and self.cardFacedUp((12,self.game[move[0]][move[1]][1])):
                return 1
            #if the move is a king and its matching queen is unknowed
            if self.game[move[0]][move[1]][0] == 13:
                return -1
        #any other move
        return 0

    def availableMoves(self):
        #we go on every build stacks,we try every possibilies :
        #   -build ->

        #we go through the build stacks and suits stack
        for i in range(6,len(self.game)):
            for j in range(0,len(self.game[i])):
                #we go through the cards...
                if self.game[i][j][2]: #...that are faced up
                    for k in range(2,len(self.game)): #we go through the others build and suits stacks
                        if k != i: #if the destination build stack is different from the source one
                            mv = [0,i,j,k,len(self.game[k])-1] #we can only add at the bottom of a build stack
                            if self.moveIsLegal(mv): #if the move is legal we add it at the end
                                self.available_moves.append(mv)
        
        #we test the top card of the talon
        if len(self.game[1]) > 0:
            #if there's at least one card
            for k in range(2,len(self.game)): #we go through the others build and suits stacks
                #print("CA TEST LES SUITS")
                mv = [0,1,len(self.game[1])-1,k,len(self.game[k])-1] #we can only add at the bottom of a build stack
                if self.moveIsLegal(mv): #if the move is legal we add it at the end
                    self.available_moves.append(mv)
                           
        #we test the availables moves from suits to build
        #for i in range(2,6):


        if len(self.available_moves) == 0:
            #No moves are availables, we deal the pile
            return False
        else:
            #print("PAS DE MOVE POSSIBLE")
            return True
    
    def evaluateMoves(self,moves_list):
        #we evaluate the priority for the first time
        for move in moves_list:
            priority = self.heuristic([move[1],move[2],move[3],move[4]])
            move[0] = priority
            #we update the priority

        maxPriority = -1000
        for each in moves_list:
            if each[0] > maxPriority:
                maxPriority = each[0]
        
        tmp = [] #we update the moves_list to keep only the best moves
        for each in moves_list:
            if each[0] == maxPriority:
                tmp.append(each)

        if(len(tmp)>1):
            #there's several moves at the maximum value, we use the other priority calculator
            for move in tmp:
                priority = move[0] + self.differentiateHeuristic([move[1],move[2],move[3],move[4]])+move[0] #we had the previous calculated heuristic to the new one
                move[0] = priority
            maxPriority = -1000
            for each in tmp:
                if each[0] > maxPriority:
                    maxPriority = each[0]
            
            tmp2 = [] #we update the moves_list to keep only the best moves
            for each in tmp:
                if each[0] == maxPriority:
                    tmp2.append(each)
            #print("content of tmp after differentiate",end="")
            #print(tmp2)
            #print(moves_list)
            return tmp2.copy()
        else:
            return tmp.copy()
        #print("Moves at the end of evaluateMoves : ",end="")
        #print(len(self.available_moves))
        #return a list that contains the index of the bests moves in self.available_moves

            
    def play(self):
        if self.availableMoves():
            print("Available move at the beginning : ",end="")
            print(self.available_moves)
            #if there is at least one available move
            self.available_moves = self.evaluateMoves(self.available_moves) #generate the priorities and give back the priority_list
            #print("Available move after evaluateMoves : ",end="")
            #print(self.available_moves)

            #We check if one of the move is repetitiv
            #we execute the only move chosen
            tmp = []
            for i in range(0,len(self.available_moves)):
                isRepetitive = self.repetitiveMove(self.available_moves[i]) #test if the opposite move happened at the previous turn
                if not isRepetitive: #is Repetitive ?
                    tmp.append(self.available_moves[i])

            self.available_moves = tmp.copy()
            print("Available move after repetitiv check : ",end="")
            print(self.available_moves)

            if len(self.available_moves)>0:
                #if there's no move after the repetition check
                if len(self.available_moves) > 1: #if there's several maximums
                    rdmNbr = randint(0,len(self.available_moves)-1)
                    #print("Aléatoire ",end="")
                    #print(rdmNbr)
                    maxMove = rdmNbr
                else:
                    maxMove = 0

                self.makeMove(self.available_moves[maxMove])
                #we add the move to the history
                print(self.available_moves[maxMove])
                self.moves_history.append(self.available_moves[maxMove])
                #we add the move to the move_history
                print("Available move at the end : ",end="")
                print(self.available_moves)
                #self.defeat(self.available_moves[0])

            else:
                #the move is repetitive
                self.dealPile()
                # we deal the pile
                #we add the move to the history, the deal of the pile is represented by a 4-zero tuple
                self.moves_history.append([0,0,0,0,0])
                print("dealPile, to prevent juggle")
                #self.defeat([0,0,0,0,0])

            self.available_moves.clear()
            

        else:
            #if there is no move available
            self.dealPile()
            #if no moves are possible, we deal the pile
            #we add the move to the history, the deal of the pile is represented by a 4-zero tuple
            self.moves_history.append([0,0,0,0,0])
            print("dealPile, no moves")


        
        self.game_history.append(self.saveGame())
        
        #we clean the available_moves to do another play


    def playRollout(self,depth):
        #################################"WE CHECK THE MOVES"###########################
        moves = []
        if self.availableMoves():
            #if there is at least one available move
            moves = self.evaluateMoves(self.available_moves) #generate the priorities and give back the priority_list
            self.available_moves.clear() #we clear this in order for not having the moves in the rollout
            #print("Available move after evaluateMoves : ",end="")
            #print(self.available_moves)

            #We check if one of the move is repetitiv
            #we execute the only move chosen
            tmp = []
            for i in range(0,len(moves)):
                isRepetitive = self.repetitiveMove(moves[i]) #test if the opposite move happened at the previous turn
                if not isRepetitive: #is Repetitive ?
                    tmp.append(moves[i])

            moves = tmp.copy()


            #If no moves anymore, we deal the pile
            if len(moves) <= 0:
                moves.append([0,0,0,0,0])
        else:
            moves.append([0,0,0,0,0])

        print("playRollout.available_moves prior to loop ")
        print(moves)

        for i in range(0,len(moves)):
            #pour chaque move dispo, on test leur valeur
            #we play the game in order to test the next moves
            if moves[i] == [0,0,0,0,0]:
                self.dealPile()
            else:
                self.makeMove(moves[i])
            #we save the move and the game status
            self.moves_history.append(moves[i])
            self.game_history.append(self.saveGame())
            print("playRollout.inFor.lenGameHistory")
            print(len(self.game_history))
            #we do a rollout
            print("playRollout.inFor.move[i]")
            print(moves[i])
            self.iterationRollout(depth-1,depth)
            self.resetPrevMove()
            #ne pas oublier de supprimer le move précédent de l'historique des moves, l'état de jeu précédent, le newCard précédent
        
        #we debug : we display the moves lists
        print("----------------------END OF THE SEARCH--------------")
        print("playRollout.afterForSearch.rollout_moves_lists")
        for each in self.rollout_moves_lists:
            print(each)

        #we choose the moves with the maximum power
        maxI = -1
        maxV = -5000
        for i in range(0,len(self.rollout_moves_lists)):
            if self.rollout_moves_lists[i][-1] > maxV:
                maxI = i
                maxV = self.rollout_moves_lists[i][-1]
        
        #We execute the moves of the moves_list
        for i in range(0,len(self.rollout_moves_lists[maxI])-1): #-1 because the last index is the value of the moves list
            if self.rollout_moves_lists[maxI][i] == [0,0,0,0,0]:
                self.dealPile()
            else:
                self.makeMove(self.rollout_moves_lists[maxI][i])
            #we save the move and the game status
            self.moves_history.append(self.rollout_moves_lists[maxI][i].copy())
            self.game_history.append(self.saveGame())

        self.rollout_moves_lists.clear()
        print("Moves dones : ")
        print(self.moves_history)
        print("playRollout.newCard_history")
        print(self.newCard_history)
        print("#####################################################################################################################################")


    def iterationRollout(self,depth,maxDepth):
        print("ITERATION N° :",end="")
        print(depth)
        if self.isOver():
            print("victory rollout")
            self.addRolloutMove(maxDepth)
            self.rollout_moves_lists[-1].append(1000) #we append the value of the moves_list
            return 
        
        if self.defeat(self.moves_history):
            print("defeat rollout")
            self.addRolloutMove(maxDepth)
            self.rollout_moves_lists[-1].append(-1000) #we append the value of the moves_list
            return 

        if(depth <= 0):
            #we add the moves_list to the list of moves_list
            print("end of depth")
            self.addRolloutMove(maxDepth)
            self.rollout_moves_lists[-1].append(self.evaluateGame()) #we append the value of the moves_list
            print(self.rollout_moves_lists[-1])
            return

        #################################"WE CHECK THE MOVES"###########################
        moves = []
        if self.availableMoves():

            #if there is at least one available move
            moves = self.evaluateMoves(self.available_moves) #generate the priorities and give back the priority_list
            self.available_moves.clear()
            #print("Available move after evaluateMoves : ",end="")
            #print(moves)

            #We check if one of the move is repetitiv
            #we execute the only move chosen
            tmp = []
            for i in range(0,len(moves)):
                isRepetitive = self.repetitiveMove(moves[i]) #test if the opposite move happened at the previous turn
                if not isRepetitive: #is Repetitive ?
                    tmp.append(moves[i])

            moves = tmp.copy()

            #If no moves anymore, we deal the pile
            if len(moves) <= 0:
                moves.append([0,0,0,0,0])
        else:
            moves.append([0,0,0,0,0])

        print("iterationRollout.available_moves,iter = ",end="")
        print(depth)
        print(" prior to loop : ")
        print(moves)
        for i in range(0,len(moves)):
            #pour chaque move dispo, on test leur valeur
            #we play the game in order to test the next moves
            if moves[i] == [0,0,0,0,0]:
                self.dealPile()
            else:
                self.makeMove(moves[i])
            #we save the move and the game status
            self.moves_history.append(moves[i])
            self.game_history.append(self.saveGame())
            print("playRollout.inFor.lenGameHistory")
            print(len(self.game_history))
            print(self.moves_history)
            print("playRollout.inFor.move[i]")
            print(moves[i])

            #we do a rollout
            self.iterationRollout(depth-1,maxDepth)
            self.resetPrevMove()
            #ne pas oublier de supprimer le move précédent de l'historique des moves, l'état de jeu précédent, le newCard précédent
        return
        
    def evaluateGame(self):
        #evaluate the game value, used by the rollout algorithm
        count = 0
        for i in range(2,6):
            count += len(self.game[i])
        return count


    def addRolloutMove(self,depth):
        #add the moves_list and remove the history
        self.rollout_moves_lists.append(self.moves_history[-depth:].copy())
        #we get the last moves

    def resetPrevMove(self):
        del self.game_history[-1]
        del self.moves_history[-1]
        print("resetPrevMove.newCard_history")
        print(self.newCard_history)
        del self.newCard_history[-1]

    def cardFacedUp(self,card):
        #return true if the card is in the talon, the pile, the suits or faced up in the build stacks
        for i in range(0,len(self.game)):
            if (card[0],card[1],1) in self.game[i]:
                return True
        return False

    def moveIsLegal(self,move):
        #return true if a move represented by the tuple (priority,source_stack,source_card,destination_stack,destination_card) is legal
        #from x stack to builds
        #print(move)
        if move[1]>=6 and move[1]<=12:
            #the source is a build
            if self.game[move[1]][move[2]][0] == 13 and move[2] == 0 and move[3]>=6 and move[3]<=13: #if the card is a king that is at the end of a build stack and if the move is between builds
                return False
        if move[3] >= 6 and move[3] <= 12:
            #the destination is a build stack
            if len(self.game[move[3]]) == 0:
                #the build stack is empty
                return self.game[move[1]][move[2]][0] == 13
                #the first card must be a king
            else:
                return self.game[move[1]][move[2]][0] == self.game[move[3]][move[4]][0]-1 and self.cardIsRed(self.game[move[1]][move[2]][1]) != self.cardIsRed(self.game[move[3]][move[4]][1])
                #true if the source card's number is lower and if the colors are differents
        #from x stack to suits
        if move[3] >= 2 and move[3] <= 5:
            if move[2] == len(self.game[move[1]])-1: #In any case, a card that is moved to a suit stack is at the end of its stack
                if len(self.game[move[3]]) == 0:
                    #if the suit stack is empty
                    return self.game[move[1]][move[2]][0] == 1
                    #the first card must be an Ace
                else:
                    return self.game[move[1]][move[2]][0] == self.game[move[3]][move[4]][0]+1 and self.game[move[1]][move[2]][1] == self.game[move[3]][move[4]][1]
                    #true if the source card's number is higher and if the symbol are the same
            else:
                return False
    def cardIsRed(self,card):
        #return true if a card is red, the card is the letters 'S','C','H','D'
        return card == 'D' or card == 'H'

    def makeMove(self,move):
        #update the game list
        #move is a tuple/list (priority,source stack,source index,destination stack, destination index)
        self.game[move[3]].extend(self.game[move[1]][move[2]:])
        del self.game[move[1]][move[2]:] #we delete the old position


        #we faced-up the card faced-down, in the case of a build move
        if move[1] >= 6 and move[1] <= 12:
            #if the move come from a build stack
            if len(self.game[move[1]])>0: #if there is at least one card in the build stack
                tmp = self.game[move[1]][move[2]-1]
                del self.game[move[1]][move[2]-1]
                self.game[move[1]].append((tmp[0],tmp[1],1))
                if tmp[2] == 0:
                    self.newCard_history.append(1) #we had the fact that a new card has been discovered
                else:
                    self.newCard_history.append(0)
                #we remove the previous tuple, and we had the same one but with the faced up
        else:
            #if the card come from the talon, we indicate that a new card has been discovered
            if move[1] == 1:
                self.newCard_history.append(1)
            else:
                self.newCard_history.append(0)


    def dealPile(self):
        #deal the pile
        if(len(self.game[1]) > 0):
            print("Talon is not empty")
            #if the talon is not empty
            self.game[0] = self.game[1][::-1] + self.game[0] 
            #We put the cards of the talon at the bottom of the pile (at the beginning of the list)
            self.game[1].clear()
            #We clear the talon
        #we add the last three card of the pile to the talon
        self.game[1].extend(self.game[0][::-1][:3])
        
        del self.game[0][-3:]
        #we deal the pile

        #no new card discovered, we save this info
        self.newCard_history.append(0)


    def defeat(self,moves_list):
        #this function check the move_history and the game, for any dead end
    
        if len(self.moves_history)>11:
            #if the game history contains at least 12 moves
            t = moves_list[-1] #the last move
            if t == (0,0,0,0,0):
                #if the last move is a deal of the pile
                for i in range(1,11): #we check if the last 10 moves are to deal the Pile
                    if self.game_history[-i] != t:
                        print("DEFEAT DETECTED")
                        return True #there's several deal of pile in the row, the game is in a dead end
            #test if there's an exchange between stacks and if there is dealPile between them
            if t[1] >= 6 and t[1] <= 13 and t[3] >= 6 and t[3] <= 13:
                #if the game is stuck in a juggle between builds
                count = 0
                for i in range(1,len(self.moves_history)+1):
                    prev = self.moves_history[-i]
                    if prev == (0,0,0,0,0):
                        count += 1
                    else:
                        if count >=5:
                            if (t[1] == prev[1] and t[3] == prev[3]) or (t[1] == prev[3] and t[3] == prev[1]):
                                #there's a juggle between 
                                return True
            
        #we check if anynew card has not been discovered for a while
        count = 0
        if len(self.game[1])>=0:
            if len(self.newCard_history)>15:
                for i in range(1,15):
                    print(count)
                    count +=1
                    if self.newCard_history[-i] == 1:
                        print("carte découverte")
                        return False #no defeat
                if count >=10:
                    return True
        
        return False #no defeat

            

    def repetitiveMove(self,move):
        #return true if the move is repetitiv
        #check if the move is only between builds or between suits or between builds and suits
        if move[1] >= 2 and move[1] <= 13 and move[3] >= 2 and move[3] <= 13:
            if(len(self.moves_history)>9):
                #check if there is a build 1 -> build 2 and a build 2 -> build 1
                for i in range(1,8):#len(self.moves_history)+1): #we go through the game history
                    prevMove = self.moves_history[-i]
                    if move[1] == prevMove[3] and move[2] == prevMove[4]+1 and move[3] == prevMove[1] and move[4] == prevMove[2]-1:
                        #if the move is between the same two builds stacks
                        prevGame = self.game_history[-i-1]       #A fonctionné avec -i-1
                        if prevGame[prevMove[1]][prevMove[2]] == self.game[move[1]][move[2]]: #if the card moved in n-1 is equal to the card moved in n
                            return True #then the move is a juggle between two stacks
        return False

    def saveGame(self):
    #return a copy of the game board
        ret = []
        for each in self.game:
            ret.append(each.copy())
        return ret



                






