from shapely.geometry import Polygon

# Define two polygons
polygon1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
polygon2 = Polygon([(0, 0), (2, 0), (3, 2), (1, 2)])

# Check if they share part of the boundary
share_boundary = polygon1.intersects(polygon2) and polygon1.touches(polygon2) and not (polygon1.contains(polygon2) or polygon2.contains(polygon1))

print("Do the polygons share part of the boundary? ", share_boundary)
