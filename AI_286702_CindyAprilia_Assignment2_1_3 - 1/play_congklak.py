import datetime
from xmlrpc.client import DateTime
from CongklakAgent import Mancala as Congklak
from CongklakTrainingAgent import CongklakTrainingAgent as Agent
import os

def play_game(agentType1, agentType2, reinforcement_learning = False, depth=0, ComputerOnly=False, CutVariance=False):
	# Create model path if doesn't exist
	base_cwd = os.getcwd()
	model_dir = base_cwd + "\\" + Agent.MODEL_FOLDER()
	if not os.path.exists(model_dir):
		os.mkdir(model_dir)
	model_path = model_dir + "\\" + Agent.MODEL_PATH()

	STARTTIME = datetime.datetime.now()

	loaded_agent = Agent(load_agent_path = model_path)
	environment = Congklak(depth,loaded_agent)
	steps_taken, winner = environment.play_game(agentType1, agentType2, reinforcement_learning, ComputerOnly, CutVariance)

	ENDTTIME = datetime.datetime.now()

	return (((ENDTTIME - STARTTIME).total_seconds()) * 1000000), steps_taken, winner #PlayingTime in Microseconds, StepsTaken, Winner

#if __name__ == "__main__":
#	play_game()
	
	