# 循环结构

# for-in循环
"""
用for循环实现1~100求和
- `range(101)`：可以用来产生0到100范围的整数，需要注意的是取不到101。
- `range(1, 101)`：可以用来产生1到100范围的整数，相当于前面是闭区间后面是开区间。
- `range(1, 101, 2)`：可以用来产生1到100的奇数，其中2是步长，即每次数值递增的值。
- `range(100, 0, -2)`：可以用来产生100到1的偶数，其中-2是步长，即每次数字递减的值。
"""
sums = 0
for x in range(101):
    sums += x
print(sums)

# while循环

"""
猜数字游戏
"""
import random

answer = random.randint(1, 100)
counter = 0
while True:
    counter += 1
    sums = int(input('输入一个数字'))
    if counter > 7:
        print('智商不足')
        break
    if sums < answer:
        print('往大的猜')
    elif sums > answer:
        print('往小的猜')
    elif sums == answer:
        print('恭喜你猜对了，一共使用了%d次' % counter)
        break

"""
输出乘法口诀表(九九表)
"""

for i in range(1, 10):
    for j in range(1, i + 1):
        # print('%d*%d=%d' % (i, j, i * j), end='\t')
        print(f'{i} * {j} = {i * j}', end='\t')
    print()

# 此处的end="\t"是制表符的意思，及打印一个制表符，不换行，
# 另外，end="\n"也是换行的意思

"""
输入一个正整数判断它是不是素数
"""
from math import sqrt

num = int(input('请输入一个正整数: '))
end = int(sqrt(num))
is_prime = True
for x in range(2, end + 1):
    if num % x == 0:
        is_prime = False
        break
if is_prime and num != 1:
    print('%d是素数' % num)
else:
    print('%d不是素数' % num)

"""
打印三角形图案
"""

row = int(input('请输入行数: '))
for i in range(row):
    for _ in range(i + 1):
        print('*', end='')
    print()


for i in range(row):
    for j in range(row):
        if j < row - i - 1:
            print(' ', end='')
        else:
            print('*', end='')
    print()

for i in range(row):
    for _ in range(row - i - 1):
        print(' ', end='')
    for _ in range(2 * i + 1):
        print('*', end='')
    print()