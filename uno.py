numbers = ['0','1','2','3','4','5','6','7','8','9']
colors = ['Red','Yellow','Green','Blue','Any']
wilds = ['(W)ild','Draw (F)our']
specials = ['Re(V)erse','(S)kip','Draw (T)wo']
deck = {'Red':{},'Blue':{},'Yellow':{},'Green':{},'Any':{}}
skipComp=False
skipPlayer=False

import random
import operator

##red = {
##    color: 'red',
##    '1':2,
##    '2':2
##    }
##
##deck = {
##    red:{
##        '1':2,
##        '2':2
##        }
##    blue:{
##        '1':2,
##        '2':2
##        }
##    }


def makeDeck (deck):
    """Constructs the deck dictionary with the four colors as keys. The values of each are dictionaries /
    In those dictionaries the cards are the keys and the amount of each card is the value."""
    for color in colors:
        if color=='Any':
            for wild in wilds:
                deck[color][wild]=4
        else:
            for number in numbers:
                 
                if number == '0':
                    deck[color][number]=1
                else:
                    deck[color][number]=2
            for special in specials:
                deck[color][special]=2
            
           
    
    return deck




def dealHands(deck):
    """creates players hand and computer hand - each hand is a list of lists. each card is a list"""
    playerHand=[]
   # playHandDict={}
    compHand=[]

    for i in range (1,8):#picks 7 random cards for player
        dealtColor =  random.choice(deck.keys())
        dealtCard = random.choice(deck[dealtColor].keys())

        while deck[dealtColor][dealtCard]<=0: #makes sure its still in the deck
             dealtColor =  random.choice(deck.keys())
             dealtCard = random.choice(deck[dealtColor].keys())
        
            
        playerHand.append([dealtColor,dealtCard])
       # playHandDict[dealtColor]=dealtCard
        #print "Dictionary is ", playHandDict

       # print "You:" , dealtColor, dealtCard
        deck[dealtColor][dealtCard] -=1
#picks 7 random cards for computer
        dealtCompColor= random.choice(deck.keys())
        dealtCompCard = random.choice(deck[dealtCompColor].keys())

        while deck[dealtCompColor][dealtCompCard]<=0:
            dealtCompColor= random.choice(deck.keys())
            dealtCompCard = random.choice(deck[dealtCompColor].keys())

        compHand.append([dealtCompColor,dealtCompCard])

        #print "Computer: ", dealtCompColor, dealtCompCard
        deck[dealtCompColor][dealtCompCard] -=1

        hands = [compHand,playerHand]
        
    return hands

def printHand(hand):

    """displayes the hands on one line in proper formatting"""
    for i in range(len(hand)):
        if hand [i][0]=='Any':
            print hand[i][1]," ",
        else:
            print hand[i][0],hand[i] [1]," ",
            #print "not working"


def discard(deck):
    """Selects the first card from the deck to be turned over at the beginning of the game"""


    discardColor= random.choice(deck.keys())
    discardCard = random.choice(deck[discardColor].keys())

    while deck[discardColor][discardCard]<=0 or  discardColor=='Any' :
        discardColor= random.choice(deck.keys())
        discardCard = random.choice(deck[discardColor].keys())

    deck[discardColor][discardCard] -=1
    turnCard = [discardColor,discardCard]
    
    return turnCard

def checkCard(card,turnCard):
    "Takes the list 'card' and checks it against the face up card to see if it is playable"
    if card[0] == 'Any':
        return True
    elif card [0] == turnCard[0] or card[1] == turnCard[1]:
        return True
    else:
        return False
    
    
def drawCard():
    """Draws a new card and checks to see if it is playable."""
    drawColor= random.choice(deck.keys())
    drawNumber = random.choice(deck[drawColor].keys())

    while deck[drawColor][drawNumber]<=0:
        drawColor= random.choice(deck.keys())
        drawNumber = random.choice(deck[drawColor].keys())

    deck[drawColor][drawNumber] -=1
    newCard = [drawColor,drawNumber]

    return newCard

def newColor():
    pickColor=""
    while pickColor.lower()!='r' and pickColor.lower()!='b' and pickColor.lower()!='g' and \
          pickColor.lower()!='y':
        pickColor=raw_input ("What color would you like this to be: (r)ed, (g)reen, (y)ellow, or (b)lue?")
        if pickColor.lower()=='r':
            turnCard[0]='Red'
        elif pickColor.lower()=='b':
            turnCard[0]='Blue'
        elif pickColor.lower()=='y':
            turnCard[0]='Yellow'
        elif pickColor.lower()=='g':
            turnCard[0]='Green'
        else:
            print "That is not a valid color."
    
                
           
    

