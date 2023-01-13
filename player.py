import math
import random

class Player:
	def __init__(self, letter):
		self.letter = letter
	def get_move(self, game):
		pass

class RandomComputerPlayer(Player):
	def __init__(self, letter):
		super().__init__(letter)
	def get_move(self, game):
		square = random.choice(game.available_moves())
		return square
		
class HumanPlayer(Player):
	def __init__(self, letter):
		super().__init__(letter)
	def get_move(self, game):
		#To be able to continue choosing
		valid_square = False
		#Haven't entered a value
		val = None
		while not valid_square:
			square = input(self.letter + "'s turn. Input move (0-8): ")
			try:
				val = int(square)
				if val not in game.available_moves():
					raise ValueError
				valid_square = True
			except:
				print("Invalid input. Try again. ")
		return val
			
		
class GeniusComputerPlayer(Player):
	def __init__(self, letter):
		super().__init__(letter)
	
	def get_move(self, game):
		if len(game.available_moves()) == 9:
			square = random.choice(game.available_moves())
		else:
			#getting square vased of the minimax algorithm 
			square = self.minimax(game, self.letter)['Position']
		return square
	
	def minimax(self, state, player):
		max_player = self.letter
		other_player = 'O' if player == 'X' else 'X'
		#We wanna see if thier was a winner in the previous round
		#Keeping track of the position and score for the minimax to work
		if state.current_winner == other_player:
			return {'Position' : None,
			'Score' :  1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
		elif not state.empty_squares():
			return {'Position' : None, 'Score' : 0}
			
		
		if player == max_player:
			best = {'Position' : None, 'Score' : -math.inf}
		else:
			best = {'Position' : None, 'Score' : math.inf}
		
		for possible_move in state.available_moves():
			#Step 1: Make a move, trying that spot
			state.make_move(possible_move, player)
			#Step 2: Recursing back by using minimax to simulate a gane after msking move
			sim_score = self.minimax(state, other_player) #alternate players
			#Step 3: Undo the move
			state.board[possible_move] = ' '
			state.current_winner = None
			sim_score['Position'] = possible_move
			#Step 4:  Update the dictionaries if necessary
			if player == max_player:
				if sim_score['Score'] > best['Score']:
					best = sim_score
			else:
				if sim_score['Score'] < best['Score']:
					best = sim_score	
				
		return best
		