class Room:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def contains(self, x, y):
        return x >= self.left and x <= self.left + self.width and y >= self.top and y <= self.top + self.height
