import urllib.request as req

url = 'https://ys.mihoyo.com/'
# 基本使用

# 类型和方法
# 模拟浏览器向服务器发送请求
res1 = req.urlopen(url)

# HTTPResponse 类型
print(type(res1))

# read 方法 返回的是字节形式的二进制数据
# 参数为空返回全部字节，传人数字就读取多个字节
# decode 为解码，把二进制的数据转换为某个编码类型的数据
context1 = res1.read().decode('utf8')
print(context1)

# 读取一行
context2 = res1.readline()
print(context2)

# 一行一行读取直到结束
context3 = res1.readlines()
print(context3)

# 返回请求状态吗
print(res1.getcode())
# 返回url
print(res1.geturl())
# 返回状态信息
print(res1.getheaders())

# 下载
# 参数1url是要下载的路径，第二个参数是文件的名称filename
urllib = req.urlretrieve()
