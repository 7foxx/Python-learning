# 函数

def foo(*argms):
    sums = 0
    for x in argms:
        sums += x
    return sums


print(foo(1, 2))

# 模块
from module._05_module1 import foo

print(foo())

from module._05_module2 import foo

print(foo())

# 作用域
a = 1


def bar():
    a = 100


bar()
# 在函数内部定义的变量为局部变量不会影响全局变量
print(a)  # 1


# global 关键字

def bar2():
    global a
    a = 200


bar2()
# 如果在函数内部用 global 声明的变量则就为全局变量，会影响全局作用域的变量
print(a)  # 200


# nonlocal 关键字


def bar3():
    b = 10

    def bar4():
        nonlocal b
        b = 20

    bar4()

    # 这里 nonlocal 在 bar4 中讲 b 改成了非局部变量
    print(b)  # 20


bar3()


# 函数返回多个值
def dubF():
    return 1, 2


x, y = dubF()

print(x, y)


# 关键字参数

def use_info(name, age, gender):
    print(name)
    print(age)
    print(gender)


use_info(age=10, gender='男', name='fff')

# 如果位置穿惨与关键字穿惨一起使用，那么位置穿惨一定要先写
use_info('fff', gender=10, age=222)


# 关键字不定长参数

def zduse(**kwargs):
    print(kwargs)


zduse(name='uuu', age=111)


# lambda 匿名函数

# 函数体只能写一行
fun = lambda a,b:a+b

print(fun(1,2))

