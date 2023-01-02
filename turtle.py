def face(direction, dx=0, dy=0):
    '''
    Face in a specific direction: North, South, East, West
    Or turn in a specific direction: Left, Right, Back
    '''
    direction = direction.upper()
    if direction == 'N': return 0,-1
    if direction == 'S': return 0,1
    if direction == 'E': return 1,0
    if direction == 'W': return -1,0 # Remember, Y coordinates increase as you go south
    if direction == 'B': return -dx,-dy # Reverse direction; i.e. turn 180 degrees.
    if direction == 'L': # Left
        if dx == 0:
            if dy == 1:
                return 1,0
            if dy == -1:
                return -1,0
        if dy == 0:
            if dx == 1:
                return 0,-1
            if dx == -1:
                return 0,1
        raise Exception(f"Bad direction ({dx},{dy})")
    if direction == 'R': # Right
        x,y = face('L', dx, dy)
        return -x,-y

class Turtle:
    def __init__(self, x, y, dx, dy):
        self.orig = (x, y, dx, dy)
        self.curr = (x, y, dx, dy)
        self.stamps = []
        self.isPenDown = False

    def up(self):
        self.isPenDown = False

    def down(self, char):
        self.isPenDown = True
        self.char = char

    def reset(self):
        self.curr = self.orig

    def left(self):
        dx, dy = face('L', self.curr[2], self.curr[3])
        self.curr = (self.curr[0], self.curr[1], dx, dy)

    def right(self):
        dx, dy = face('R', self.curr[2], self.curr[3])
        self.curr = (self.curr[0], self.curr[1], dx, dy)

    def stamp(self):
        if self.isPenDown:
            (x, y, dx, dy) = self.curr
            self.stamps.append((x, y, self.char))

    def move(self, steps):
        (x, y, dx, dy) = self.curr
        for i in range(steps):
            (x, y, dx, dy) = self.curr
            self.curr = (x + dx, y + dy, dx, dy)
            self.stamp()

    def xy(self):
        return self.curr[0], self.curr[1]

if __name__ == '__main__':
    turtle = Turtle(10,10,0,1)
    assert(turtle.curr == (10,10,0,1))
    turtle.move(3)
    assert(turtle.curr == (10,13,0,1))
    turtle.left()
    turtle.move(3)
    assert(turtle.curr == (13,13,1,0))
    turtle.left()
    turtle.move(3)
    assert(turtle.curr == (13,10,0,-1))
    turtle.left()
    turtle.move(3)
    assert(turtle.curr == (10,10,-1,0))