import random
import operator

colors = ['Red','Yellow','Green','Blue']
numbers = ['0','1','2','3','4','5','6','7','8','9']
wilds = ['(W)ild','Draw (F)our']
specials = ['Re(V)erse','(S)kip','Draw (T)wo']


class Card(object):

  def __init__(self, color, value):
    self.color = color
    self.value = value

    if self.value == "Draw (F)our":
      self.skipTurn = True
      self.drawCards = 4
    elif self.value == "Draw (T)wo":
      self.skipTurn = True
      self.drawCards = 2
    elif self.value == "(S)kip":
      self.skipTurn = True
      self.drawCards = 0
    else :
      self.skipTurn = False
      self.drawCards = 0



  def __str__(self):
    if self.color != "any":
      return "%s %s" % (self.color, self.value)
    else :
      return self.value

  def getColor(self):
    return self.color

  def setColor(self, color):
    self.color = color

  def getNumber(self):
    return self.value

  def checkCard(self,turnCard):
    if self.getColor() == turnCard.getColor() or self.getNumber() == turnCard.getNumber():
        return True
    else:
        return False

class Deck(object):

  def __init__(self):
    cards = []
    for color in colors:
      for number in numbers:
        if number == '0':
          total = 1
        else:
          total = 2
        for x in range (total):
          cards.append(Card(color, number))
      for special in specials:
        for x in range(2):
          cards.append(Card(color,special))
      for wild in wilds:
        for x in range(4):
          cards.append(Card('any', wild))
    self.cards = cards


  def __str__(self) :
    for card in self.cards:
      return card

  def dealCard(self):
    dealtCard = random.choice(self.cards)
    self.cards.remove(dealtCard)
    return dealtCard

  def returnCard(self, card):
    self.cards.append(card)


class Hand(object):

  def __init__(self):
    self.cards = []
    self.wilds = 0

  def __str__(self):
    result = '';
    for card in self.cards:
      if result != '':
        result = result + ', ' + str(card)
      else:
        result = str(card)
    return result

  def hasValidPlay(self, turnCard):
    for card in self.cards:
      if card.checkCard(turnCard) or card.getColor()=='any':
        return True
    return False

  def canPlayDrawFour(self, turnCard):
    for card in self.cards:
      if card.checkCard(turnCard):
        return False
    return True

  def addCard(self, card):
    self.cards.append(card)

  def discard(self,card):
    self.cards.remove(card)
    return card

  def countCards(self):
    return len(self.cards)

  def findCard(self, color, number):
    for card in self.cards:
      if color == card.color and number == card.value:
        return card
    return False

  def pickValidCard(self, turnCard):
    for card in self.cards:
      if card.checkCard(turnCard) :
        return card
    for card in self.cards:
      if card.getNumber() == "(W)ild" :
        return card
    for card in self.cards:
      if card.getNumber() == "Draw (F)our" :
        return card
    return False

  def maxColor(self) :
    colors = {'Blue':0, 'Red': 0, 'Green': 0, 'Yellow': 0}
    for card in self.cards:
      color = card.getColor()
      if color != 'any':
        colors[color] += 1
    return max(colors.iteritems(), key=operator.itemgetter(1))[0]


