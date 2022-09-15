import operator
from statistics import stdev, median
import matplotlib.pyplot as plt
import numpy as np
import cv2
from cv_image import process_floor_plan
from random import uniform
from Particle import Particle


from constants import PARTICLE_QUANTITY, PARTICLE_SIZE, X_COORD, Y_COORD, INIT_CONFIDENCE, BLACK_PIXEL, MOE

#List to hold all generated particles
PARTICLES = []

#Bounds to generate the particles within
TOP_BOUND = None
BOTTOM_BOUND = None

#variable to store the numpy array
IMAGE = None

#variable to store the virtual robot
ROBOT = None

#list to store all the distance tuples for every  particle
DISTANCES = []

#used to calculate the particle size
MIN_CONSTANT = 1/50

#initialize the min confidence to the init constant (1/number of particles)
MIN_CONFIDENCE = INIT_CONFIDENCE

#generate the particles within the bounds of the floor plan
def generate_particles(num_particles: int):
    print(len(IMAGE))
    print(len(IMAGE[0]))
    i = 0
    while len(PARTICLES) < num_particles:
        valid_particle = False
        while not valid_particle:
            valid_particle = True
            x_coord = uniform(BOTTOM_BOUND[X_COORD] + MOE, TOP_BOUND[X_COORD] - MOE)
            y_coord = uniform(BOTTOM_BOUND[Y_COORD] + MOE, TOP_BOUND[Y_COORD] - MOE)
            coord = (x_coord, y_coord)
            for particle in PARTICLES:
                if(particle.get_coordinates() == coord) and not valid_particle:
                    valid_particle = False
            
            if((IMAGE[int(round(x_coord))][int(round(y_coord))] == BLACK_PIXEL).all()):
                valid_particle = False
        print(str(i) + " generated") if i%1000 == 0 and i != 0 else None
        name = "Particle " + str(i)
        orient = (uniform(-1, 1), uniform(-1, 1))
        new_particle = Particle(coord, orient, IMAGE, name)
        if(new_particle.valid):
            PARTICLES.append(new_particle)
            i += 1
    print(str(num_particles) + " generated")

#select a random particle to serve as the "virtual robot"
def create_robot():
    global ROBOT
    while ROBOT == None:
        valid_particle = False
        while not valid_particle:
            valid_particle = True
            x_coord = uniform(BOTTOM_BOUND[X_COORD] + MOE, TOP_BOUND[X_COORD] - MOE)
            y_coord = uniform(BOTTOM_BOUND[Y_COORD] + MOE, TOP_BOUND[Y_COORD] - MOE)
            coord = (x_coord, y_coord)
            if((IMAGE[int(round(x_coord))][int(round(y_coord))] == BLACK_PIXEL).all()):
                valid_particle = False
        orient = (uniform(-1, 1), uniform(-1, 1))
        ROBOT = Particle(coord, orient, IMAGE, "Robot")
        if(not ROBOT.valid):
            print('Invalid Robot')
            # print(ROBOT.valid)
            ROBOT = None
        
    print('Valid Robot!')
    # ROBOT.display()

#Get the confidence value for all particles relative to the simulated robot
def get_confidence():
    DISTANCES = []
    for particle in PARTICLES:
        temp = tuple(map(operator.sub, particle.get_distance(), ROBOT.get_distance()))
        DISTANCES.append(tuple(map(operator.abs, temp)))
    
    dist = []
    for val in DISTANCES:
        dist.append(sum(list(val)))
    if(len(dist) >= 2):
        std_dev = stdev(dist)
        med = median(dist)
    
        constant = 0

        # number of standard deviations from the mean
        for val in dist:
            index = dist.index(val)

            if(val < med):
                constant = (MIN_CONFIDENCE * (med - val)/std_dev)
            elif(med < val):
                constant = -(MIN_CONFIDENCE * (val - med)/std_dev)           
            else:
                constant = 0
                
            new_confidence = (PARTICLES[index].get_confidence() + constant) if (PARTICLES[index].get_confidence() + constant) > 0 else 0

            PARTICLES[index].set_confidence(new_confidence)

    remove_particles()

#delete any particles that fall below the minimum confidence threshold
def remove_particles():
    global MIN_CONFIDENCE
    for particle in PARTICLES:
        if particle.get_confidence() < MIN_CONFIDENCE:
            index = PARTICLES.index(particle)
            PARTICLES.pop(index)
    if(1/len(PARTICLES) < 1):
        MIN_CONFIDENCE = 1/len(PARTICLES)

#initialize the scatter plot that acts as the map for the particle filter
def initialize_map():
    coords = []
    conf = []

    plt.imshow(IMAGE)

    for particle in PARTICLES:
        particle.set_confidence(1/len(PARTICLES))
        coords.append(particle.get_coordinates())
        conf.append(particle.get_confidence())
    
    plt.scatter(x=[coord[X_COORD] for coord in coords], y=[coord[Y_COORD] for coord in coords], 
    s=[(PARTICLE_SIZE/MIN_CONSTANT)*score for score in conf], c='r', alpha=0.75)
    plt.show()
    plt.pause(0.5)
    plt.close('all')

#move all the particles equal distances
def move_particles():
    for particle in PARTICLES:
        particle.move(10)

#display the floor plan with particles drawn on  
def show_map():
    coords = []
    conf = []
    plt.imshow(IMAGE)
    for particle in PARTICLES:
        coords.append(particle.get_coordinates())
        conf.append(particle.get_confidence())

    # 100 = P_SIZE/MIN_CONSTANT * score
    # 100 = 2/(MIN_CONSTANT) * 100
    #   1 = 2 * MIN_CONSTANT
    # 1/2 = MIN_CONSTANT
    plt.scatter(x=[coord[X_COORD] for coord in coords], y=[coord[Y_COORD] for coord in coords], 
    s=[(PARTICLE_SIZE/MIN_CONSTANT)*score for score in conf], c='r', alpha=0.75)
   
if __name__ == "__main__":
    print('Initializing...')
    #disable blocking
    plt.ion()
    
    path = 'img/floor_plan_1.png'

    IMAGE = cv2.imread(path)

    MAX, MIN = process_floor_plan(path)

    # Sets the top bound to the highest X and Y values
    TOP_BOUND = MAX.start if MAX.start > MAX.end else MAX.end
    BOTTOM_BOUND = MIN.end if MIN.end < MIN.start else MIN.start

    MAX.display()
    MIN.display()

    print('Generating Particles...')
    generate_particles(PARTICLE_QUANTITY)
    print('')

    create_robot()

    initialize_map()

    while(len(PARTICLES) > 1):
        move_particles()
        ROBOT.move(10)
        get_confidence()
        show_map()
        plt.pause(0.5)
        plt.close('all')
    plt.scatter(PARTICLES[0].get_coordinates()[X_COORD], PARTICLES[0].get_coordinates()[Y_COORD], s=3, c='red')
    plt.scatter(ROBOT.get_coordinates()[X_COORD], ROBOT.get_coordinates()[Y_COORD], s=3, c='black')
    print('\nRobot Location Approximated')
    ROBOT.display()
    PARTICLES[0].display()

    show_map()
    plt.waitforbuttonpress(0)
        
