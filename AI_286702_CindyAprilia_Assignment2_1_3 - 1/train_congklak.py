import os
import logging
from CongklakAgent import Mancala as Congklak
from CongklakTrainingAgent import CongklakTrainingAgent as Agent
import os

def train_agent(agentType1='M', agentType2='M', n_games=1, games_per_checkpoint=1, model_save_path='model/mancala_agent.pkl', depth=7, cutVariance=False):
	
	# If model already exists, expand on it, otherwise start fresh
	loaded_agent = Agent(load_agent_path = model_save_path)
	environment = Congklak(depth,loaded_agent)

	while n_games>0:

		steps_taken, winner = environment.play_game(agentType1=agentType1, agentType2=agentType2, reinforcement_learning=True, ComputerOnly=True, cutVariance=False)
		# Checkpoint
		if n_games%games_per_checkpoint == 0:
			environment.mancala_agent.save_agent(model_save_path)
			logging.info('Saved RL Agent Model!')
			print('Remaining Games: ', n_games)
		n_games -= 1
		
	# Save final agent model
	environment.mancala_agent.save_agent(model_save_path)
		
	return environment


#if __name__ == "__main__":
#	#environment = train_agent(n_games = 1000000, games_per_checkpoint=25000)
#	environment = train_agent(n_games = 1000, games_per_checkpoint=25)
	
	