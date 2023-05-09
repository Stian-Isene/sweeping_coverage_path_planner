from shapely import Polygon, LineString, Point, ops
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]

for i in range(len(x) - 1):
    print(i)



side1 = LineString([(0, 0), (1, 2)])

side2 = LineString([(1, 2), (3, 3)])

intersection = side1.intersection(side2)
x = intersection.x
y = intersection.y

tuple1 = (1, 0)
tuple2 = (1, 1)
tuple3 = (0, 3)

list_of_tuples = [tuple1, tuple2, tuple3]

poly = Polygon(list_of_tuples)


x, y = poly.exterior.xy
plt.plot(x, y)
plt.show()


print(x)
print(y)