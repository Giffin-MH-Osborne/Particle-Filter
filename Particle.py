from constants import X_COORD, Y_COORD, TURN, BLACK_PIXEL, CHECK_DIST
import operator
import numpy as np
import math

class Particle:
    #for output purposes
    __name = ""

    #store coordinates of particle
    __coordinates = (0,0)

    #store orientation of particle (Unit circle)
    __orientation = (0,0)

    #orientation value stored as radians
    __angle = 0.0

    #amount to move the particle by (used to determine when to turn)
    __move_val = 0

    #save the image to check for walls/collisions
    __image = np.array(0)

    #distance from each side of the particle (left, right, fore, rear)
    __distance = (0,0,0,0)

    #confidence that this particle represents the robot
    __confidence = 0.0

    #value to counter when particles are generated out of bounds
    valid = False

    def __init__(self, coords:tuple, orient:tuple, image: np.array, name: str):
        #assume it is valid
        self.valid = True
        self.__name = name
        self.__coordinates = coords
        self.__orientation = orient
        self.___get_complete_angle()
        self.__image = image
        self.__distance = self.__check_distance()

    #destructor method used to delete particle if it is out of bounds or the confidence val is too low
    def __del__(self):
        return None

    #confidence accessor and mutator
    def set_confidence(self, confidence):
        self.__confidence = confidence

    def get_confidence(self):
        return self.__confidence

    #return the raw numerical orientation
    def get_orientation(self):
        return self.__orientation

    #check the particles distance between the particle and the walls.
    def validate_particle(self):
        self.__check_distance()

    #convert the numerical orientation into a more readable version for output
    def get_anglicized_orientation(self):
        north_south = ""
        east_west = ""
        if self.__orientation[X_COORD] > 0:
            east_west = "E"
        elif self.__orientation[X_COORD] < 0:
            east_west = "W"

        if self.__orientation[Y_COORD] < 0:
            north_south = "S"
        elif self.__orientation[Y_COORD] > 0:
            north_south = "N"
        
        return north_south + east_west

    #return the distance vals between the particle and the nearest 4 walls
    def get_distance(self):
        return self.__distance

    #return the raw numerical __coordinates
    def get_coordinates(self):
        return self.__coordinates

    #check the distance between the particle and each wall
    def __check_distance(self):
        #initialize the wall position to the current position of the particle
        left_wall, right_wall, fore_wall, rear_wall = self.__coordinates, self.__coordinates,self.__coordinates, self.__coordinates
        
        #local variable for ease of writing (more convenient to write angle then self.__angle)
        angle = self.__angle

        #get the angle for each cardinal direction of the particle in radians
        #if the angle becomes greater than 2 pi radians or less than 0 radians adjust it accordingly
        left_angle = angle + math.pi/2 if angle + math.pi/2 < 2*math.pi else angle - 3*math.pi/2
        right_angle = angle - math.pi/2 if angle - math.pi/2 > 0 else angle + 3*math.pi/2
        rear_angle = angle + math.pi if angle + math.pi < 2*math.pi else angle - math.pi

        #4 while loops to check collision with wall
        #try catch for if the particle spawned outside of the bounds
        try:
            while ((self.__image[int(math.floor(left_wall[Y_COORD]))][int(math.floor(left_wall[X_COORD]))] != BLACK_PIXEL).all()):
                change = self.__trig(left_angle)
                left_wall = tuple(map(operator.add, left_wall, change))
        
            while ((self.__image[int(math.floor(right_wall[Y_COORD]))][int(math.floor(right_wall[X_COORD]))] != BLACK_PIXEL).all()):
                change = self.__trig(right_angle)
                right_wall = tuple(map(operator.add, right_wall, change))

            while ((self.__image[int(math.floor(fore_wall[Y_COORD]))][int(math.floor(fore_wall[X_COORD]))] != BLACK_PIXEL).all()):
                change = self.__trig(angle)
                fore_wall = tuple(map(operator.add, fore_wall, change))

            while ((self.__image[int(math.floor(rear_wall[Y_COORD]))][int(math.floor(rear_wall[X_COORD]))] != BLACK_PIXEL).all()):
                change = self.__trig(rear_angle)
                rear_wall = tuple(map(operator.add, rear_wall, change))
        except(IndexError):
            print("{0}: OUT OF BOUNDS".format(self.__name))
            self.valid = False
            self.__del__
        
        #calculate the distance between the particle and each wall
        # use pythagorean theorem to calculate the distance val
        left_wall = tuple(map(operator.sub, left_wall, self.__coordinates))
        left_dist = math.sqrt(left_wall[X_COORD]**2 + left_wall[Y_COORD]**2) 

        right_wall = tuple(map(operator.sub, right_wall, self.__coordinates))
        right_dist = math.sqrt(right_wall[X_COORD]**2 + right_wall[Y_COORD]**2) 

        fore_wall = tuple(map(operator.sub, fore_wall, self.__coordinates))
        fore_dist = math.sqrt(fore_wall[X_COORD]**2 + fore_wall[Y_COORD]**2) 

        rear_wall = tuple(map(operator.sub, rear_wall, self.__coordinates))
        rear_dist = math.sqrt(rear_wall[X_COORD]**2 + rear_wall[Y_COORD]**2) 

        return (left_dist, right_dist, fore_dist, rear_dist)
            
