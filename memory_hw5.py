# implementation of card game - Memory

import simplegui
import random

frame_weight=800
frame_height=100


# helper function to initialize globals
def new_game():
    global num_list,exposed,state,counter
    state=0
    exposed=[]
    num_list=range(8)
    num_list.extend(range(8))
    # Randomlize the list
    random.shuffle(num_list)
    # Debug Logic
    #print num_list
    
    # Iniliaze expose value
    for i in num_list:
        exposed.append(False)
    counter=0
    label.set_text('Turns='+str(counter))
    

     
# define event handlers
def mouseclick(pos):
    global state,pre1,pre2,current,counter
    # add game state logic here
    # Display the card
    idx=pos[0]//(frame_weight/16)
    current=idx
    # If the card has not been exposed, execute
    if exposed[idx]==False:
        exposed[idx]=True
        # Logic
        if state == 0:
            state = 1
            pre1=current
            counter=counter+1
            # Updates Turns
            label.set_text('Turns='+str(counter))
                
        elif state == 1:
            state=2
            pre2=pre1
            pre1=current
            
        else:      
            if num_list[pre2] != num_list[pre1]:
                exposed[pre1]=False
                exposed[pre2]=False
            state = 1
            pre2=pre1
            pre1=current
            counter=counter+1
            # Update Turns
            label.set_text('Turns='+str(counter))
    
                       
    
    
    
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    # Initial position and draw all numbers
    delta=frame_weight/32
    pos=delta
    for n in range(len(num_list)):
        canvas.draw_text(str(num_list[n]), (pos-10, frame_height/2+15), 50, 'White')
        
        # Draw the card with 3 lines, 2 boundry and 1 thick line
        if exposed[n]==False:
            canvas.draw_line([pos, 0], [pos, frame_height], frame_weight/16, 'Green')
            if n<15 and n>0:
                canvas.draw_line([pos+delta, 0], [pos+delta, frame_height], 2, 'Red')
                canvas.draw_line([pos-delta, 0], [pos-delta, frame_height], 2, 'Red')
            elif n==15:
                canvas.draw_line([pos-delta, 0], [pos-delta, frame_height], 2, 'Red')
            else:
                canvas.draw_line([pos+delta, 0], [pos+delta, frame_height], 2, 'Red')
        # Update next card        
        pos=pos+delta*2
#    canvas.draw_line([frame_weight/32*3, 0], [frame_weight/32*3, frame_height], frame_weight/16, 'Green')    
        
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", frame_weight, frame_height)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric