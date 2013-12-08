# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize global variables used in your code
num_range=100



# helper function to start and restart the game
def new_game():
    # remove this when you add your code    
    global time_guess
    # Calculate the guess number upbound
    time_guess=int(math.ceil(math.log(num_range+1)/math.log(2)))
    print
    global num_generate
    num_generate = random.randrange(1,num_range)
    print 'New Game. Range is from 0 to %d' %(num_range)
    print 'Number of remaining guesses is %d' %time_guess
    


# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global num_range
    num_range=100
    print ''
    new_game()
    

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range
    num_range=1000
    print ''
    new_game()

    
    
def input_guess(guess):
    # main game logic goes here	
    global time_guess
    global num_generate
    

    
    
    
    time_guess=time_guess-1
    if time_guess > 0:        
        num_guess=int(guess)
        print '\nGuess was %d' %(num_guess)
        print 'Number of remaining guesses is %d' %(time_guess)
        if num_guess > num_generate:
            print 'Lower!'
        elif num_guess < num_generate:
            print 'Higher!'
        else:
            print 'Correct!'
            new_game()
            
                
        
    else:
        num_guess=int(guess)
        print '\nGuess was %d' %(num_guess)
        print 'You ran out of the guesses. The number was %d\n' %(num_generate)
        new_game()
    # remove this when you add your code
    

    
    
    
# create frame
frame = simplegui.create_frame('Guess the Number',200,200)


# register event handlers for control elements
frame.add_button("Range is [0,100)",range100,200)
frame.add_button("Range is [0,1000)",range1000,200)
frame.add_input("Enter a guess",input_guess,200)

# call new_game and start frame
new_game()


# always remember to check your completed program against the grading rubric
