from shapely import Polygon, LineString, Point, ops

x = [1, 2, 3, 4]

for i in range(len(x) - 1):
    print(i)



side1 = LineString([(0, 0), (1, 2)])

side2 = LineString([(1, 2), (3, 3)])

intersection = side1.intersection(side2)
x = intersection.x
y = intersection.y

print(x)
print(y)