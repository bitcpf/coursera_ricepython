# template for "Stopwatch: The Game"
import simplegui
import time


# define global variables

width_frame = 300
height_frame = 200
interval = 100
current_time=0
position = [100, 100]
score_position = [260,20]

total_stop=0
suc_stop=0

# Initialize
f_timer=False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    D=str(t%10)
    temp=t/10
    C=str(temp%10)
    B=str(temp%60/10)
    A=str(temp/60)
    message = A + ":" + B + C + "." + D
    return message
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global f_timer
    if f_timer == False:
        f_timer=True
        timer.start()

def stop():
    global current_time
    global total_stop
    global suc_stop
    global f_timer
    if f_timer == True:
        timer.stop()
        total_stop=total_stop+1
        if current_time%10 == 0:
            suc_stop=suc_stop+1
        f_timer=False
    
    

def reset():
    global current_time
    global f_timer
    global suc_stop
    global total_stop
    if f_timer== True:
        timer.stop()
        f_timer=False
    current_time=0
    suc_stop=0
    total_stop=0

# define event handler for timer with 0.1 sec interval
def tick():
    global current_time
    # Grab time
    current_time=current_time+1
    
    
    

# define draw handler
def draw(canvas):
    global total_stop
    global suc_stop
    message = format(current_time)
    canvas.draw_text(message, position, 40, "White")
    score = str(suc_stop) + "/" + str(total_stop)
    canvas.draw_text(score,score_position, 30, "Green")

    
# create frame
frame = simplegui.create_frame("Stop Watch", width_frame, height_frame)

timer = simplegui.create_timer(interval, tick)
# register event handlers
start = frame.add_button('Start', start)
stop = frame.add_button('Stop', stop)
reset = frame.add_button('Reset', reset)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval, tick)

# start frame
frame.start()


# Please remember to review the grading rubric

