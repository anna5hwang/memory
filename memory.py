#card game of memory
import math, random, sys

SUITS = "CDSH"
RANKS = "A23456789TJQK"
totalCards = 52
numColumns = 5
possMatches = [10, 20, 25]

#creates a class for a Card object that will contain a card value, boolean match, boolean flipped, and a string representation rep
class Card:
	def __init__(self, rank_suit, match, flipped, rep):
		self.value = rank_suit
		self.match = match
		self.flipped = flipped
		self.rep = rep

#creates a class for a GameBoard object that contains an int for the total matches left and a double array for the board itself
class GameBoard:
	def __init__(self, totMatches, row, col):
		self.matchLeft = totMatches
		self.board = [[0]*col for i in range(row)]
		self.row = row
		self.col = col

#spits out the card values to be used in the game
def valuesCreate(num):
	#creates an array with all the possible card values
	values = [0]*totalCards
	index = 0
	for i in range(len(SUITS)):
		for j in range(len(RANKS)):
			values[index] = " " + SUITS[i] + RANKS[j]
			index += 1

	#randomizes the card values
	random.shuffle(values)

	#selects the first num amounts to use as the playing deck
	deck = values[0:num]

	#copies itself, which means a match occurs when it is exactly the same
	deck = deck + deck

	#makes doubly ensure that the deck is shuffled 
	random.shuffle(deck)
	random.shuffle(deck)

	return deck

#initializes the board given the user decision on the number of pairs
def board(row, col, matches):
	#initializes the board game 
	game = GameBoard(matches, row, col)

	#creates the values that we will be putting into the cards
	deck = valuesCreate(matches)
	
	#places the cards inside the board game 
	index = 0
	for i in range(row):
		for j in range(col):
			game.board[i][j] = Card(deck[index], False, False, " X ")
			index += 1	

	return game

#prints the card representation on the board
def boardPrint(game):
	print("\n")
	#prints out how many matches left to find
	print("You have this many matches left to find: " + str(game.matchLeft))

	print("", end = '  ')
	for j in range(len(game.board[0])):
		print(" " + str(j), end = ' ')

	print("\n")

	for i in range(len(game.board)):
		print(i, end = ' ')
		for j in range(len(game.board[i])):
			print(game.board[i][j].rep, end = '') 
		print("\n")

	print("\n")

#prints out the revealed answers on the board
def boardPrintAnswer(game):
	print("", end = '  ')
	for j in range(len(game.board[0])):
		print(" " + str(j), end = ' ')

	print("\n")

	for i in range(len(game.board)):
		print(i, end = ' ')
		for j in range(len(game.board[i])):
			print(game.board[i][j].value, end = '') 
		print("\n")

	print("\n")

#reveals the card selected 
def cardSelected(game, cardloc):
	#checks whether this card was already matched or not
	if(game.board[cardloc[0]][cardloc[1]].match):
		print("This card has already been matched! You've wasted this turn.")
		print("\n")
		return game 

	#checks whether this card was already flipped
	if(game.board[cardloc[0]][cardloc[1]].flipped):
		print("This card has already been flipped! You've wasted this turn.")
		print("\n")
		return game

	game.board[cardloc[0]][cardloc[1]].flipped = True
	game.board[cardloc[0]][cardloc[1]].rep = game.board[cardloc[0]][cardloc[1]].value
	boardPrint(game)
	return game

#checks whether the two cards selected were matches
def checkMatch(game, cardloc, cardloc2):
	#in the case of the match, the rep of card will be " O " 
	#makes sure that it's not the same card being selected twice and that it's the same value
	if(game.board[cardloc[0]][cardloc[1]].value == game.board[cardloc2[0]][cardloc2[1]].value and cardloc != cardloc2):
		game.board[cardloc[0]][cardloc[1]].match = game.board[cardloc2[0]][cardloc2[1]].match = True
		game.board[cardloc[0]][cardloc[1]].rep = game.board[cardloc2[0]][cardloc2[1]].rep = " O "
		game.matchLeft -= 1
		print("There's a match!")

	#if there's no match, the rep of card will be " X " again and flipped = F
	else:
		if(game.board[cardloc[0]][cardloc[1]].match == False):
			game.board[cardloc[0]][cardloc[1]].rep = " X "	
			game.board[cardloc[0]][cardloc[1]].flipped = False	

		if(game.board[cardloc2[0]][cardloc2[1]].match == False):
			game.board[cardloc2[0]][cardloc2[1]].rep = " X "
			game.board[cardloc2[0]][cardloc2[1]].flipped = False
		print("Sorry! No match, try again!")

	boardPrint(game)
	return game

#checks to see whether user input is an int and that there are 2 inputs given
def inputCheckGet(game):
	try:
		i1, j1 = [int(x) for x in input("Enter row and column number (in that order)\nfor the card you want to flip over: ").split()]
		cardloc = [i1, j1]

		if(cardloc[0] > (game.row-1) or cardloc[1] > (game.col-1) or cardloc[0] < 0 or cardloc[1] < 0):
			print("That's not within range! Put in a valid number.")
			print("\n")
			return inputCheckGet(game)
		else:
			return cardloc

	except ValueError:
		print("That's not an int! Put in a valid number.")
		print("\n")
		return inputCheckGet(game)
	

#main method
if __name__ == "__main__":
	numMatches = int(input('Welcome to a game of memory!\nHow many total pairs would you like to match: 10, 20, or 25?\n'))

	#makes sure that it's a valid input from the possible number of matches
	if numMatches not in possMatches:
		print("Not a valid input - restart and choose from 10, 20, or 25")	
		sys.exit()

	print("This is the initial board game:")
	game = board(int((numMatches*2)/numColumns), numColumns, numMatches)
	boardPrint(game)

	# print("answers:")
	# boardPrintAnswer(game)

	while(game.matchLeft != 0):
		cardloc = inputCheckGet(game)
		game = cardSelected(game, cardloc)

		cardloc2 = inputCheckGet(game)
		game = cardSelected(game, cardloc2)
		game = checkMatch(game, cardloc, cardloc2)

	print("Winner winner chicken dinner. Congrats on winning!")
