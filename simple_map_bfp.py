import shapely
from shapely import Polygon, LineString, Point, ops
from shapely.geometry import mapping
import matplotlib.pyplot as plt
line = LineString([[1., 1.], [2., 1.]])

poly1 = Polygon( [(0., 0.), (10., 0.), (10., 10.), (0.,10.) ] )
#poly2 = Polygon( [(0.25, 0.25), (0.5,0.25), (0.5,0.5), (0.25,0.5) ] )
#polydiff = poly1.difference(poly2)

# xe,ye = polydiff.exterior.xy
#
#
# for LinearRing in polydiff.interiors:
#     xi,yi = LinearRing.xy
#
# obj = mapping(polydiff)
# print(obj['coordinates'])
#
# myPoly = gpd.GeoSeries([polydiff])
# myPoly.plot()
# plt.show()
boundary = line.boundary.bounds
cutting_span = 1
continue_cutting = True

max = poly1.bounds[3]

line_test = LineString([[5, 5], [20, 20]])
#print(poly1.exterior.coords)
# line_ = LineString([[boundary[2], boundary[3]], [8, 8]])
# line = ops.linemerge((line, line_))

# while(not(line.intersects(poly1.boundary))):
#     boundary = line.boundary.bounds
#     line_ = LineString([[boundary[2], boundary[3]], [boundary[2] +1, boundary[3] +1]])
#     line = ops.linemerge((line, line_))

for x in range(0, cutting_span, 20):
   # print(x)


    boundary = line.boundary.bounds
    x = boundary[2] + 1
    y = boundary[3]
    point = Point(x, y)

    while (not (poly1.boundary.intersects(point))):


        if not(poly1.boundary.intersects(point)):
            line_ = LineString([[boundary[2], boundary[3]], [boundary[2] +1, boundary[3]]])
            line = ops.linemerge((line, line_))
        boundary = line.boundary.bounds
        test = boundary[2] + 1
        point = Point(test, boundary[3])

    boundary = line.boundary.bounds
    line_ = LineString([[boundary[2], boundary[3]], [boundary[2], boundary[3] + cutting_span]])
    line = ops.linemerge((line, line_))


    boundary = line.boundary.bounds
    x = boundary[2] - 1
    y = boundary[3]
    point = Point(x, y)
    while (not (poly1.boundary.intersects(point))):


        if not(poly1.boundary.intersects(point)):
            line_ = LineString([[boundary[2], boundary[3]], [boundary[2] - 1, boundary[3]]])
            line = ops.linemerge((line, line_))
        boundary = line.boundary.bounds
        x = boundary[2] - 1
        y = boundary[3]
        point = Point(x, y)

    boundary = line.boundary.bounds
    line_ = LineString([[boundary[2], boundary[3]], [boundary[2], boundary[3] + cutting_span]])
    line = ops.linemerge((line, line_))

    # boundary = line.boundary.bounds
    # line_ = LineString([[boundary[2], boundary[3]], [boundary[2], boundary[3] + cutting_span]])
    # line = ops.linemerge((line, line_))
    # continue_cutting = False
    # while (not (line.intersects(poly1.boundary))):
    #     boundary = line.boundary.bounds
    #     if poly1.intersects(Point(boundary[2], boundary[3])):
    #         line_ = LineString([[boundary[2], boundary[3]], [boundary[2] - 1, boundary[3]]])
    #         line = ops.linemerge((line, line_))





print(poly1.intersection(line_test))

if poly1.boundary.intersects(Point(10, 1)):
    #print("TRUE")
    pass

plt.plot(*line.xy)
x, y = poly1.exterior.xy
plt.plot(x, y)
#print(line.xy)
plt.plot(*line_test.xy)

plt.show()
