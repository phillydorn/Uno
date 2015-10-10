
skipComp=False
skipPlayer=False

import random
import operator
from deck import Deck
from deck import Hand



def dealHands(deck):
  for x in range(7):
    playerHand.addCard(deck.dealCard())
    compHand.addCard(deck.dealCard())





def printHands():
    print "Your hand is " + str(playerHand)
    print "The computer has " + str(compHand.countCards()) + " cards."

def drawCards(num):
  for x in range(num):
    playerHand.addCard(deck.dealCard())

def dealFirstCard():

  turnCard = deck.dealCard()

  if turnCard.getNumber() == "Draw (F)our" or turnCard.getNumber() == "(W)ild":
    deck.returnCard(turnCard)
    return dealFirstCard()
  else :
    print "The first card turned over is ", turnCard
    return turnCard



def newColor():
    pickColor=""
    while pickColor.lower()!='r' and pickColor.lower()!='b' and pickColor.lower()!='g' and \
          pickColor.lower()!='y':
        pickColor=raw_input ("What color would you like this to be: (r)ed, (g)reen, (y)ellow, or (b)lue?")
        if pickColor.lower()=='r':
            return 'Red'
        elif pickColor.lower()=='b':
            return 'Blue'
        elif pickColor.lower()=='y':
            return 'Yellow'
        elif pickColor.lower()=='g':
            return 'Green'
        else:
            print "That is not a valid color."





def playHand(hand, turnCard):


  def formatCard(letterInput):

    if len(letterInput) == 2:
        if letterInput[0].lower() == 'r':
            yourColor='Red'
        elif letterInput[0].lower() == 'b':
            yourColor = 'Blue'
        elif letterInput [0].lower() == 'y':
            yourColor = 'Yellow'
        elif letterInput [0].lower() == 'g':
            yourColor = 'Green'
        else :
          print "You have entered an invalid entry."
          return False


        if ord(letterInput[1]) in range (48,58):
            yourNumber = letterInput[1]
        elif letterInput[1].lower() == 's':
            yourNumber = '(S)kip'
        elif letterInput[1].lower() == 'v':
            yourNumber = 'Re(V)erse'
        elif letterInput[1].lower() == 't':
            yourNumber = "Draw (T)wo"
        else:
          print "You have entered an invalid entry."
          return False

    elif len(letterInput) == 1:
        if letterInput.lower()=='w':
            yourColor = 'any'
            yourNumber = '(W)ild'
        elif letterInput.lower() == 'f':
            yourColor = 'any'
            yourNumber = 'Draw (F)our'
        else:
          print "You have entered an invalid entry."
          return False

    return (yourColor, yourNumber)



  if hand.hasValidPlay(turnCard):
    printHands()
    letterInput =raw_input("""Please play a card. Enter the first letter of the color and the number.
      For the special cards, enter the letter in parentheses.""")
    cardInput = formatCard(letterInput)
    if not cardInput :
      return playHand(hand, turnCard)
    else :
      cardPlay = hand.findCard(cardInput[0], cardInput[1])

      if not cardPlay :
        print "You do not have that card in your hand."
        return playHand(hand, turnCard)

      elif cardPlay.getNumber() == "(W)ild" or (cardPlay.getNumber() == "Draw (F)our" and hand.canPlayDrawFour(turnCard)):
        print "You play " + str(cardPlay)
        cardPlay.setColor(newColor())
        return hand.discard(cardPlay)

      elif cardPlay.checkCard(turnCard):
        print "You play " + str(cardPlay)
        return hand.discard(cardPlay)

      else :
        print "You can't play that card."
        return playHand(hand, turnCard)


  else:
    print "You do not have a playable card. Time to draw."
    newCard = deck.dealCard()
    if newCard.checkCard(turnCard) or newCard.getColor() == 'any':
      print "You draw and play " + str(newCard)
      return newCard

    else:
      print "You draw " + str(newCard)
      playerHand.addCard(newCard)
      return turnCard


def playCompHand (hand, turnCard):
    """Plays the computer's hand"""
    playCard = hand.pickValidCard(turnCard)

    if playCard:
      print "The computer plays ", str(playCard)
      if playCard.getColor()== 'any':
        playCard.setColor(hand.maxColor())
        print "The computer selects " + playCard.getColor() + " as the color."

      print "The computer has " + str(hand.countCards()-1) + " cards left."
      return hand.discard(playCard)

    else:
      print "The computer does not have a valid card. The computer draws."
      newCard = deck.dealCard()

      if newCard.checkCard(turnCard) or newCard.getColor() == 'any' :
        print "The computer draws " + str(newCard) + ". It plays " + str(newCard) + "."
        if newCard.getColor() == 'any':
          newCard.setColor(hand.maxColor())
          print "The computer selects " + newCard.getColor() + " as the color."

        print "The computer has " + str(hand.countCards()) + " cards left."

        return newCard
      else :
        hand.addCard(newCard)
        print "The computer has " + str(hand.countCards()) + " cards left."

        return turnCard

print "Welcome to Uno! Let's deal some cards!"

deck = Deck()
playerHand = Hand()
compHand = Hand()
dealHands(deck)


printHands()

print
turnCard = dealFirstCard()

if turnCard.drawCards > 0:
  print "You draw " + str(turnCard.drawCards) + " cards."
  drawCards(turnCard.drawCards)

if turnCard.skipTurn :
  print "Your turn is skipped."
  discard = playCompHand(compHand, turnCard)
else :
  discard = playHand(playerHand, turnCard)


while compHand.countCards()>0 or playerHand.countCards() > 0:


  discard = playCompHand(compHand, discard)
  discard = playHand(playerHand, discard)
