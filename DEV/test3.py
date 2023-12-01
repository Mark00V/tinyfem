from shapely.geometry import MultiLineString

# Create a MultiLineString object
multi_line = MultiLineString([[(0, 0), (1, 1)], [(2, 2), (3, 3)]])

for line in multi_line.geoms:
    print(line)
    # Iterate over the points in the LineString
    for point in line.coords:
        print(point)