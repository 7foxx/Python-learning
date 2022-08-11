# 变量的使用
"""
使用变量保存数据并进行加减乘除运算
"""
a = 321
b = 12
print(a + b)  # 333
print(a - b)  # 309
print(a * b)  # 3852
print(a / b)  # 26.75

"""
使用type()检查变量的类型
"""
a = 100
b = 12.345
c = 1 + 5j
d = 'hello, world'
e = True
print(type(a))  # <class 'int'>
print(type(b))  # <class 'float'>
print(type(c))  # <class 'complex'>
print(type(d))  # <class 'str'>
print(type(e))  # <class 'bool'>

"""
使用input()函数获取键盘输入(字符串)
使用int()函数将输入的字符串转换成整数
使用print()函数输出带占位符的字符串
"""
a = int(input('a = '))
b = int(input('b = '))
print('%d + %d = %d' % (a, b, a + b))
print('%d - %d = %d' % (a, b, a - b))
print('%d * %d = %d' % (a, b, a * b))
print('%d / %d = %f' % (a, b, a / b))
print('%d // %d = %d' % (a, b, a // b))
print('%d %% %d = %d' % (a, b, a % b))
print('%d ** %d = %d' % (a, b, a ** b))

# 运算符
"""
赋值运算符和复合赋值运算符
"""
a = 10
b = 3
a += b  # 相当于：a = a + b
a *= a + 2  # 相当于：a = a * (a + 2)
print(a)  # 算一下这里会输出什么

"""
比较运算符和逻辑运算符的使用
"""
flag0 = 1 == 1
flag1 = 3 > 2
flag2 = 2 < 1
flag3 = flag1 and flag2
flag4 = flag1 or flag2
flag5 = not (1 != 2)
print('flag0 =', flag0)  # flag0 = True
print('flag1 =', flag1)  # flag1 = True
print('flag2 =', flag2)  # flag2 = False
print('flag3 =', flag3)  # flag3 = False
print('flag4 =', flag4)  # flag4 = True
print('flag5 =', flag5)  # flag5 = False

# 练习
"""
将华氏温度转换为摄氏温度
"""
f = float(input('请输入华氏温度: '))
c = (f - 32) / 1.8
print('%.1f华氏度 = %.1f摄氏度' % (f, c))

"""
输入半径计算圆的周长和面积
"""
radius = float(input('请输入圆的半径: '))
perimeter = 2 * 3.1416 * radius
area = 3.1416 * radius * radius
print('周长: %.2f' % perimeter)
print('面积: %.2f' % area)

"""
输入年份 如果是闰年输出True 否则输出False
"""
year = int(input('请输入年份: '))
# 如果代码太长写成一行不便于阅读 可以使用\对代码进行折行
is_leap = year % 4 == 0 and year % 100 != 0 or \
          year % 400 == 0
print(is_leap)
