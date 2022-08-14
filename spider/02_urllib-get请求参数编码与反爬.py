import urllib.request as req
import urllib.parse

url = 'https://www.baidu.com/s?'
# 对请求进行编码
kwd = urllib.parse.quote('原神')
print(kwd)
urlAll = url + kwd

data = {
    'wd':'原神'
}

data = urllib.parse.urlencode(data)
print(data)

# 请求制定解决反爬的第一种手段
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

# 模拟浏览器发送请求

request = req.Request(urlAll, headers=headers)
res = req.urlopen(request)
print(res.read().decode('utf8'))