def playCards(hand,turnCard):
    """Takes the players input String and selects the right card from player's hand
    Makes sure the card is actually in the hand. Hand is a list of tuples."""
    canPlayDrawFour=True
    haveWild=False
    yourColor = "Invalid"
    yourNumber = "Invalid"
    global skipComp
    for cards in range(len(hand)): #checks to see if you can play a draw four (if you have a match to the discard)
        if hand[cards][0] == turnCard[0] or (hand[cards][1] == turnCard[1] and \
                                             turnCard[1]!= 'Draw (F)our' and \
                                             turnCard[1] !='(W)ild'):
            canPlayDrawFour = False
            break
    for cards in range(len(hand)):#checks to see if you have any wilds
        if hand[cards][0] == 'Any':
            haveWild=True
            break

    if canPlayDrawFour == True and haveWild == False:#If you can't play any cards you draw
        print "You do not have a playable card. Time to draw."
        newCard = drawCard()

        if newCard[1]=="(W)ild" or newCard[1]=="Draw (F)our":
            print "You draw and play",newCard[1]
            turnCard[1]=newCard[1]
            if newCard[1]=='Draw (F)our':
                skipComp==True
                print "The computer draws four cards."
                for i in range (4):
                    compHand.append(drawCard())
            newColor()
        elif checkCard(newCard,turnCard):
            print "You draw and play",newCard[0],newCard[1]
            turnCard=newCard
            if turnCard[1]=='Draw (T)wo' or turnCard[1] == '(S)kip':
                skipComp=True
                if turnCard[1]=='Draw (T)wo':
                    for i in range (2):
                        compHand.append(drawCard())
        else:
            print"You draw",newCard[0],newCard[1],"Sorry. You can't play it."
            hand.append(newCard)
        
        
    else:
        
        print
        cardPlay=raw_input("""Please play a card. Enter the first letter of the color and the number. 
        For the special cards, enter the letter in parentheses.""")

        if len(cardPlay) == 2:#assigns 'yourColor' and 'yourNumber' to the card names
            if cardPlay[0].lower() == 'r':
                yourColor='Red'
            elif cardPlay[0].lower() == 'b':
                yourColor = 'Blue'
            elif cardPlay [0].lower() == 'y':
                yourColor = 'Yellow'
            elif cardPlay [0].lower() == 'g':
                yourColor = 'Green'
           

            if ord(cardPlay[1]) in range (48,58):
                yourNumber = cardPlay[1]
            elif cardPlay[1].lower() == 's':
                yourNumber = 'Skip'
            elif cardPlay[1].lower() == 'v':
                yourNumber = 'Reverse'
            elif cardPlay[1].lower() == 't':
                yourNumber = "Draw Two"
           
          

            
        elif len(cardPlay) == 1:
            if cardPlay.lower()=='w':
                yourColor = 'Any'
                yourNumber = 'Wild'
            elif cardPlay.lower() == 'f':
                yourColor = 'Any'
                yourNumber = 'Draw Four'
       
     
        for cards in range(len(hand)):

            if (yourNumber == 'Wild' and hand[cards][1]=='(W)ild') or \
               (yourNumber == 'Draw Four' and hand[cards][1]=="Draw (F)our" and canPlayDrawFour==True):
                
                print "You discard", hand[cards][1]
                turnCard[1]=hand[cards][1]
                hand.remove(hand[cards])
                if turnCard[1]=="Draw (F)our" and len(hand)>0:
                    skipComp=True
                    print 'The computer draws four cards.'
                    for i in range(4):
                        compHand.append(drawCard())
                
                if len(hand)>0:
                    newColor()
                break
                
            elif len(cardPlay)==2 and yourColor ==hand[cards][0] and \
                (yourNumber ==hand[cards][1] or \
                 (yourNumber == 'Reverse' and hand[cards][1]=='Re(V)erse') or \
                 (yourNumber == 'Skip' and hand[cards][1]=='(S)kip') or \
                 (yourNumber == 'Draw Two' and hand[cards][1]=='Draw (T)wo')):

                 if checkCard(hand[cards],turnCard):
                    
                    print "You discard",hand[cards][0],hand [cards][1]
                    turnCard=hand[cards]
                    hand.remove(hand[cards])
                    if turnCard[1]=='Draw (T)wo' or turnCard[1] == '(S)kip':
                        skipComp=True
                    if turnCard[1]=='Draw (T)wo' and len(hand)>0:
                        print "The computer draws two cards."
                        for i in range(2):
                            compHand.append(drawCard())
                    break
                 else:
                    print "You can't play that card."
                    playCards(hand,turnCard)
                    break
        else:
            print
            print "You haven't chosen a valid card."
            printHand(hand)
            handAndTurn = playCards(hand,turnCard)
            hand=handAndTurn[0]
            turnCard=handAndTurn[1]
         
    handAndTurn=[hand,turnCard]
    return handAndTurn
            
        
