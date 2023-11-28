# use in fa:
# 1: walrus
# squares = [square for x in range(10) if (square := x ** 2) > 5]
# print(squares)

# other examp
# def my_function(a, b):
#     return a * b
#
# result = my_function((x := 10), x * 2)
# print(x)
# print(result)

# 2: gen exp
# ge = (i for i in range(10))
# for _ in range(10):
#     print(next(ge))

# 3: callback
# def process_data(data, callback):
#     # Perform some data processing
#     processed_data = data + 10
#
#     # Call the callback function with the processed data
#     callback(processed_data)
#
# # Define a callback function
# def print_result(result):
#     print(f"Processed result: {result}")
#
# # Call the process_data function with the callback
# data_to_process = 5
# process_data(data_to_process, print_result)