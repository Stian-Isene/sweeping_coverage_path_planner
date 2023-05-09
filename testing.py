import sys
from math import atan2, cos, isnan

import shapely.ops
from numpy import deg2rad, rad2deg
from shapely import Polygon, LineString, MultiPoint, Point, ops

import matplotlib.pyplot as plt
import numpy as np

def unit_vector(vector):
    #Returns the unit vector
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    #Returns the angle between the vectors v1 and v2 in radians
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def get_sides_from_polygon(poly: Polygon):
    sides = []
    x, y = poly.exterior.xy
    for i in range(len(x)-1):
        sides.append(LineString([(x[i], y[i]), (x[i+1], y[i +1])]))

    return sides

def get_closest_side(point: Point,sides: list):
    closest_side = None
    distance_closest_side = float('inf')
    for side in sides:
        if side.distance(point) < distance_closest_side:
            closest_side = side
            distance_closest_side = side.distance(point)

    return closest_side

def get_line_from_polygon_within_two_points(points: list, poly: Polygon):
    #Get the line connecting two points on a polygon.
    #Creating the path to be returned
    path = list()
    #Creating the points
    x1 = points[0][0]
    y1 = points[0][1]
    x2 = points[1][0]
    y2 = points[1][1]

    side1 = LineString([])
    side2 = LineString([])

    point_1 = Point(x1, y1)
    point_2 = Point(x2, y2)

    sides = get_sides_from_polygon(poly)

    #Get the sides of the polygon the points are one
    for side in sides:
        if side.contains(point_1):
            side1 = side
        if side.contains(point_2):
            side2 = side


    #Check if it is the same side
    if side1.equals(side2):
        path.append([x1, y1])
        path.append([x2, y2])
    else:
        intersection = side1.intersection(side2)
        x = intersection.x
        y = intersection.y

        path.append([x1, y1])
        path.append([x, y])
        path.append([x2, y2])



    return path




path_width = 4

#Simulating the input, two vertices on the vector.
vertex_1 = (2., 0.)
vertex_2 = (3., 7.)

delta_x = (vertex_2[0] - vertex_1[0])
delta_y = (vertex_2[1] - vertex_1[1])



slope = delta_y/delta_x

y_intercept =vertex_1[1] - slope*vertex_1[0]

#Creating the vector from the vertices, we have to check what comes first here.
vertex_vector = [delta_x, delta_y]

unit_vectori = [1, 0]
unit_vectorj = [0, 1]

#Getting the angle between the x-plane and the vertex_vector, saving it as theta.

theta = rad2deg(angle_between(vertex_vector, unit_vectori))

#theta = np.rad2deg(atan2(delta_y, delta_x)) #The angle between the line across the vertices and the xy-plane
phi = 90 - theta    #In the right angled triangle between parallell lines, this angle is used.



#Getting the translation along x or y axis for creating parallell lines.
translation = (path_width/2)/cos(deg2rad(phi))


#Creating the polygon from the given coords, and shrinks it
poly1 = Polygon([(2., 0.),(10., 0.5), (25., 3.),  (20.5, 7.), (10., 10), (3., 7.)])
poly2 = poly1.buffer((path_width*-1)/2)


line = LineString([[-1., 5], [20., 5]]) #Testing
lines = []  #Testing



##This is the path we want to use
path = []

#Getting the max parameters the polygons
minx_1, miny_1, maxx_1, maxy_1 = poly1.bounds
minx_2, miny_2, maxx_2, maxy_2 = poly2.bounds

#Visualises the square boundary of the field polygon
poly3 = Polygon([(minx_1, miny_1), (minx_1, maxy_1), (maxx_1, maxy_1), (maxx_1, miny_1)])

#Testing going from max y to min y.

#Creating a linestring element to find the intersection of the bounding box.
line_test = LineString([(vertex_1[0]+(-100), y_intercept + slope*(vertex_1[0]+(-100))), (vertex_2[0]+100, y_intercept + slope*(vertex_2[0]+100))])

line_vertex = LineString([(vertex_1[0], vertex_1[1]), (vertex_2[0], vertex_2[1])])


# Finds the point where the line intersects the bounding box
x1, y1, x2, y2, = poly3.intersection(line_test).boundary.bounds

line_test_intersected = LineString([(x1, y1), (x2, y2)])

line_test_2 = LineString([(x2 + translation, maxy_1), (x1 + translation, miny_1)])

plt.plot(*line_test_2.xy)

# for i in np.arange(x1 + translation, maxx_2, translation):
#     line_for = LineString([(x2 + i, maxy_1), (x1 + i, miny_1)])
#
#     x1_ = poly2.intersection(line_for).boundary.bounds[0]
#     y1_ = poly2.intersection(line_for).boundary.bounds[1]
#     x2_ = poly2.intersection(line_for).boundary.bounds[2]
#     y2_ = poly2.intersection(line_for).boundary.bounds[3]
#
#     plt.plot(*LineString([(x1_, y1_), (x2_, y2_)]).xy)
#     print(i)



