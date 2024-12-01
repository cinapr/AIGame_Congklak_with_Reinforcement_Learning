import random
import numpy as np
from CongklakSearchingAgent import CongklakSearchingAgent
from CongklakTrainingAgent import CongklakTrainingAgent as agent
from CongklakBoard import CongklakBoard

RANDOM_FIRST_STEPS = 6

class Mancala:
	
	def __init__(self, depth=0, mancala_agent=None):
		self.board = CongklakBoard()
		self.SearchingAgent = CongklakSearchingAgent(depth)

		self.pockets = self.board.initialize_board()
		# Load Mancala agent if necessary
		if mancala_agent is None:
			#self.mancala_agent = agent.Agent(0.5, 0.5, 0.9, 6, 'model/mancala_agent.pkl')
			self.mancala_agent = agent(0.5, 0.5, 0.9, 6, agent.MODEL_FOLDER() + '/' + agent.MODEL_PATH() +'.pkl')
		else:
			self.mancala_agent = mancala_agent
		
	def play_game(self, agentType1='M', agentType2='M', reinforcement_learning = False, ComputerOnly=False, cutVariance=False):
		
		if (agentType1 != 'MR' and agentType1 != 'M' and agentType1 != 'R' and agentType2 != 'MR' and agentType2 != 'M' and agentType2 != 'R' ):
			return 'Should either use Random or MinMax Learning'

		# Reset board
		self.pockets = self.board.initialize_board()
		
		if reinforcement_learning == True:
			player_1 = 'computer'
			player_2 = 'computer'
			mancala_agent = self.mancala_agent
			mancala_agent.previous_state = self.board.get_state(player=2, pockets=self.pockets)
		
		else:
			if (ComputerOnly):
				player_1 = 'computer'
				player_2 = 'computer'
				mancala_agent = self.mancala_agent
				mancala_agent.previous_state = self.board.get_state(player=2, pockets=self.pockets)
			else :
				# Assume both players are humans for now
				player_1 = 'human'
				player_2 = 'human'
			
				# Computer or human player 1
				if input("Player 1 human? (y/n) ") == 'n':
					player_1 = 'computer'
					#mancala_agent = agent.CongklakTrainingAgent()
			
				# Proc user for computer or human opponent
				if input("Player 2 human? (y/n) ") == 'n':
					player_2 = 'computer'
					mancala_agent = self.mancala_agent
					mancala_agent.previous_state = self.board.get_state(player=2, pockets=self.pockets)
		
		player_turn = 1
		previous_move = -1 # Previous move marked in board draw
		
		game_over = False
		steps_taken = 0
		matiJalan = False
		loser = 3 #loser is counted when MatiJalan, winner will be used when MatiHabis

		while not(game_over):
			steps_taken += 1
			
			# Start by drawing the board
			if reinforcement_learning == False:
				self.board.draw_board(self.pockets, previous_move)
			
			# Ask for move from corresponding player
			if player_turn == 1:
				if player_1 == 'human':
					move = int(input("Player 1 - Choose Pocket 1- " + str(CongklakBoard.POSITION_OF_HOME_HOLE_1()) + " : "))
					move = self.convert_move(move, player=1)
				else:
					# Basic computer randomly chooses a Mancala position
					valid_move = False
					while not(valid_move):
						#ubah angka menjadi best move
						if (agentType1 == 'R' or (agentType1 == 'MR' and steps_taken < RANDOM_FIRST_STEPS)):
							move = self.convert_move(random.randint(1,CongklakBoard.POSITION_OF_HOME_HOLE_1()),player_turn)
						elif (agentType1 == 'M' or (agentType1 == 'MR' and steps_taken >= RANDOM_FIRST_STEPS)):
							move = self.SearchingAgent.get_best_move(self.pockets, True, cutVariance)
						valid_move = self.valid_move(move, player_turn)

						if (move == -1):
							loser = player_turn
							break
			else:
				if player_2 == 'human':
					move = int(input("Player 2 - Choose Pocket 1-" + str(CongklakBoard.POSITION_OF_HOME_HOLE_1()) + ": "))
					move = self.convert_move(move, player=2)
				else:
					# Basic computer randomly chooses a Mancala position
					valid_move = False
					while not(valid_move):
						if (agentType2 == 'R' or (agentType2 == 'MR' and steps_taken <= RANDOM_FIRST_STEPS)): #JANGANLUPA
							computer_action = mancala_agent.take_action(self.board.get_state(player_turn, self.pockets))
							move = self.convert_move(computer_action, player_turn)
						elif (agentType2 == 'M' or (agentType2 == 'MR' and steps_taken >= RANDOM_FIRST_STEPS)):
							move = self.SearchingAgent.get_best_move(self.pockets, False, cutVariance)
						
						valid_move = self.valid_move(move, player_turn)

						if (move == -1):
							loser = player_turn
							break
					
					if (valid_move):
						# Inject the state into the agent for learning
						mancala_agent.update_q(self.board.get_state(player_turn, self.pockets))
					
			if (move != -1):
				# Check if move is valid prior to performing
				if not(self.valid_move(move, player_turn)):
					print("INVALID MOVE")
					continue
			
				# Perform assumed valid move and determine next to move
				player_turn, game_over = self.simulate_move(move, player_turn)
			
				# Update previous move
				previous_move = move

			else :
				game_over = True
				matiJalan = True

		if reinforcement_learning == True:
			# Assume mancala agent is player 2 for now
			mancala_agent.update_q(self.board.get_state(player=2,pockets=self.pockets), self.pockets[CongklakBoard.POSITION_OF_HOME_HOLE_2()])

			# Update agent for persistence
			self.mancala_agent = mancala_agent
		
		#if reinforcement_learning == False:
		# Draw final board and announce winner
		self.board.draw_board(self.pockets)
		if (matiJalan):
			winner = self.determine_winner()
		else:
			winner = self.determine_winner()

		print("Winner: ", winner, "!!!")

		return steps_taken, winner #return steps_take to win and the winner
			
	def convert_move(self, move, player):
		""" Converts the standard 1-6 input of the player into the corresponding
		pocket for each player as needed
		"""
		if player == 1:
			return move-1 # Shift left once to get the pocket position
		if player == 2:
			return move+(CongklakBoard.POSITION_OF_HOME_HOLE_1()) # Shift right 6 spaces to refer to upper board spot
		return False # Error case handling
	
	def valid_move(self, pocket_position, player):
		
		# Move is invalid if player chooses anything other than own pockets
		player_1_side = (0 <= pocket_position <= (CongklakBoard.POSITION_OF_HOME_HOLE_1()-1))
		player_2_side = ((CongklakBoard.POSITION_OF_HOME_HOLE_1()+1) <= pocket_position <= (CongklakBoard.POSITION_OF_HOME_HOLE_2()-1))
		
		# Must have stones in the pocket to be valid
		if self.pockets[pocket_position] > 0:
			if player_1_side and player==1:
				return True
			if player_2_side and player==2:
				return True
			
		# All other moves are false
		return False
	
	def check_game_over(self):
		""" Checks if all pockets are empty of stones. If so assigns all
			remaining stones to the appropriate mancala.
		"""
		
		game_over = False
		
		empty_player_1 = sum(self.pockets[:(CongklakBoard.POSITION_OF_HOME_HOLE_1())]) == 0
		empty_player_2 = sum(self.pockets[(CongklakBoard.POSITION_OF_HOME_HOLE_1()+1):(CongklakBoard.POSITION_OF_HOME_HOLE_2())]) == 0
		
		# If player 2 is empty, collect player 1's stones
		if empty_player_2:
			# Put remaining stones in player 2's mancala
			self.pockets[(CongklakBoard.POSITION_OF_HOME_HOLE_1())] += sum(self.pockets[:(CongklakBoard.POSITION_OF_HOME_HOLE_1())])
			self.pockets[:(CongklakBoard.POSITION_OF_HOME_HOLE_1())] = [0]*(CongklakBoard.POSITION_OF_HOME_HOLE_1())
			game_over = True
		
		# If player 1 is empty, collect player 1's stones
		if empty_player_1:
			# Put remaining stones in player 2's mancala
			self.pockets[(CongklakBoard.POSITION_OF_HOME_HOLE_2())] += sum(self.pockets[(CongklakBoard.POSITION_OF_HOME_HOLE_1()+1):(CongklakBoard.POSITION_OF_HOME_HOLE_2())])
			self.pockets[(CongklakBoard.POSITION_OF_HOME_HOLE_1()+1):(CongklakBoard.POSITION_OF_HOME_HOLE_2())] = [0]*(CongklakBoard.POSITION_OF_HOME_HOLE_1())
			game_over = True
		
		return game_over
	
	def determine_winner(self, loser = 3):
		
		if (loser == 1):
			return "Player 2 (Menang Jalan)"
		elif (loser == 2):
			return "Player 1 (Menang Jalan)"
		elif (loser != 1 and loser !=2):
			if self.pockets[(CongklakBoard.POSITION_OF_HOME_HOLE_2())]>self.pockets[(CongklakBoard.POSITION_OF_HOME_HOLE_1())]:
				return "Player 2 (Menang Mati)"
			elif self.pockets[(CongklakBoard.POSITION_OF_HOME_HOLE_2())]<self.pockets[(CongklakBoard.POSITION_OF_HOME_HOLE_1())]:
				return "Player 1 (Menang Mati)"
			
		return "Draw"

	def determine_winner_matiJalan(self, name):
		return "Player " + str(name)
	
	def switch_player(self, player):
		
		if player == 1:
			return 2
		return 1
	
	def capture(self, pocket_position, mancala_pocket):
		""" Captures all stones in the pocket and pocket opposite, goes into
		The proper mancala pocket specified as input
		"""
		
		#CEK YG INI
		#opposite_pocket_dict = {0: 12, 1:11, 2:10, 3:9, 4:8, 5:7,
		#						7:5, 8:4, 9:3, 10:2, 11:1, 12:0}

		opposite_pocket_dict = {}
		for hole in range(CongklakBoard.NUMBER_OF_HOLE()):
			if((hole != CongklakBoard.POSITION_OF_HOME_HOLE_1()) and (hole != CongklakBoard.POSITION_OF_HOME_HOLE_2())):
				opposite_pocket_dict[hole] = (CongklakBoard.NUMBER_OF_HOLE() - 2) - hole
		
		# Take the stone from the pocket itself
		self.pockets[mancala_pocket] += self.pockets[pocket_position]
		self.pockets[pocket_position] = 0
		
		# Take the stones from the opposite pocket
		opposite_pocket = opposite_pocket_dict[pocket_position]
		self.pockets[mancala_pocket] += self.pockets[opposite_pocket]
		self.pockets[opposite_pocket] = 0
		
		return True
	
	def simulate_move(self, pocket_position, player):
		
		# Condense to local version of pockets
		pockets = self.pockets
		
		stones_drawn = pockets[pocket_position]
		pockets[pocket_position] = 0
		
		# Inefficient loop, clean up in future
		while stones_drawn > 0:
			pocket_position += 1
			
			# Case to handle looping back to start of board
			if pocket_position > len(pockets)-1:
				pocket_position = 0
				
			# Consider special cases (mancala pocket) before normal stone drops
			mancala_1_position = pocket_position==(CongklakBoard.POSITION_OF_HOME_HOLE_1())
			mancala_2_position = pocket_position==(CongklakBoard.POSITION_OF_HOME_HOLE_2())
			player_1 = player == 1
			player_2 = player == 2
			if mancala_1_position and player_2:
				continue # Skip stone drop and proceeding logic
			if mancala_2_position and player_1:
				continue # Skip stone drop and proceeding logic
				
			# Stone drop
			pockets[pocket_position] += 1
			stones_drawn -= 1
		
		# Determine if capture occurs
		end_on_player_1_side = (0 <= pocket_position <= (CongklakBoard.POSITION_OF_HOME_HOLE_1()-1))
		end_on_player_2_side = ((CongklakBoard.POSITION_OF_HOME_HOLE_1()+1) <= pocket_position <= (CongklakBoard.POSITION_OF_HOME_HOLE_2()-1))
		
		# Only capture if stone is empty (has 1 stone after placement)
		stone_was_empty = pockets[pocket_position] == 1
		
		# Player 1 capture
		if player_1 and end_on_player_1_side and stone_was_empty:
			self.capture(pocket_position, (CongklakBoard.POSITION_OF_HOME_HOLE_1()))
			
		# Player 2 capture
		if player_2 and end_on_player_2_side and stone_was_empty:
			self.capture(pocket_position, (CongklakBoard.POSITION_OF_HOME_HOLE_2()))
		
		# Determine next player
		if mancala_1_position and player_1:
			next_player = player # Player 1 Mancala gets another turn
		elif mancala_2_position and player_2:
			next_player = player # Player 2 Mancala gets another turn
		else:
			next_player = self.switch_player(player) # All else switch player
		
		game_over = self.check_game_over()
		
		return next_player, game_over