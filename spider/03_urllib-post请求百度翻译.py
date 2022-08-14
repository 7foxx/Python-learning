import json
import urllib.request as request
import urllib.parse as parse

url = 'https://fanyi.baidu.com/sug'

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

data = {
    'kw': 'spider'
}

# post 请求参数必须进行编码
# urlencode 编码的是二进制的所以我们需要用 encode 再次编码为 utf-8 的格式
data = parse.urlencode(data).encode('utf-8')

# 请求对象定制
UrlALl = request.Request(url, data, headers=headers)

# 发送请求
response = request.urlopen(UrlALl)

# 请求响应数据
context = response.read().decode('utf8')

obj = json.loads(context)

print(obj)