test_ = poly2.boundary
test_multipoint = Point([vertex_2])

#Splitting
sides_poly_2 = get_sides_from_polygon(poly2)

# for x in sides_poly_2:
#     plt.plot(*x.xy)


#Getting the first side of the inner polygon, and adds it to the path.

#Gets the closes side:
closest_side = get_closest_side(Point(delta_x, delta_y), sides_poly_2)

#plt.plot(*closest_side.xy)

#Adds it to the path.

#path.append([closest_side.xy[0][0], closest_side.xy[0][1]])
#path.append([closest_side.xy[1][0], closest_side.xy[1][1]])



i = translation

while (i < maxx_2):


    #Creates the first line
    line_for = LineString([(x2 + i, maxy_1), (x1 + i, miny_1)])

    x1_ = poly2.intersection(line_for).boundary.bounds[0]
    y1_ = poly2.intersection(line_for).boundary.bounds[1]
    x2_ = poly2.intersection(line_for).boundary.bounds[2]
    y2_ = poly2.intersection(line_for).boundary.bounds[3]

    path.append([x1_, y1_])
    path.append([x2_, y2_])

    #plt.plot(*LineString([(x1_, y1_), (x2_, y2_)]).xy)

    #Creates the first crossing line
    side = get_closest_side(Point(x2_, y2_), sides_poly_2)
    vertical_line = LineString([(x2_, maxy_1), (x2_, miny_1)])
    #plt.plot(*vertical_line.xy)
    x1_vertical = poly2.intersection(vertical_line).boundary.bounds[0]
    y1_vertical = poly2.intersection(vertical_line).boundary.bounds[1]
    x2_vertical = poly2.intersection(vertical_line).boundary.bounds[2]
    y2_vertical = poly2.intersection(vertical_line).boundary.bounds[3]

    path.append([x2_vertical, y2_vertical])

   # plt.plot(*LineString([(x2_, y2_), (x2_vertical, y2_vertical)]).xy)

    #plt.show()
    i += translation
    #Creates the second line
    line_for = LineString([(x2 + i, maxy_1), (x1 + i, miny_1)])

    x1_ = poly2.intersection(line_for).boundary.bounds[0]
    y1_ = poly2.intersection(line_for).boundary.bounds[1]
    x2_ = poly2.intersection(line_for).boundary.bounds[2]
    y2_ = poly2.intersection(line_for).boundary.bounds[3]

    path.append([x2_, y2_])
    path.append([x1_, y1_])

    #plt.plot(*LineString([(x2_, y2_), (x1_, y1_)]).xy)

    #Creates the second crossing line

    side = get_closest_side(Point(x1_, y1_), sides_poly_2)
    vertical_line = LineString([(x1_, maxy_1), (x1_, miny_1)])

    x1_vertical = poly2.intersection(vertical_line).boundary.bounds[0]
    y1_vertical = poly2.intersection(vertical_line).boundary.bounds[1]
    x2_vertical = poly2.intersection(vertical_line).boundary.bounds[2]
    y2_vertical = poly2.intersection(vertical_line).boundary.bounds[3]

    path.append([x1_vertical, y1_vertical])

    #plt.plot(*vertical_line.xy)

    #plt.plot(*LineString([(x1_, y1_), (x1_vertical, y1_vertical)]).xy)


    i += translation

#Cleaning the list, removing all the empty list objects
path = list(filter(lambda z:not isnan(z[0]) or not isnan(z[1]), path))

#Adding the last side to the path
closest_side = get_closest_side(Point(maxx_2, maxy_2 - miny_2), sides_poly_2)

#plt.plot(*closest_side.xy)


#print(poly2.intersection(line))

x = poly2.intersection(line)

#print(x.boundary.bounds[1])




#Getting the intersections of from the created line and the shrunk polygon
# x1 = x.boundary.bounds[0]
# y1 = x.boundary.bounds[1]
# x2 = poly2.intersection(line).boundary.bounds[2]
# y2 = poly2.intersection(line).boundary.bounds[3]
#
# line2 = LineString([(x1, y1), (x2, y2)])

x, y = poly1.exterior.xy
plt.plot(x, y)

x, y = poly2.exterior.xy
plt.plot(x, y)

x, y = poly3.exterior.xy
#plt.plot(x, y)


plt.plot(*zip(*path))

#plt.plot(*line2.xy)
#plt.plot(*LineString(path).xy)
#plt.plot(*line_test_intersected.xy)
#plt.plot(*line_test_2.xy)

points = (vertex_2, [10, 10])

print(get_line_from_polygon_within_two_points(points, poly1))

line = poly1.exterior

plt.show()