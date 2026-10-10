import pygame as pg 
import random as rnd 
import numpy as np
import math


class Bird:
    def __init__(self,x,y,r,y_vel,jump_vel,g,color):
        self.x=x 
        self.y=y 
        self.r=r 
        self.y_vel=y_vel
        self.g=g 
        self.color=color
        self.jump_vel=jump_vel
    def flap(self,t):
        self.y_vel+=self.g*t
        self.y+=self.y_vel*t
    def hit_box(self):
        return pg.Rect(self.x-self.r,self.y-self.r,self.r*2,self.r*2)
    def out_of_cage(self,scr_size):
        return self.y-self.r<0 or self.y+self.r>scr_size[1]
    def jump(self):
        self.y_vel=self.y_vel*0.1-self.jump_vel
    
    def drawBeak(self,wnd,org=(0,0),scale=(1,1),xvel=300):
        dx=org[0]
        dy=org[1]
        
        kx=scale[0]
        ky=scale[1]

        vel_vec=(xvel,self.y_vel)
        vec_int=math.sqrt(xvel*xvel+self.y_vel*self.y_vel)
        vel_vec=(vel_vec[0]*1/vec_int,vel_vec[1]*1/vec_int)

        ort_vel1=(vel_vec[1],-vel_vec[0])
        ort_vel2=(-vel_vec[1],vel_vec[0])

        beak_start=(self.x+vel_vec[0]*self.r/2,self.y+vel_vec[1]*self.r/2)
        beak_1=(beak_start[0]+ort_vel1[0]*self.r/2,beak_start[1]+ort_vel1[1]*self.r/2)
        beak_2=(beak_start[0]+ort_vel2[0]*self.r/2,beak_start[1]+ort_vel2[1]*self.r/2)
        beak_3=(self.x+vel_vec[0]*self.r*4/3,self.y+vel_vec[1]*self.r*4/3)

        beak_1=(beak_1[0]*kx,beak_1[1]*ky)
        beak_2=(beak_2[0]*kx,beak_2[1]*ky)
        beak_3=(beak_3[0]*kx,beak_3[1]*ky)
        
        beak_1=(beak_1[0]+dx,beak_1[1]+dy)
        beak_2=(beak_2[0]+dx,beak_2[1]+dy)
        beak_3=(beak_3[0]+dx,beak_3[1]+dy)
        pg.draw.polygon(wnd,(255,150,80),(beak_1,beak_2,beak_3))

    def drawBox(self,wnd,org=(0,0),scale=(1,1)):

        dx=org[0]
        dy=org[1]
        kx=scale[0]
        ky=scale[1]
        
        ox=self.hit_box().left*kx+dx
        oy=self.hit_box().top*ky+dy
        bh=self.hit_box().width*kx
        bw=self.hit_box().height*ky
        pg.draw.rect(wnd,(150,150,150),(ox,oy,bw,bh),1)
 
    def draw(self,wnd,org=(0,0),scale=(1,1),xvel=300):
        dx=org[0]
        dy=org[1]
        kx=scale[0]
        ky=scale[1]
        pg.draw.ellipse(wnd,self.color,(self.x*kx-self.r*kx+dx,self.y*ky+dy-self.r*ky,2*self.r*kx,2*self.r*ky))
        self.drawBeak(wnd,org,scale,xvel)
        #self.drawBox(wnd,org,scale)
        
class Pipe_pair:
    def __init__(self,rect1,rect2):
        self.top=rect1
        self.bot=rect2 
        self.color=(30,200,80)

    
    
    def __init__(self,scr_size,top_of_bot_pipe):
        
        margin_per=0.07
        hole_height=scr_size[1]*0.45
        pipe_width=hole_height*0.25

        min_bot_top=round((1-margin_per)*scr_size[1])
        max_bot_top=round(margin_per*scr_size[1]+hole_height)
#        top_of_bot_pipe=rnd.randint(max_bot_top,min_bot_top)
        
        self.bot=pg.Rect(scr_size[0],top_of_bot_pipe,pipe_width,scr_size[1]-top_of_bot_pipe)
        self.top=pg.Rect(scr_size[0],0,pipe_width,top_of_bot_pipe-hole_height)

        self.color=(30,200,80)

   
    def draw(self,wnd,org=(0,0),scale=(1,1)):
        dx=org[0]
        dy=org[1]

        kx=scale[0]
        ky=scale[1]

        pg.draw.rect(wnd,self.color,(self.top[0]*kx+dx,self.top[1]*ky+dy,self.top[2]*kx,self.top[3]*ky))                
        pg.draw.rect(wnd,self.color,(self.bot[0]*kx+dx,self.bot[1]*ky+dy,self.bot[2]*kx,self.bot[3]*ky))                
    

    def collision(self,rect):
        return self.top.colliderect(rect) or self.bot.colliderect(rect)
    def move(self,px):
        self.top.x+=px
        self.bot.x+=px
    def out_of_screen(self,scr_size):
        return self.bot.right<0
    def hole_rect(self):
        return (self.top.left,self.top.bottom,self.bot.width,self.bot.top-self.top.bottom)



