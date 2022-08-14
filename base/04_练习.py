"""
找出所有水仙花数
"""
for x in range(100, 99999):
    i = x % 10
    j = x // 10 % 10
    k = x // 100
    if x == i ** 3 + j ** 3 + k ** 3:
        print(x)
