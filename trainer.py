from agent import Agent
from network import Network 
import random
import multiprocessing
import copy
from population import Population
class Trainer:
    
    def __init__(self,gen_num,gen_size):
        self.gens_best=[]
        self.pdbg=False
        self.gen=0
        self.max_gen=gen_num
        
        self.population=Population(gen_size)
        self.pause=False
    def __init__(self,gen_num,gen_size,perc,prob,amount):
        self.perc=perc
        self.prob=prob
        self.amount=amount
        self.gens_best=[]
        self.pdbg=False
        self.gen=0
        self.max_gen=gen_num
        
        self.population=Population(gen_size)
        self.pause=False

    
    def GetGen(self):
        return self.gen
    
    def GetScore(self):
        return self.bestAgent.Score()

    def RunGen(self,num_threads=4):
        return self.population.run(num_threads)
    def NextGen(self):
        self.population.new(self.perc,self.prob,self.amount)
        self.gen+=1
        
    def Train(self):
        print("Training started.")
        while(self.gen<=self.max_gen and not self.pause):
            self.NewBest(self.RunGen(1))#<<<
            print("Gen "+ str(self.gen) +" best network:\n"+self.bestAgent().network.pprint()+"\nScore: "+str(self.bestAgent().Score())+"iter "+str(self.bestAgent().timems)+"sec")
            print("------------------------")
            self.NextGen()
    def NewBest(self,agent):
        agent.gen=self.gen
        self.gens_best.append(agent)
    
    def dbg(self):
        self.pdbg=not self.pdbg

    def Pause(self):
        self.pause=not self.pause
        if self.pause:
            print("paused");
    
    def getTop(self,k):
        if(len(self.gens_best)>=k):
            return self.gens_best[-k:]
        return self.gens_best
    def bestAgent(self):
        if(self.gens_best==None): return None
        return self.gens_best[-1]