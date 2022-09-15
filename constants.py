import numpy as np
from math import sqrt, asin

#Number of particles to generate
PARTICLE_QUANTITY = 10000

#number of pixels to move
CHECK_DIST = 5

#Initial Confidence Value
INIT_CONFIDENCE = 1/PARTICLE_QUANTITY

#Constant in order to determine size as the particle filter runs
PARTICLE_SIZE = 2

#Indices for the coordinates of the numpy array
X_COORD = 1
Y_COORD = 0

#Value to turn the particle by
TURN = asin(1/2)


#Margin of Error
MOE = 5

#Vals for white and black pixels
WHITE_PIXEL = np.array([255,255,255])
BLACK_PIXEL = np.array([0,0,0])