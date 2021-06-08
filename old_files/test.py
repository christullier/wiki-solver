import random

my_list = [30, 21 , 14, 1, 24, 14, 15, 12]
for i in range(0,10):
    n = random.randint(1,30)
    my_list.append(n)

largest = 0
# for i in range(len(my_list)):
#     if my_list[i-1] > my_list[i]:
#         largest = my_list[i-1]


print(largest)
print(max(my_list))
