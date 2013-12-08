# Implementation of classic arcade game Pong

import simplegui
import random



# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True


direction = LEFT


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    # Initital position of ball
    ball_pos=[WIDTH/2,HEIGHT/2]
    

    ball_vel=[random.randrange(120, 240)/80.0,-random.randrange(60, 180)/80.0]
    
    if direction == False:
        ball_vel[0] = -ball_vel[0]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2,direction  # these are ints
    score1=0
    score2=0
    paddle1_vel=0
    paddle2_vel=0
    paddle1_pos=HEIGHT / 2
    paddle2_pos=HEIGHT / 2

    
    spawn_ball(direction)
    direction = not direction


def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White") # Middle Line
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White") # Left gutter
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White") # Right Gutter
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
                
    # draw ball
    c.draw_circle(ball_pos,BALL_RADIUS,2,'White','White')
    
        
    # collide and reflect off of left hand side of canvas
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT-BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # Gutter 
    if ball_pos[0] < BALL_RADIUS+PAD_WIDTH:
        if ball_pos[1] + BALL_RADIUS >= paddle1_pos-PAD_HEIGHT/2 and ball_pos[1] -BALL_RADIUS <= paddle1_pos+PAD_HEIGHT/2:
            ball_vel[0] = - ball_vel[0]*1.1
            ball_vel[1] = - ball_vel[1]*1.1
           
        else:
            spawn_ball(RIGHT)
            score2 += 1

            
    elif ball_pos[0] > WIDTH-BALL_RADIUS-PAD_WIDTH:
        if ball_pos[1] +BALL_RADIUS >= paddle2_pos-PAD_HEIGHT/2 and ball_pos[1] -BALL_RADIUS <= paddle2_pos+PAD_HEIGHT/2:
            ball_vel[0] = - ball_vel[0]*1.1
            ball_vel[1] = - ball_vel[1]*1.1
            
        else:
            spawn_ball(LEFT)
            score1 += 1
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos < PAD_HEIGHT/2:
        paddle1_pos = PAD_HEIGHT/2
    elif paddle1_pos > HEIGHT-PAD_HEIGHT/2:
        paddle1_pos = HEIGHT-PAD_HEIGHT/2
    else:       
        paddle1_pos += paddle1_vel 
    
    
    if paddle2_pos < PAD_HEIGHT/2:
        paddle2_pos = PAD_HEIGHT/2
    elif paddle2_pos > HEIGHT-PAD_HEIGHT/2:
        paddle2_pos = HEIGHT-PAD_HEIGHT/2
    else:       
        paddle2_pos += paddle2_vel 
    
    
    
    # draw paddles    
    # Draw Paddle with Line
    c.draw_line((PAD_WIDTH/2,paddle1_pos-PAD_HEIGHT/2),(PAD_WIDTH/2,paddle1_pos+PAD_HEIGHT/2), PAD_WIDTH, 'White')
    c.draw_line((WIDTH-PAD_WIDTH/2,paddle2_pos-PAD_HEIGHT/2),(WIDTH-PAD_WIDTH/2,paddle2_pos+PAD_HEIGHT/2), PAD_WIDTH, 'White')
    
    

    
    # draw scores
    
    c.draw_text(str(score1), [WIDTH / 4 , 50], 40, 'White')
    c.draw_text(str(score2), [WIDTH / 4 * 3-30, 50], 40, 'White')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 2
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 2    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -2
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -2    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0


def reset():
    global score1,score2
    score1 = 0
    score2 = 0
    new_game()
    
    
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', reset)



# start frame
new_game()
frame.start()
