import os
import csv
from pickle import TRUE
from CongklakBoard import CongklakBoard
import statistics

class CongklakSearchingAgent():

	def __init__(self, depth=(CongklakBoard.POSITION_OF_HOME_HOLE_1()+1), alpha=99999999) :
		#player 1 = MIN
		# board[0:(CongklakBoard.POSITION_OF_HOME_HOLE_1())] are player 0's houses
		# board[(CongklakBoard.POSITION_OF_HOME_HOLE_1())] is player 0's store

		# board[(CongklakBoard.POSITION_OF_HOME_HOLE_1()+1):(CongklakBoard.POSITION_OF_HOME_HOLE_2())] are player 1's houses
		# board[(CongklakBoard.POSITION_OF_HOME_HOLE_2())] is player 1's store
		#board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

		self.depth = depth

		beta = -alpha

		self.MAX_INT = alpha
		self.MIN_INT = beta

	def get_best_move(self, board, player1, cutVariance=False):
		save_move = []
		if (player1):
			print ('player 1 Turn with depth ' + str(self.depth))
			if (cutVariance):
				get_variance = self.get_variance(board, False, self.depth, self.MAX_INT, self.MIN_INT)
				move = get_variance[3]
				#_, move = self.min_max_value_cutVariance(False, get_variance[1], get_variance[2], self.depth, self.MAX_INT, self.MIN_INT, save_move)
			else:
				_, move, _ = self.max_value(board, self.depth, self.MAX_INT, self.MIN_INT, save_move)
			#print("Best move player A is", move)
		else:
			print ('player 2 Turn with depth ' + str(self.depth))
			if (cutVariance):
				get_variance = self.get_variance(board, True, self.depth, self.MAX_INT, self.MIN_INT)
				move = get_variance[3]
				#_, move = self.min_max_value_cutVariance(True, get_variance[1], get_variance[2], self.depth, self.MAX_INT, self.MIN_INT, save_move)
			else:
				_, move, _ = self.min_value(board, self.depth, self.MAX_INT, self.MIN_INT, save_move)
			#print("Best move player B is", move)
		print ('\n' + str(move))
		return move


	def turn(self, pit, board, player):
		board_cpy = board.copy()

		last_pit = -1

		curr_pit = (pit + 1) % (CongklakBoard.NUMBER_OF_HOLE())
		count = board_cpy[pit]
		board_cpy[pit] = 0
		while count != 0:
			# if curr_pit is not opponent's store, deposit
			if not ((player == 0 and curr_pit == (CongklakBoard.POSITION_OF_HOME_HOLE_2())) or
					(player == 1 and curr_pit == (CongklakBoard.POSITION_OF_HOME_HOLE_1()))):
				board_cpy[curr_pit] += 1
				count -= 1

				last_pit = curr_pit
			curr_pit = (curr_pit + 1) % (CongklakBoard.NUMBER_OF_HOLE())

		# if the last pit was empty and is ours and the opposite pit is not empty,
		# then steal all seeds
		if board_cpy[last_pit] == 1 and board_cpy[(CongklakBoard.POSITION_OF_HOME_HOLE_2()-1) - last_pit] != 0:
			if 0 <= last_pit and last_pit <= (CongklakBoard.POSITION_OF_HOME_HOLE_1()-1) and player == 0:
				board_cpy[(CongklakBoard.POSITION_OF_HOME_HOLE_1())] += board_cpy[last_pit] + board_cpy[(CongklakBoard.POSITION_OF_HOME_HOLE_2()-1) - last_pit]
				board_cpy[(CongklakBoard.POSITION_OF_HOME_HOLE_2()-1) - last_pit] = 0
				board_cpy[last_pit] = 0
			elif (CongklakBoard.POSITION_OF_HOME_HOLE_1()+1) <= last_pit and last_pit <= (CongklakBoard.POSITION_OF_HOME_HOLE_2()) and player == 1:
				board_cpy[(CongklakBoard.POSITION_OF_HOME_HOLE_2())] += board_cpy[last_pit] + board_cpy[(CongklakBoard.POSITION_OF_HOME_HOLE_2()-1) - last_pit]
				board_cpy[(CongklakBoard.POSITION_OF_HOME_HOLE_2()-1) - last_pit] = 0
				board_cpy[last_pit] = 0

		# if the last pit was our store, we can move again
		move_again = False
		if (last_pit == (CongklakBoard.POSITION_OF_HOME_HOLE_1()) and player == 0) or \
		  (last_pit == (CongklakBoard.POSITION_OF_HOME_HOLE_2()) and player == 1):
			move_again = True
		return move_again, board_cpy

	def successors(self, board, player):
		if player == 0:
			pits = list(range(0, (CongklakBoard.POSITION_OF_HOME_HOLE_1())))
		else:
			pits = list(range((CongklakBoard.POSITION_OF_HOME_HOLE_1()+1), (CongklakBoard.POSITION_OF_HOME_HOLE_2())))

		successor_li = []
		for pit in pits:
			if board[pit] != 0:
				move_again, board_cpy = self.turn(pit, board, player)
				successor_li.append((pit, move_again, board_cpy))

		return successor_li

	def get_variance(self, board, minPlayer, k, a, b):
		iteration = 0
		variance = 0
		currboard = []
		TSucc = []
		move = -1

		if(minPlayer == True):
			playercode = 1
		else:
			playercode = 0

		for succ in self.successors(board, playercode):
			if (CongklakSearchingAgent.check_valid_move(board, succ[0], minPlayer) == False):
				continue

			save_move = []
			save_move.append(succ[0])
			if(minPlayer == True):
				varianceTempV, varianceTempMove, varianceTempSaveMove = self.min_value(succ[2], k, a, b, save_move)
			else:
				varianceTempV, varianceTempMove, varianceTempSaveMove = self.max_value(succ[2], k, a, b, save_move)
			
			#if (CongklakSearchingAgent.check_valid_move(succ[2], varianceTempMove, minPlayer)):
			if (len(save_move) >= 2):
				varianceTemp = statistics.variance(varianceTempSaveMove)

				if (iteration == 0):
					variance = varianceTemp
					currboard = succ[2]
					TSucc = succ
					move = succ[0]
				else:
					if (((varianceTemp < variance) and (minPlayer)) or ((varianceTemp > variance) and (minPlayer == False))):
						variance = varianceTemp
						currboard = succ[2]
						TSucc = succ
						move = succ[0]

			else:
				if (iteration == 0):
					iteration -= 1
						
			iteration += 1

		return variance, currboard, TSucc, move


	def check_valid_move(board, pocket_position, minPlayer):
		if minPlayer:
			player = 2
		else:
			player = 1

		# Move is invalid if player chooses anything other than own pockets
		player_1_side = (0 <= pocket_position <= (CongklakBoard.POSITION_OF_HOME_HOLE_1()-1))
		player_2_side = ((CongklakBoard.POSITION_OF_HOME_HOLE_1()+1) <= pocket_position <= (CongklakBoard.POSITION_OF_HOME_HOLE_2()-1))
		
		# Must have stones in the pocket to be valid
		if board[pocket_position] > 0:
			if player_1_side and player==1:
				return True
			if player_2_side and player==2:
				return True
			
		# All other moves are false
		return False

			
	def min_max_value_cutVariance(self, MIN_PLAYER, board, succ, k, a, b, save_move):
		if k == 0 or self.is_terminal(board):
			return self.utility(board), None
		
		if (MIN_PLAYER):
			v = self.MIN_INT
		else :
			v = self.MAX_INT

		save_move = []

		if (MIN_PLAYER):
			pit, move_again, board_cpy = succ
			if move_again:
				v2, _, _ = self.min_value(board_cpy, k - 1, a, b, save_move)
			else:
				v2, _, _ = self.max_value(board_cpy, k - 1, a, b, save_move)
			if v2 < v:
				v, move = v2, pit
				b = min(b, v)
			if v <= a:
				return v, move
		else : 
			pit, move_again, board_cpy = board
			if move_again:
				v2, _, _ = self.max_value(board_cpy, k - 1, a, b, save_move)
			else:
				v2, _, _ = self.min_value(board_cpy, k - 1, a, b, save_move)
			if v2 > v:
				v, move = v2, pit
				a = max(a, v)
			if v >= b:
				return v, move
		return v, move

	def max_value(self, board, k, a, b, save_move):
		if k == 0 or self.is_terminal(board):
			return self.utility(board), None, None
		v = self.MIN_INT

		for succ in self.successors(board, 0):
			pit, move_again, board_cpy = succ
			if move_again:
				v2, _, _ = self.max_value(board_cpy, k - 1, a, b, save_move)
			else:
				v2, _, _ = self.min_value(board_cpy, k - 1, a, b, save_move)
			if v2 > v:
				v, move = v2, pit
				a = max(a, v)
			if v >= b:
				save_move.append(move)
				return v, move, save_move

		save_move.append(move)
		return v, move, save_move

	def min_value(self, board, k, a, b, save_move):
		if k == 0 or self.is_terminal(board):
			return self.utility(board), None, None
		v = self.MAX_INT

		for succ in self.successors(board, 1):
			pit, move_again, board_cpy = succ
			if move_again:
				v2, _, _ = self.min_value(board_cpy, k - 1, a, b, save_move)
			else:
				v2, _, _ = self.max_value(board_cpy, k - 1, a, b, save_move)
			if v2 < v:
				v, move = v2, pit
				b = min(b, v)
			if v <= a:
				save_move.append(move)
				return v, move, save_move

		save_move.append(move)
		return v, move, save_move
		
	def is_terminal(self, board):
		secondboard = board[(CongklakBoard.POSITION_OF_HOME_HOLE_1()+1):(CongklakBoard.POSITION_OF_HOME_HOLE_2())]
		firstboard = board[0:(CongklakBoard.POSITION_OF_HOME_HOLE_1())]
		return sum(firstboard) == 0 or sum(secondboard) == 0
		
	def utility(self, board):
		pos_mid = int(CongklakBoard.NUMBER_OF_HOLE()/2)
		pos_end = CongklakBoard.NUMBER_OF_HOLE()
		return sum(board[0:pos_mid]) - sum(board[pos_mid:pos_end])

	def saveTestingData(filePath, data, header=['NUMBER OF HOLE','NUMBER OF BEADS', 'CUT VARIANCE','MIN-MAX DEPTH', '1st PLAYER TYPE', '2nd PLAYER TYPE', 'WINNER', 'HOW TO WIN?', 'STEPS TAKEN TO WIN', 'TIME TO END'], myDelimiter=';'):
		
		if(os.path.isfile(filePath) == False):
			with open(filePath, 'w', encoding="UTF8") as file_: #1.create new file
				writer = csv.writer(file_,delimiter=myDelimiter) # 2. Create a CSV writer
				
				if(header != []):
					writer.writerow(header) # 3. Write header to file

				writer.writerows(data)

				file_.close()
				
		else:
			with open(filePath, mode='a', encoding="UTF8") as file_: #1.open old file
				writer = csv.writer(file_,delimiter=myDelimiter) # 2. Create a CSV writer
				writer.writerows(data) #filldata
				file_.close()