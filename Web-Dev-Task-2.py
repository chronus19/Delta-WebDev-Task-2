import curses
import time
import threading
from random import randint

screen = curses.initscr()
base = 16       # Base line 
x_max = 40      # Starting position of obstacles, from left
head = chr(148)
body = chr(219)
player = { 'x': 15, 'y':base }      # Player coordinates
alive = 1       

is_jumping = 0
obstacle = {}

# Time parameters for the game
CYCLE_TIME = 0.18
AIR_TIME = 1
CLOUD_TIME = 0.45

def screen_init():
    # Initialise the screen 
    screen.erase()
    screen.border(0);
    screen.box();
    curses.curs_set(0)
    screen.keypad(1)
    for i in range(7):
        screen.hline(base+i+1,2,'#',76)
    screen.refresh()

def print_obstacle(x=1,xsize=1,ysize=1):
    global screen,base
    for i in range(ysize):
        screen.addstr(base-i,int(x),"X"*int(xsize) + " ");

class move(threading.Thread):
    def run(self):
        global screen,alive,x_max,CYCLE_TIME,AIR_TIME,CLOUD_TIME,is_jumping,obstacle
        y,x = screen.getmaxyx()
        
        t = 1
        score = 0
        level = 1

        screen.addstr(1,25," Delta Web Dev - TASK  2    " )
        screen.addstr(3,25," LEVEL :- " + str(level))
        screen.addstr(4,25," SCORE :- " + str(score))
        
        obstacle['x']= x_max;
        obstacle['xsize']=randint(1,3)
        obstacle['ysize']=randint(1,3)

        while alive:
            
            # Move obstacle to left 
            print_obstacle(obstacle['x'],obstacle['xsize'],obstacle['ysize'])

            # Moving Leg Animation
            if is_jumping == 0:
                if t:
                    screen.addstr(base,player['x'],'!');
                    screen.addstr(base,player['x']+1,'!');
                    t = 0
                else:
                    screen.addstr(base,player['x'],'/');
                    screen.addstr(base,player['x']+1,'\\');
                    t = 1

            # Checking for collision
            if ((player['x'] in range(obstacle['x'],obstacle['x']+obstacle['xsize']) ) or (player['x']+1 in range(obstacle['x'],obstacle['x']+obstacle['xsize']))) and player['y'] >= base+1-obstacle['ysize']:
                   alive = 0
                   time.sleep(0.3)
                   game_over(score)
                   
            obstacle['x'] -= 1
            
            if obstacle['x'] <=4:
                score += obstacle['xsize']*obstacle['ysize'];
                screen.addstr(4,25," SCORE :- " + str(score))

                # Increase Level and Difficulty
                if score >= level*20 and level < 8:
                        level += 1
                        screen.addstr(3,25," LEVEL :- " + str(level))
                        CYCLE_TIME -= 0.015
                        AIR_TIME -= 0.1
                        CLOUD_TIME -= 0.022
                screen.addstr(base-2,4,"     ");
                screen.addstr(base-1,4,"     ");
                screen.addstr(base,4,"     ");

                # Create new obstacle
                obstacle['x']= x_max;
                obstacle['xsize']=randint(1,3)
                obstacle['ysize']=randint(1,3)
                
            screen.refresh()
            time.sleep(CYCLE_TIME)

def game_over(score):
    screen_init()
    screen.addstr(base-6,24," GAME OVER ");
    screen.addstr(base-4,24," YOUR SCORE :-  " + str(score));
    screen.refresh()
    screen.getch()
    
class clouds(threading.Thread):
    # Moving clouds animation
    global screen,x_max,CLOUD_TIME

    def run(self):
        pos = x_max
        while alive:
            screen.addstr(base-9,pos+2,"("+chr(176)+   ") ")
            screen.addstr(base-8,pos+1,"("+chr(176)*3+   ") ")
            screen.addstr(base-7,pos,"("+chr(176)*5+   ") ")
            pos -= 1
            if pos <= 2:
                pos = x_max
                screen.addstr(base-9,2," "*7);
                screen.addstr(base-8,2," "*7);
                screen.addstr(base-7,2," "*8);
                screen.refresh()
                time.sleep(randint(2,6))
            screen.refresh()
            time.sleep(CLOUD_TIME)
            
        
class input(threading.Thread):
    def run(self):
        global screen
        while alive:
            k=screen.getch()
            if k == 259:        # For handling 'UP' key presses
                jump_up = jump()
                jump_up.start()
            #screen.addstr(12,5,'Entered = ' + str(k))
            time.sleep(0.2);
            
class jump(threading.Thread):
    def run(self):
        # For making Jump animation
        global screen,AIR_TIME,is_jumping
        y = base
        i = 0
        is_jumping = 1
        while i<3 and alive:
            screen.addstr(y-3,player['x'],head*2);
            screen.addstr(y-2,player['x'],body*2);
            screen.addstr(y-1,player['x'],"//");
            screen.addstr(y,player['x'],"  ");
            player['y'] = y-1
            screen.refresh()
            y -= 1
            i += 1
            time.sleep(0.06)
        time.sleep(AIR_TIME)
        i=0
        screen.addstr(y-2,player['x'],"   ");
        while i<2 and alive:
            screen.addstr(y-1,player['x'],"   ");
            screen.addstr(y,player['x'],head*2);
            screen.addstr(y+1,player['x'],body*2);
            screen.addstr(y+2,player['x'],"//");
            y += 1
            i += 1
            player['y'] = y+1
            screen.refresh()
            time.sleep(0.06)
        is_jumping = 0   


screen_init()
screen.addstr(base-2,player['x'],head*2);
screen.addstr(base-1,player['x'],body*2);
screen.addstr(base,player['x'],"!!");

# Start the game 
main_thread = move()
main_thread.start()
cloud_animate = clouds()
cloud_animate.start()
input_handler = input()
input_handler.start()

