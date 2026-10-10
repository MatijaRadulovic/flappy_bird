from game import Game 
from network import Network 
from agent import Agent 
from trainer import Trainer
import pygame as pg 
import threading

#m-changde mode 
#p-pause
#r-restart
#left arrow-slow down
#right arrow-speed up

auto_dead=True
fstfwd=3
p_gen_num=30
p_gen_siz=128

mut_rate=0.12
mut_amount=10
keep_perc=0.4

t=Trainer(p_gen_num,p_gen_siz,keep_perc,mut_rate,mut_amount)

th1=threading.Thread(target=t.Train)
th1.start()

pg.init()

width,height=1800,1000
window=pg.display.set_mode((width,height))
w, h = pg.display.get_surface().get_size()

scr_rect=pg.Rect(0,0,w,h)
end = False

fps=15
calcps=120


COMPUTE=pg.USEREVENT+3
pg.time.set_timer(COMPUTE,round(1000/calcps))

DRAW=pg.USEREVENT+1
pg.time.set_timer(DRAW,round(1000/fps))


game1=None
players=None
grid=1
players_num=0
alldead=True

grid_mode=False
pause=False

while not end:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            end=True
            pg.quit()
            break
        if  event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if ( event.key==pg.K_r):
                    alldead=True
                if event.key==pg.K_t:
                    t.Pause()    
                if event.key==pg.K_p:
                    pause=not pause   
                if event.key== pg.K_RIGHT:
                    fstfwd=min(fstfwd+1,10)
                if event.key== pg.K_LEFT:
                    fstfwd=max(fstfwd-0.5,0.5)
                if event.key== pg.K_m:
                    grid_mode= not grid_mode
        if not pause:       
            if event.type == DRAW: 
                window.fill((0,0,0))
                game_drawn=False
                if(players!=None and players_num>0):
                    game_h=h/grid 
                    game_w=w/grid
                    for i in range(grid):
                        for j in range(grid):
                            if(i*grid+j<players_num):
                                if(grid_mode):
                                    players[i*grid+j].DrawScaled(window,(game_w*j,game_h*i,game_w,game_h))
                                else:
                                    if(not game_drawn and not players[i*grid+j].dead):
                                        game_drawn=True
                                        players[i*grid+j].DrawScaled(window,(0,0,width,height))
                                    players[i*grid+j].DrawBird(window,(0,0,width,height))
                    if(not grid_mode and not game_drawn and players_num>0):
                        players[0].game.game_over_draw(window,(0,0,width,height))
                pg.display.flip()

                
            elif event.type == COMPUTE:
                if(not alldead):
                    if(auto_dead):
                        alldead=True
                    for i in range(grid):
                            for j in range(grid):
                                if(i*grid+j<players_num and not players[i*grid+j].dead):
                                    players[i*grid+j].step(fstfwd*1/calcps)
                                    alldead=False
                else:
                    players_num=len(t.gens_best)
                    if players_num==1:
                        players=[t.bestAgent()]
                        players[0].Restart(333460)
                    elif(players_num<=4):
                        grid=2
                        players=t.getTop(4)
                        for i in range(players_num):
                            players[i].Restart(333460)
                    else:
                        grid=3
                        players=t.getTop(9)
                        players_num=len(players)
                        for i in range(players_num):
                            players[i].Restart(333460)
                    alldead=False
t.Pause()
th1.join()            



