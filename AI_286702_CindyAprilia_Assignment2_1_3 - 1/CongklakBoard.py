
class CongklakBoard():
	def __init__(self) :
		pass

	def NUMBER_OF_HOLE():
		return 14

	def NUMBER_OF_BEADS():
		return 4

	def POSITION_OF_HOME_HOLE_1():
		return (int(CongklakBoard.NUMBER_OF_HOLE()/2) - 1)

	def POSITION_OF_HOME_HOLE_2():
		return (CongklakBoard.NUMBER_OF_HOLE() - 1)


	
	def initialize_board(self):
		
		num_stones_on_start = CongklakBoard.NUMBER_OF_BEADS()
		
		pockets = [num_stones_on_start] * (CongklakBoard.NUMBER_OF_HOLE())
		pockets[CongklakBoard.POSITION_OF_HOME_HOLE_1()] = 0
		pockets[CongklakBoard.POSITION_OF_HOME_HOLE_2()] = 0
		
		return pockets


	
	
	def get_state(self, player, pockets):
		""" Returns the unique numeric state of the board for each player from
			the players own perspective. Mancala pockets not necessary but they
			can act as the reward to the computer at the end of the game.
		"""
		
		assumed_max_stones_per_pocket = 16
		
		pocket_copy = list(pockets)
		
		# Flip the board interpretation if player 2
		if player == 1:
			relevant_pockets = pocket_copy[:(CongklakBoard.POSITION_OF_HOME_HOLE_1())] + pocket_copy[(CongklakBoard.POSITION_OF_HOME_HOLE_1()+1):(CongklakBoard.POSITION_OF_HOME_HOLE_2())]
		else:
			relevant_pockets = pocket_copy[(CongklakBoard.POSITION_OF_HOME_HOLE_1()+1):(CongklakBoard.POSITION_OF_HOME_HOLE_2())] + pocket_copy[:(CongklakBoard.POSITION_OF_HOME_HOLE_1())]
			
#		# Convert mancala base counting system to decimal for state
#		# Conversion similar to octal-2-decimal except the base number
#		# is max_stones+1
#		base_number = assumed_max_stones_per_pocket + 1
#		
#		# Use int64 due to massive number of combinations which may occur
#		# Should be optimized in the future to account for many situations
#		# which do not occur in practice (eg, 12 stones in all pockets)
#		multiplier_index = np.arange(len(relevant_pockets)-1,-1,-1, dtype='int64')
#		multipliers = base_number**multiplier_index
#		state_pieces = multipliers*np.array(relevant_pockets)
#		state = np.sum(state_pieces)
		
		return relevant_pockets




	def draw_board(self, selfpockets, previous_move=-1):
		
		previous_move_marker = '__'
		
		# Create copy for modification
		#pockets = list(self.pockets)
		pockets = list(selfpockets)
		
		# Convert the last board movement to a special marker to stand out
		# only if previous move is valid
		if previous_move >= 0:
			pockets[previous_move] = previous_move_marker
		
		# Unpack list of stones in each spot for readability
		mancala_1 = "{0:0>2}".format(pockets[(CongklakBoard.POSITION_OF_HOME_HOLE_1())])
		mancala_2 = "{0:0>2}".format(pockets[(CongklakBoard.POSITION_OF_HOME_HOLE_2())])

		lower_pockets = []
		upper_pockets = []

		for hole in range(CongklakBoard.NUMBER_OF_HOLE()):
			if(hole < CongklakBoard.POSITION_OF_HOME_HOLE_1()):
				lower_pockets.append("{0:0>2}".format(pockets[hole]))
			elif(CongklakBoard.POSITION_OF_HOME_HOLE_1() < hole < CongklakBoard.POSITION_OF_HOME_HOLE_2()):
				upper_pockets.append("{0:0>2}".format(pockets[hole]))

		'''
		pocket_1 = "{0:0>2}".format(pockets[0])
		pocket_2 = "{0:0>2}".format(pockets[1])
		pocket_3 = "{0:0>2}".format(pockets[2])
		pocket_4 = "{0:0>2}".format(pockets[3])
		pocket_5 = "{0:0>2}".format(pockets[4])
		pocket_6 = "{0:0>2}".format(pockets[5])
		mancala_1 = "{0:0>2}".format(pockets[6])
		
		pocket_7 = "{0:0>2}".format(pockets[7])
		pocket_8 = "{0:0>2}".format(pockets[8])
		pocket_9 = "{0:0>2}".format(pockets[9])
		pocket_10 = "{0:0>2}".format(pockets[10])
		pocket_11 = "{0:0>2}".format(pockets[11])
		pocket_12 = "{0:0>2}".format(pockets[12])
		mancala_2 = "{0:0>2}".format(pockets[13])
		
		lower_pockets = [pocket_1,pocket_2,pocket_3,pocket_4,pocket_5,pocket_6]
		upper_pockets = [pocket_12,pocket_11,pocket_10,pocket_9,pocket_8,pocket_7]
		'''
		
		print("___________________________________________________________________")
		print("|  ____	____	____	____	____	____	____		 |")
		print("| |	|   [_{}_]  [_{}_]  [_{}_]  [_{}_]  [_{}_]  [_{}_]   ____  |".format(*upper_pockets))
		print("| | {} |												  |	| |".format(mancala_2))
		print("| |____|	____	____	____	____	____	____   | {} | |".format(mancala_1))
		print("|		 [_{}_]  [_{}_]  [_{}_]  [_{}_]  [_{}_]  [_{}_]  |____| |".format(*lower_pockets))
		print("|_________________________________________________________________|")
		
		return True




