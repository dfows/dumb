#pyramids

import math
import random
import ordinaryCards as cardz

class Pyramid:
  def __init__(self, pyramidCards):
    self.pyramidCards = pyramidCards
    self.uncovered = []
    self.covered = []
    # now map them in the shape of a pyramid
    for rows in range(7):
      for c in range(rows):
        pcard = self.pyramidCards[sum(range(rows))+c]
        pcard.coveredBy.append(self.pyramidCards[sum(range(rows+1))+c])
        pcard.coveredBy.append(self.pyramidCards[sum(range(rows+1))+(c+1)])
    self.updateStatus()
  def updateStatus(self):
    #this might just be run upon initializing the game
    for i in self.pyramidCards:
      i.updateStatus()
      if i.hidden:
        self.covered.append(i)
      else:
        self.uncovered.append(i)
  def remove(self, card):
    self.pyramidCards.remove(card)
    for i in self.covered:
      i.updateStatus()
  def __str__(self):
    for rows in range(8):
      offset = "   "*(8-rows)
      print offset,
      for c in range(rows):
        idx = sum(range(rows))+c
        i = self.pyramidCards[idx]
        print i,
        #if len(i.coveredBy) >0:
          #for x in i.coveredBy:
            #print x,
        print " ",
      print "\n"
    return " "

class PyramidCard(cardz.Card):
  def __init__(self, suit, value, hidden=True):
    #inherit constructor? is that allowed in python
    cardz.Card.__init__(self, suit, value)
    #additional attributes:
    self.coveredBy = []
    self.hidden = hidden
  def updateStatus(self):
    if len(self.coveredBy) == 0:
      self.hidden = False
  def __str__(self):
    if self.hidden:
      return "XoX"
    else:
      return cardz.Card.__str__(self)

class PyramidGame:
  def __init__(self):
    self.pyramidCards = []
    # create a deck
    newdeck = cardz.Deck(PyramidCard)
    # randomly put 28 pcards into pyramidCards
    for i in range(28):
      r = random.randint(0,(len(newdeck)-1))
      pcard = newdeck.cards.pop(r)
      self.pyramidCards.append(pcard)
    self.flipdeck = newdeck
    #in which case it should take in an array of 28 cards as an argument
    self.pyramid = Pyramid(self.pyramidCards)
    self.flipdeck.shuffle()
    self.getNewCard()
    #not really crucial to gameplay
    self.points = 0
    self.WEIGHT = 1.075 #idk bro i just made up some shit
    self.streak = 0
  def isWon(self):
    #check if all the cards inthe pyramid are gone
    if len(self.pyramidCards) == 0:
      return True
  def isLost(self):
    #check if all the cards in the flipdeck are gone but there are still cards in the pyramid
    if len(self.flipdeck) == 0 and len(self.pyramidCards) > 0:
      return True
  def play(self):
    #initialize thing
    print "hello, player.  here is ur current pyramid"
    while not self.isWon() and not self.isLost(): 
      print self.pyramid
      print "there are",str(len(self.flipdeck)),"cards left in your deck"
      print "your current card is",self.currentCard
      self.getNextMove()
    if self.isWon():
      print "yay"
    else:
      print "fail"
  def getNextMove(self):
    move = input("what is your next move? ")
    if move == 'N': #i have to change this to something less stupid
      self.getNewCard()
    else:
      card = self.pyramid.uncovered[move]
      self.pyramid.uncovered[move] = "   "
      self.useCard(card)
  def getNewCard(self):
    #pop the top card of flipdeck
    #set current card to it
    self.currentCard = self.flipdeck.cards.pop(0)
    self.currentCard.hidden = False
  def useCard(self, card):
    if (self.currentCard == None) or (card.value == self.currentCard.value+1) or (card.value == self.currentCard.value-1):
      self.currentCard = card
      self.pyramid.remove(card)
      #noncrucial elements
      self.streak += 1
      self.points += self.streak * self.WEIGHT
    else:
      print "invalid move"

