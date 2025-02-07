import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(f"Координаты: ({self.x}, {self.y})")

    def move(self, new_x, new_y):
        self.x = new_x  
        self.y = new_y  

    def dist(self, other_point):
        return math.sqrt((self.x - other_point.x)**2 + (self.y - other_point.y)**2)

p1 = Point(0, 1)
p2 = Point(2, 2)
p1.show()
p2.show()
x1move=int(input("x1:"))
y1move=int(input("y1:"))
x2move=int(input("x2:"))
y2move=int(input("y2:"))
p1.move(x1move,y1move)
p2.move(x2move,y2move)
print(f"Расстояние: {p1.dist(p2)}")