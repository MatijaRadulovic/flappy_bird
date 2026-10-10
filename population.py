from agent import Agent
import multiprocessing
import random

class Population:
    def __init__(self,size):
        self.agents=[]       
        for i in range(size):
            self.agents.append(Agent())
    
    def Size(self):
        return len(self.agents)



    def new(self,perc=0.4,mut_rate=0.15,mut_amount=12):
        org_size=self.Size()*perc
        org_size=round(org_size)
        it=org_size
        for i in range(org_size):
            self.agents[i].Reset()            
        while(it<self.Size()):
            self.agents[it]=(Agent( self.agents[it%org_size].network.MutantClone(mut_rate,mut_amount)))
            self.agents[it].Reset()
            it+=1
            
    
    def run(self,num_threads=4):
        with multiprocessing.Pool(num_threads) as threads:
            self.agents=threads.map(Agent.Run,self.agents)
        self.agents.sort(key=lambda x: x.Score(),reverse=True)
        return self.agents[0]
    