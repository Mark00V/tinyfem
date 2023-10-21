my_set = {(1, 2), (3, 4)}
test_set = (2, 1)

if (test_set[0], test_set[1]) in my_set or (test_set[1], test_set[0]) in my_set:
    print("success")


my_set = {}
test_set = (2, 1)

if (test_set[0], test_set[1]) in my_set or (test_set[1], test_set[0]) in my_set:
    print("xxxsuccess")