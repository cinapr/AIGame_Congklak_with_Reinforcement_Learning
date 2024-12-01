#from inspect import _Object
from CongklakBoard import CongklakBoard
from train_congklak import train_agent
from CongklakTrainingAgent import CongklakTrainingAgent
from CongklakAgent import Mancala as Congklak
from play_congklak import play_game
from CongklakSearchingAgent import CongklakSearchingAgent
from train_congklak import train_agent
import datetime

RECOMMENDED_LEVEL = 2
CUT_VARIANCE = False

class MainClass():
    def playing(self):
        playing = True
        while (playing==True) :
            choose1 = input("\n\n\n\n\nHai, welcome to Congklak with Learning..\nWhat do you want to do? (1/2/3/4/Other_keys) \n1. Compare Best Move \n2. Train Agent \n3. Play with Learning \nOther_keys. Quit\n")

            if (str(choose1) == "1") :
                Iterates = int(input("How many times to test? "))
                Level = int(input("Which level to test? "))
                for iterate in range (Iterates):
                    self.Compare(Level, 'MR')

                '''
                for iterate in range (Iterates):
                    self.Compare(1, 'M')
                for iterate in range (Iterates):
                    self.Compare(2, 'M')
                for iterate in range (Iterates):
                    self.Compare(3, 'M')
                for iterate in range (Iterates):
                    self.Compare(4, 'M')
                for iterate in range (Iterates):
                    self.Compare(5, 'M')
                for iterate in range (Iterates):
                    self.Compare(6, 'M')
                for iterate in range (Iterates):
                    self.Compare(7, 'M')
                for iterate in range (Iterates):
                    self.Compare(8, 'M')
                for iterate in range (Iterates):
                    self.Compare(9, 'M')
                for iterate in range (Iterates):
                    self.Compare(10, 'M')
                for iterate in range (Iterates):
                    self.Compare(11, 'M')
                for iterate in range (Iterates):
                    self.Compare(12, 'M')
                for iterate in range (Iterates):
                    self.Compare(13, 'M')
                for iterate in range (Iterates):
                    self.Compare(14, 'M')
                for iterate in range (Iterates):
                    self.Compare(15, 'M')
                for iterate in range (Iterates):
                    self.Compare(1, 'MR')
                for iterate in range (Iterates):
                    self.Compare(2, 'MR')
                for iterate in range (Iterates):
                    self.Compare(3, 'MR')
                for iterate in range (Iterates):
                    self.Compare(4, 'MR')
                for iterate in range (Iterates):
                    self.Compare(5, 'MR')
                for iterate in range (Iterates):
                    self.Compare(6, 'MR')
                for iterate in range (Iterates):
                    self.Compare(7, 'MR')
                for iterate in range (Iterates):
                    self.Compare(8, 'MR')
                for iterate in range (Iterates):
                    self.Compare(9, 'MR')
                for iterate in range (Iterates):
                    self.Compare(10, 'MR')
                for iterate in range (Iterates):
                    self.Compare(11, 'MR')
                for iterate in range (Iterates):
                    self.Compare(12, 'MR')
                for iterate in range (Iterates):
                    self.Compare(13, 'MR')
                for iterate in range (Iterates):
                    self.Compare(14, 'MR')
                for iterate in range (Iterates):
                    self.Compare(15, 'MR')
                '''

            elif (str(choose1) == "2") :
                choose2 = input("What algorithm do you want to use for training? (R) Random or (M) MinMax : ")
                Iterates = int(input("How many times to test?"))

                if (choose2 == "M"):
                    choose3 = input("Default Recommended Level? (Y/N) : ")

                    if (choose3 == "Y"):
                        train_agent('M', n_games=Iterates, games_per_checkpoint=1, model_save_path=(CongklakTrainingAgent.MODEL_FOLDER() + "/" + CongklakTrainingAgent.MODEL_PATH() +".pkl"), depth=int(RECOMMENDED_LEVEL), cutVariance=CUT_VARIANCE)
                    else:
                        choose4 = input("Which level do you want it to be?\n")
                        train_agent('M', n_games=Iterates, games_per_checkpoint=1, model_save_path=(CongklakTrainingAgent.MODEL_FOLDER() + "/" + CongklakTrainingAgent.MODEL_PATH() +".pkl"), depth=int(str(choose4)), cutVariance=CUT_VARIANCE)
                else:
                    train_agent('R', n_games=Iterates, games_per_checkpoint=1, model_save_path=(CongklakTrainingAgent.MODEL_FOLDER() + "/" + CongklakTrainingAgent.MODEL_PATH() +".pkl"), cutVariance=CUT_VARIANCE)
            elif (str(choose1) == "3") :
                #play
                Iterates = int(input("How many times to test? "))
                
                for iterate in range (Iterates):
                    self.CompareTrained('M', 'M')

            else :
                playing = False
                print("Bye..Bye...")

    def Compare(self, depth, agentType1='M', agentType2='M', reinforcement_learning = False):
        performance_time, steps_taken, winner = play_game(agentType1, agentType2, reinforcement_learning, depth, True, CUT_VARIANCE)
        if "Draw" not in winner : 
            winner_Name = winner.split(' (')[0]
            winning_Type = (str(winner.split(' (')[1]))[:-1]
        else :
            winner_Name = 0
            winning_Type = "Draw"
        CongklakSearchingAgent.saveTestingData('CompareResult.csv', [[CongklakBoard.NUMBER_OF_HOLE(), CongklakBoard.NUMBER_OF_BEADS(), CUT_VARIANCE, depth, agentType1, agentType2, winner_Name, winning_Type, steps_taken, performance_time]])

    def CompareTrained(self, agentType1='M', agentType2='M'):
        STARTTIME = datetime.datetime.now()
        #play = Congklak(RECOMMENDED_LEVEL)
        play = Congklak(RECOMMENDED_LEVEL)
        steps_taken, winner = play.play_game(agentType1, agentType2, True, True, CUT_VARIANCE)
        ENDTTIME = datetime.datetime.now()
        performance_time = (((ENDTTIME - STARTTIME).total_seconds()) * 1000000)

        if "Draw" not in winner : 
            winner_Name = winner.split(' (')[0]
            winning_Type = (str(winner.split(' (')[1]))[:-1]
        else :
            winner_Name = 0
            winning_Type = "Draw"
        CongklakSearchingAgent.saveTestingData('CompareTrainedResult.csv', [[CongklakBoard.NUMBER_OF_HOLE(), CongklakBoard.NUMBER_OF_BEADS(), CUT_VARIANCE, "RL"+str(RECOMMENDED_LEVEL), agentType1, agentType2, winner_Name, winning_Type, steps_taken, performance_time]])

    #train
    #train = train_agent(n_games = 1000, games_per_checkpoint=25)

if __name__ == '__main__':
    MC = MainClass()
    MC.playing()