def playCompHand (hand,turnCard):
    """Plays the computer's hand"""
    colors = {
        'Blue':0,
        'Yellow':0,
        'Green':0,
        'Red':0
        }

    global skipPlayer
    for cards in range(len(hand)):

          if hand[cards][0]!='Any' and (hand[cards][0] == turnCard[0] or hand [cards][1] == turnCard[1]):
                
                print "The computer plays",hand[cards][0],hand[cards][1]
                turnCard=hand[cards]
                hand.remove(hand[cards])
                if turnCard[1]=='Draw (T)wo' or turnCard[1]=='(S)kip':
                    skipPlayer=True
                    if turnCard[1]=='Draw (T)wo':
                        print 'You draw two cards.'
                        for i in range(2):
                            playerHand.append(drawCard())
                print "The computer has",len(hand),"cards left."
                break
    else:
        
         for cards in range(len(hand)):
             if hand[cards][0] == 'Any':
               
                print "The computer plays",hand[cards][1]
                turnCard = hand[cards]
                hand.remove(hand[cards])
                if turnCard[1]=='Draw (F)our':
                    skipPlayer = True
                    print "You draw four cards."
                    for i in range (4):
                        playerHand.append(drawCard())
                if len(hand)==0:
                    break
                
                print "The computer has",len(hand),"cards left."

               
                for cards in range(len(hand)):
                    if hand[cards][0] in colors.keys():
                        colors[str(hand[cards][0])]+=1
                turnCard[0] = max(colors.iteritems(),key=operator.itemgetter(1))[0]
                if len(hand)>0:
                      print "The computer picks",turnCard[0],"as the color."
              
                break
         
         else:
            print "The computer draws a card."
            compNewCard=drawCard()

            if compNewCard[0]=='Any':
                print "The computer draws and plays",compNewCard[1]
                turnCard[1]=compNewCard[1]
                if turnCard[1]=='Draw (F)our':
                      skipPlayer=True
                      print "You draw four cards."
                      for i in range (4):
                          playerHand.append(drawCard())
                colors = {
                    'Blue':0,
                    'Yellow':0,
                    'Green':0,
                    'Red':0
                    }
                for cards in range(len(hand)):#chooses the wild color based on which color computer has most
                    if hand[cards][0] in colors.keys():
                        colors[str(hand[cards][0])]+=1
                turnCard[0] = max(colors.iteritems(),key=operator.itemgetter(1))[0]
                print "The computer picks",turnCard[0],"as the color."
            elif checkCard(compNewCard,turnCard):
                print "The computer draws and plays",compNewCard[0],compNewCard[1]
                turnCard[0]=compNewCard[0]
                turnCard[1]=compNewCard[1]
                if compNewCard[1]=='(S)kip' or compNewCard[1]=='Draw (T)wo':
                      skipPlayer=True
                      if compNewCard[1]=='Draw (T)wo':
                          print "You draw two cards."
                          for i in range(2):
                              playerHand.append(drawCard())
                
            else:
                print "The computer draws a card but cannot play it."
                hand.append(compNewCard)
                
            
            
    handAndTurn=(hand,turnCard)
    return handAndTurn
            

print "Welcome to Uno! Let's deal some cards!"

makeDeck(deck)


hands = dealHands(deck)
compHand = hands[0]
playerHand = hands[1]

    
print "Your hand is :"
printHand(playerHand)
print
turnCard = discard(deck)
if turnCard[0]=='Any':
    print "The first card turned over is ", turnCard[1]
else:
    print "The first card turned over is ",turnCard[0],turnCard[1]
    if turnCard[1]=='(S)kip' or turnCard[1]=='Draw (T)wo':
        skipPlayer=True
        if turnCard[1]=='Draw (T)wo':
            print "You draw two cards."
            for i in range (2):
                playerHand.append(drawCard())

while compHand or playerHand:  

    skipComp=False
   
    if not skipPlayer:
        handAndTurn = playCards(playerHand,turnCard)
        playerHand=handAndTurn[0]
        turnCard=handAndTurn[1]
       
        
    else:
        print "Your turn is skipped."

    if not playerHand:
        break
    
    skipPlayer=False

    if not skipComp:
        handAndTurn = playCompHand(compHand,turnCard)
        turnCard = handAndTurn[1]
        compHand=handAndTurn[0]
       
        
    else:
        print "The computer's turn is skipped."
    if not compHand:
        break
   
    print "Your hand is ",
    printHand(playerHand)
    print

if not playerHand:
    print "You win!"
else:
    print "The computer wins. Sorry."
