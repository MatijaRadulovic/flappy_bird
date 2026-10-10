from network import Network
from game import Game 
import pygame as pg
import statistics as st
import logging 


class Agent:
    
    def __init__(self,network=None):
        self.gen=0
        self.best=-1
        self.timems=0
        self.pdbg=False        
        self.game=Game()
        self.network= network
        if not network:
            self.network=Network(2,8,1,2)
        self.iter=0
        self.max_iter=5000
        self.dead=False
    

    def Reset(self):
        self.game=Game()
        self.dead=False
        self.iter=0
        self.timems=0
        self.best=-1
    def Restart(self,seed):
        self.game=Game(seed)
        self.dead=False
        self.iter=0
        self.timems=0
        self.best=-1
    def __reset(self):
        
        self.game=Game()
        self.dead=False
        self.iter=0
        self.timems=0
    
    def time_interval(self):
        ts=max((25/self.game.speed),0.01)
        return ts
    
    def step(self,dt):
        self.game.update(dt)
        self.iter+=1
        self.timems+=dt

        if self.game.over:
            self.dead=True

        if round(self.Action())==1:
            self.game.jump_clicked()

    
    def Draw(self,wnd,org=(0,0),scale=(1,1)):
        self.game.draw(wnd,org)
        self.__drawData(wnd,org)
        pass
    def DrawScaled(self,wnd,rect):
        self.game.drawScaled(wnd,rect)
        self.__drawData(wnd,rect)
        pass
    def DrawBird(self,wnd,rect):
        self.game.drawBird(wnd,rect)
    
    def __drawData(self,wnd,rect):
        
        decistxt=self.Action()
        pt=30
        
        if(decistxt>0.5):
            tcolor=(255,100,100)
        else:
            tcolor=(150,255,150)
        gentxt="Gen: "+str(self.gen)
        gencol=(100,150,255)
        braintxt = "Jump: " +"{:3.1f}".format(self.game.State()[0])+" "+"{:3.1f}".format(self.game.State()[1])+"  "+"{:3.4f}".format(decistxt)

        font = pg.font.SysFont(None, pt)
        btextrend = font.render(braintxt ,True,tcolor)
        gtextrend =font.render(gentxt ,True,gencol)
        
        dx=rect[0]
        dy=rect[1]
        w=rect[2]
        h=rect[3]

        pos = (15+dx,h-15+dy-btextrend.get_size()[1]-gtextrend.get_size()[1]-15)
        
        wnd.blit(gtextrend,pos)
        pos=(pos[0],pos[1]+gtextrend.get_size()[1]+15)
        wnd.blit(btextrend,pos)

        pass

    def run(self,rounds=4):
            scores=[]
            for i in range(rounds):        
                self.__reset()
                while(not self.dead and self.iter<self.max_iter):
                    self.step(self.time_interval())
                scores.append(self.iter)
            self.best=st.median(scores)
            return self
    
    def refBest(self):
        newIter=self.iter
        if self.best==-1:
            self.best=newIter
        else:
            self.best=min(self.best,newIter)


    def Action(self):
        y=self.network.Output(self.game.State())
        return y[0]

    def Score(self):
        return self.best


    @staticmethod 
    def Run(agent):
        return agent.run()

    @staticmethod
    def MakeChild(agent1,agent2):
        brain=Network.MakeChild(agent1.network,agent2.network)
        return Agent(brain) 