class Game:

    def __init__(self,seed=-1,scr_size=(1500,800)):
        self.dbg=False
        if(seed==-1):
            self.rng=np.random.default_rng()
        else:
            self.rng=np.random.default_rng(seed)
            self.dbg=True
        self.game_size=scr_size
        scalex=1#scr_size[0]/800
        scaley=1#scr_size[1]/800
        init_speed=300*scalex
        self.bird=Bird(scr_size[0]/6,scr_size[1]/2,scr_size[0]/50,0,500*scaley,900*scaley,(230,200,80))
        self.speed=init_speed
        self.pipes=[]
        self.points=0
        self.new_pipe()
        self.over=False
        
    def set_seed(self,seed):
        self.rng=np.random.default_rng(seed=seed)
        self.dbg=True
    def update_points(self):
        self.points+=1
        self.speed+=2+(200/(50+self.points*2))
        
    def new_pipe(self):
        margin_per=0.07
        hole_height=self.game_size[1]*0.45
        pipe_width=hole_height*0.25
        min_bot_top=round((1-margin_per)*self.game_size[1])
        max_bot_top=round(margin_per*self.game_size[1]+hole_height)
        top_of_bot_pipe=self.rng.integers(max_bot_top,min_bot_top)

        npipe=Pipe_pair(self.game_size,top_of_bot_pipe)
        self.pipes.append(npipe)
        birdrect=self.bird.hit_box()
        
        
        ty=0

        if(birdrect.top<npipe.top.bottom):
            s=abs( npipe.top.bottom-birdrect.top )
            a=self.bird.g 
            v=-self.bird.y_vel
            
            ty=s/ ((-v+math.sqrt(v*v+4*a/2*s))/a)
        
        
        elif(birdrect.bottom>npipe.bot.top):
            s=abs (birdrect.bottom-npipe.bot.top)
            v=self.bird.jump_vel
            ty=s/v

        minnext=ty*self.speed*1.2
        lower=max(round(minnext),round(self.game_size[0]*0.33))
        if(self.dbg):
            lower=round(self.game_size[0]*0.33)
        upper=round(self.game_size[0]*0.8)
        if(lower<upper):
            self.distance_to_next=self.rng.integers(lower,upper)
        else:
            self.distance_to_next=lower
    def game_over_draw(self,wnd, rect):
            org=(rect[0],rect[1])
            scale=(rect[2]/1500,rect[3]/800)
    
            dx=org[0]
            dy=org[1]
            
            kx=scale[0]
            ky=scale[1]
            text="Game over!"
            font = pg.font.SysFont(None, 75)
            textrend = font.render(text ,True,(255,255,255))
            wnd.blit(textrend,(self.game_size[0]*kx/2+dx-textrend.get_size()[0]/2,ky*self.game_size[1]/2+dy-textrend.get_size()[1]/2))
    
    def draw(self,wnd,org=(0,0),scale=(1,1)):
        dx=org[0]
        dy=org[1]
        
        kx=scale[0]
        ky=scale[1]

        for pipe in self.pipes:
            pipe.draw(wnd,org,scale) 
        self.bird.draw(wnd,org,scale)
        text="Speed: " + str(round(self.speed))
        font = pg.font.SysFont(None, 25)
        textrend = font.render(text ,True,(255,255,255))
        wnd.blit(textrend,(15+dx,15+dy))
        pg.draw.rect(wnd,(255,255,255),(org[0],org[1],self.game_size[0]*kx,ky*self.game_size[1]),1)
        if(self.over):
            text="Game over!"
            font = pg.font.SysFont(None, 75)
            textrend = font.render(text ,True,(255,255,255))
            wnd.blit(textrend,(self.game_size[0]*kx/2+dx-textrend.get_size()[0]/2,ky*self.game_size[1]/2+dy-textrend.get_size()[1]/2))
    
    def drawBird(self,wnd,rect):
        org=(rect[0],rect[1])
        scale=(rect[2]/1500,rect[3]/800)
        if(not self.over):
            self.bird.draw(wnd,org,scale)


    def drawScaled(self,wnd,rect):
        org=(rect[0],rect[1])
        scale=(rect[2]/1500,rect[3]/800)
        self.draw(wnd,org,scale)

    def update(self,t):
        self.speed+=t
        step=-t*self.speed
        
        i=0
        n=len(self.pipes)
        while(i<n):
            pipe=self.pipes[i]
            pipe.move(step)
            i+=1
            if(pipe.collision(self.bird.hit_box())):
                self.over=True 
            if(pipe.out_of_screen(self.game_size)):
                self.pipes.remove(pipe)   
                i-=1
                n-=1
               

        self.distance_to_next+=step 
        if(self.distance_to_next<0 or len(self.pipes)==0):
            self.new_pipe()
            self.update_points()

        self.bird.flap(t)
        if(self.bird.out_of_cage(self.game_size)):
            self.over=True
    def jump_clicked(self):
        self.bird.jump()
    def pipes_infront(self,num):
            next_pipes=[]
            for pipe in self.pipes:
                if num<=0:
                    break
                if pipe.bot.right>self.bird.x:
                    num-=1
                    next_pipes.append(pipe)
            return next_pipes
    def State2(self):
        trans_x=-self.game_size[0]/6
        trans_y=-self.game_size[1]/2
        pipe=self.pipes_infront(1)
        
        (hole_x,hole_y,hole_w,hole_h)=pipe.hole_rect()
        return (self.bird.y+trans_y,self.speed,self.bird.y_vel,hole_x+trans_x,hole_y+trans_y,hole_w,hole_h)
        
    def State(self):
        pipes=self.pipes_infront(1)
        if(len(pipes)==0):
            self.new_pipe()
            pipes=self.pipes_infront(1)
        pipe=pipes[0]
        y_dist=self.bird.y-pipe.bot.top
        x_dist=self.bird.x-pipe.bot.left
        return (x_dist,y_dist)

    
    