#convert the radian angle into an orientation on the unit circle
    def __trig(self, angle) -> tuple:
        if(0 <= angle < math.pi/2):
            return (CHECK_DIST, CHECK_DIST)
        elif(math.pi/2 <= angle < math.pi):
            return (-CHECK_DIST, CHECK_DIST)
        elif(math.pi <= angle < 3*math.pi/2):
            return (-CHECK_DIST, -CHECK_DIST)
        return (CHECK_DIST, -CHECK_DIST)

    #T | A
    #S | c
    #used to calculate the turns
    def __get_angle(self) -> tuple:
        orient = self.__orientation

        hyp = math.sqrt(orient[X_COORD]**2 + orient[Y_COORD]**2)
        if(orient[X_COORD] < 0):
            if(orient[Y_COORD] < 0):
                #SOH
                opp = -orient[Y_COORD]

                val = opp/hyp
                angle = math.asin(val)
            else:
                #CAH
                adj = -orient[X_COORD]

                val = adj/hyp              
                angle = math.atan(val)
        else:
            if(orient[Y_COORD] < 0):
                #TOA
                opp = -orient[Y_COORD]
                adj = orient[X_COORD]

                val = opp/adj
                angle = math.atan(val)
            else:
                opp = orient[Y_COORD]

                val = opp/hyp
                angle = math.asin(val)
        return(angle)

    #used for directioning the particles
    def ___get_complete_angle(self):
        orient = self.__orientation

        hyp = math.sqrt(orient[X_COORD]**2 + orient[Y_COORD]**2)
        if(orient[X_COORD] < 0):
            if(orient[Y_COORD] < 0):
                #SOH
                opp = -orient[Y_COORD]

                val = opp/hyp
                angle = math.asin(val) + math.pi
            else:
                #CAH
                adj = -orient[X_COORD]

                val = adj/hyp              
                angle = math.acos(val) + math.pi/2
        else:
            if(orient[Y_COORD] < 0):
                #TOA
                opp = -orient[Y_COORD]
                adj = orient[X_COORD]

                val = opp/adj
                angle = math.atan(val) + 3*math.pi/2
            else:
                opp = orient[Y_COORD]

                val = opp/hyp
                angle = math.asin(val)
        self.__angle = angle

    #check if the particles current position coincides with a black pixel on the floor plan
    def __check_collision(self,x,y):
        if((self.__image[int(math.floor(x))][int(math.floor(y))] == BLACK_PIXEL).all()):
                return False
        return True

    #turn the particle  
    def turn(self, turn, dir):
        if(dir == 'l'):
            self.__angle -= turn
            if(self.__angle < 0):
                self.__angle += 2*math.pi
        else:
            self.__angle += turn
            if(self.__angle > 2*math.pi):
                self.__angle -= 2*math.pi
        
        hyp = 1
        x = math.cos(self.__angle)
        y = math.sin(self.__angle)

        self.__orientation = (y, x)

    #move the particle 
    def move(self, distance: float):
        self.__move_val += 1
        valid_move = False

        if(self.__move_val % 5 == 0):
            self.turn(TURN, 'l')

        while not valid_move:
            orient = self.__orientation
            angle = self.__get_angle()

            hyp = distance
            adj = hyp * math.cos(angle)
            opp = hyp * math.sin(angle)

            current_x = self.__coordinates[X_COORD]
            current_y = self.__coordinates[Y_COORD]

            if(orient[X_COORD] < 0):
                adj = -adj
                if(orient[Y_COORD] < 0):
                    opp = -opp
            else:
                if(orient[Y_COORD] < 0):
                    opp = -opp
            
            new_x = current_x + adj
            new_y = current_y + opp

            if(self.__check_collision(new_y, new_x)):
                self.__coordinates = (new_y, new_x)
                valid_move = True
            else:
                self.turn(2*TURN, 'r')
        self.__distance = self.__check_distance()
        
    def display(self):
        print(self.__name)
        print("Coordinates: " + str(self.__coordinates))
        print("Anglicized Orientation: " + self.get_anglicized_orientation())
        print("Raw Numerical Orientation: " + str(self.__orientation))
        print("Angle: " + str(self.__angle))
        for i in range(4):
                if i == 0: 
                    print("Left " + str(self.__distance[i]))
                elif i == 1: 
                    print("Right " + str(self.__distance[i]))
                elif i == 2: 
                    print("Fore " + str(self.__distance[i]))
                else:
                    print("Rear " + str(self.__distance[i]))
        print("Confidence: " + str(self.__confidence*100) +"%")
        print("\n\n")