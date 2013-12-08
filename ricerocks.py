# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
accelerate=2
thruster=False

started=True
score=0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        canvas.draw_image(self.image,self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.thrusterf()

        
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        self.pos[0]=self.pos[0]%800
        self.pos[1]=self.pos[1]%600
        
        self.vel[0]*=0.97
        self.vel[1]*=0.97
        
        self.angle+=self.angle_vel

    def get_position(self):
        return self.pos
        
    def get_radius(self):
        
        return self.radius
        

        
    def shoot(self):
        global missile_group
        angle=angle_to_vector(self.angle)
        pos=[0,0]
        pos[0]=self.pos[0]%800+self.image_size[0]*angle[0]/2
        pos[1]=self.pos[1]%600+self.image_size[1]*angle[1]/2
        vel=[0,0]
        vel[0]=self.vel[0]+angle[0]*3.5
        vel[1]=self.vel[1]+angle[1]*3.5
        
        new_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(new_missile)
        
        
        
    
    def thrusterf(self):
        if thruster==False:
            self.image_center[0] = 45
            ship_thrust_sound.pause()
        else:
            self.image_center[0]=135
            temp=angle_to_vector(self.angle)
            
            
            # Update velocity
            self.vel[0]+=0.5*temp[0]
            self.vel[1]+=0.5*temp[1]
            
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()

        
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        canvas.draw_image(self.image,self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    
    def update(self):
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        self.pos[0]=self.pos[0]%800
        self.pos[1]=self.pos[1]%600
        
        
        if self.age<self.lifespan:
            self.age+=1
            return False
        else:
            return True
            

        
        self.angle+=self.angle_vel

    def get_position(self):
        return self.pos
        
    def get_radius(self):
        return self.radius
    
    def collide(self,other_object):
        
        pos=self.get_position()
        radius=self.get_radius()
        othr_pos=other_object.get_position()
        othr_rad=other_object.get_radius()
        dis=(pos[0]-othr_pos[0])**2+(pos[1]-othr_pos[1])**2
 

        if dis<(radius+othr_rad)**2:
            return True
        else:
            return False
        
        
        
def draw(canvas):
    global time,lives,score,started,rock_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    
        
    
    
    # draw ship and sprites
    my_ship.draw(canvas)
    #a_rock.draw(canvas)
    #a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    #a_rock.update()
    #a_missile.update()
    
    
    process_sprite_group(rock_group,canvas)
    process_sprite_group(missile_group,canvas)
    
    dif=group_group_collide(missile_group,rock_group)
    
    score=score+dif
    
    # User Interface
    canvas.draw_text('Lives: '+str(lives), (20, 40), 30, 'White')
    canvas.draw_text('Score: '+str(score), (800-20-len('Score :'+str(score))*15, 40), 30, 'White')

    
        
    if group_collide(rock_group,my_ship):
        lives=lives-1
    
    if lives<=0:
        started=False
        timer.stop()
        rock_group=set([])
        canvas.draw_text('Game Over', [WIDTH / 2-120, HEIGHT / 2], 50, 'White')
        
    if started:
        soundtrack.play()
    else:
        soundtrack.rewind()
    
# timer that spawns a rock    
def rock_spawner():
    #global a_rock
    global rock_group
    pos=[0,0]
    pos[0]=random.random()*800
    pos[1]=random.random()*600
    vel=[0,0]
    
    # Keep new rock away from my ship
    
    
   
    while ((my_ship.pos[0]-pos[0])**2+(my_ship.pos[1]-pos[1])**2)<80**2:
        
        pos[0]=random.random()*800
        pos[1]=random.random()*600
    
    
    flag1=random.randint(1,2)
    flag2=random.randint(1,2)
    flag3=random.randint(1,2)
    if flag1 == 1:
        vel[0]=random.random()*(score+1)/5
    else:
        vel[0]=-random.random()*(score+1)/5
    
    if flag2 == 1:
        vel[1]=random.random()*(score+1)/5
    else:
        vel[1]=-random.random()*(score+1)/5

    if flag1 == 1:
        ang_vel=-random.random()/12
    else:
        ang_vel=random.random()/12     
    #a_rock = Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info)

    new_rock = Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info)
# Debug
    #print len(rock_group)
    
    if len(rock_group)<12:
        rock_group.add(new_rock)
    else:
        rock_group.pop()
        rock_group.add(new_rock)
    return rock_group

# Key down handler
def keydown(key):
    global thruster
    
    
    if key == simplegui.KEY_MAP["up"]:
        thruster=True 
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel=-0.08
    if key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel=0.08
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        
        
def keyup(key):
    global thruster
    my_ship.angle_vel=0
    thruster=False

    

def process_sprite_group(group,canvas):
 
    for rock in group:
        
        rock.draw(canvas)
        tst=rock.update()
        if tst==True:
            group.remove(rock)
            set(group)
            

def group_collide(group,other_object):
    
 
    for rock in group:
        if rock.collide(other_object):
            group.remove(rock)
            set(group)
            return True
    return False
        
    
def group_group_collide(group1,group2):
    pre_collide=len(group1)
    for g1 in group1:
        if group_collide(group2,g1):
            group1.discard(g1)
            set(group1)
            
    return pre_collide-len(group1)


def reset():
    global lives,score
    timer.start()
    lives=3
    score=0
    my_ship.pos=[WIDTH / 2, HEIGHT / 2]

   
def mouseclick(pos):
    global started
    if started==False:
        reset()
        started=True
    
        


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# Last Project
# Initialize Rocks, Set empty rock
rock_group=set([])




# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 1, ship_image, ship_info)





#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

missile_group=set([])

frame.set_mouseclick_handler(mouseclick) 

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)


# get things rolling
timer.start()
frame.start()
