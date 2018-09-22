# Blackjack
# http://www.codeskulptor.org/#user45_EB1Ejexj43bskxd.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
            
    def __str__(self):
        string = ""
        for i in range(len(self.cards)):
            string += (str(self.cards[i]) + " ")
        return "Hand contains " + string

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = 0
        for c in self.cards:
            hand_value += VALUES[c.get_rank()]
        for c in self.cards:
            if 'A' not in c.get_rank():
                return hand_value
            elif hand_value + 10 <= 21:
                return hand_value + 10
        return hand_value
            
    def draw(self, canvas, pos):
        i = 0
        for c in self.cards:
            c.draw(canvas, [pos[0] + i * 100, pos[1]])
            i += 1
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for S in SUITS:
            for R in RANKS:
                self.deck.append(Card(S, R))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        card_dealt = random.choice(self.deck)
        self.deck.remove(card_dealt)
        return card_dealt
    
    def __str__(self):
        string = ""
        for i in range(52):
            string += str(self.deck[i]) + " "
        return "Deck contains " + string   



#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, outcome1, outcome2, score
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    outcome1 = ""
    outcome2 = "Hit or stand?"
    if in_play:
        outcome1 = "You lose."
        score -= 1
    in_play = True

def hit():
    global player, deck, outcome1, in_play, score
    if not in_play:
        return None
    if player.get_value() <= 21:
        player.add_card(deck.deal_card())
        if player.get_value() > 21:
            score -= 1
            outcome1 = "You went bust."
            in_play = False
            
            
def stand():
    global player, dealer, deck, in_play, score, outcome1, outcome2
    if not in_play:
        return None
    if player.get_value() > 21:
        in_play = False
        score -= 1
        outcome1 = "You went bust."
        outcome2 = "New deal?"
        return None
    else:
        while (dealer.get_value() < 17):
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            in_play = False
            score += 1
            outcome1 = "Dealer went bust."
            outcome2 = "New deal?"
            in_play = False
            return None
    in_play = False
    if player.get_value() > dealer.get_value():
        outcome1 = "Player wins."
        score += 1
    else:
        outcome1 = "Dealer wins."
        score -= 1
    outcome2 = "New deal?"


# draw handler    
def draw(canvas):
    global outcome1, outcome2, score
    player.draw(canvas, [100, 400])
    if not in_play:
        dealer.draw(canvas, [100, 200])
    else:
        dealer.draw(canvas, [100, 200])
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [136, 248], CARD_BACK_SIZE)                          
    canvas.draw_text("Dealer",(100, 150), 30, "Black")
    canvas.draw_text("Player",(100, 370), 30, "Black")
    canvas.draw_text("Blackjack",(180, 70), 60, "White")
    canvas.draw_text(outcome1,(220, 150), 30, "Black")
    canvas.draw_text(outcome2,(220, 370), 30, "Black")
    canvas.draw_text("score " + str(score), (450, 110), 30, "Black")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
