import numpy as np

# Sample arrays
array1 = np.array([1, 2, 3, 4, 5])
array2 = np.array([3, 5, 7])

# Find the indices of values in array1 that are not in array2
indices_not_in_array2 = np.where(~np.isin(array1, array2))
print(np.isin(array1, array2))
# Get the values in array1 that are not in array2
values_not_in_array2 = array1[indices_not_in_array2]

# Print the results
print("Indices of values not in array2:", indices_not_in_array2)
print("Values not in array2:", values_not_in_array2)
