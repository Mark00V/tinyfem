from shapely.geometry import Polygon

# Define two polygons
polygon1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
polygon2 = Polygon([(1, 0), (2, 0), (2, 1) ])

# Perform the union operation
union_polygon = polygon1.union(polygon2)

# Print the result
print(union_polygon, union_polygon.is_valid)

for elem in union_polygon:
    print(elem)