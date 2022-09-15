from constants import X_COORD, Y_COORD
from math import sqrt, pow

class Line:
    start = ()
    end = ()
    colour = ()
    length = 0.0

    def __init__(self, start, end, colour):
        self.start = start
        self.end = end
        self.colour = colour
        self.length = sqrt(pow(end[X_COORD]- start[X_COORD],2) + pow(end[Y_COORD] - start[Y_COORD], 2))


    def __gt__(self, other):
        return ((self.start[X_COORD] > other.start[X_COORD]) and (self.start[Y_COORD] > other.start[Y_COORD]))

    def __lt__(self, other):
        return ((self.end[X_COORD] < other.end[X_COORD]) and (self.end[Y_COORD] < other.end[Y_COORD]))

    def display(self):
        print("   -------(X  Y)--------")
        print("Origin: " + str(self.start))
        print("End:    " + str(self.end))
        print("Length: " + str(self.length))
        print("Colour: " + str(self.colour))
        print("\n\n")