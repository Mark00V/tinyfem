import numpy as np

# Create a NumPy array with x, y coordinates
coordinates = np.array([[1, 2], [3, 4], [1, 2], [5, 6], [3, 4]])

# Use np.unique to remove duplicate rows (x, y coordinates)
unique_coordinates = np.unique(coordinates, axis=0)

print("Original coordinates:")
print(coordinates)

print("\nCoordinates with duplicates removed:")
print(unique_coordinates)
