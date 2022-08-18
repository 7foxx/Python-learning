# 原神官网新闻

import json
import re
import urllib.request
import urllib.parse

url = "https://content-static.mihoyo.com/content/ysCn/getContentList?"

data = {
    "pageSize": 10000,
    "pageNum": 1,
    "channelId": 10
}
data = urllib.parse.urlencode(data)
urlAll = url + str(data)

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

URL = urllib.request.Request(urlAll, headers=headers)
res = urllib.request.urlopen(URL)

bodyArr = json.loads(res.read().decode('utf-8'))['data']['list']

rolePV = []
roleMV = []
verisonPV = []
EV = []
longImg = []
ThePlot = []
gossip = []
MentionWatt = []
TheSkin = []
for list in bodyArr:
    title = list['title']
    url = "https://ys.mihoyo.com/main/news/detail/" + list['contentId']
    if re.search(r'角色PV', title):
        rolePV.append({
            f"{title}": url
        })
    elif re.search(r'角色演示', title):
        roleMV.append({
            f"{title}": url
        })
    elif re.search(r'版本PV', title):
        verisonPV.append({
            f"{title}": url
        })
    elif re.search(r'EP', title):
        EV.append({
            f"{title}": url
        })
    elif re.search(r'长图', title):
        longImg.append({
            f"{title}": url
        })
    elif re.search(r'剧情PV', title):
        ThePlot.append({
            f"{title}": url
        })
    elif re.search(r'拾枝杂谈', title):
        gossip.append({
            f"{title}": url
        })
    elif re.search(r'《原神·提瓦特篇》', title):
        MentionWatt.append({
            f"{title}": url
        })
    elif re.search(r'衣装PV', title):
        TheSkin.append({
            f"{title}": url
        })

objs = {
    "rolePV": rolePV,
    "roleMV": roleMV,
    "verisonPV": verisonPV,
    "EV": EV,
    "longImg": longImg,
    "ThePlot": ThePlot,
    "gossip": gossip,
    "MentionWatt": MentionWatt,
    "TheSkin": TheSkin
}
f = open('data.json', 'w', encoding='utf-8')

# write 方法必须写一个字符串
f.write(json.dumps(objs))
print(objs)