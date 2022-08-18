# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import os

from itemadapter import ItemAdapter
from urllib.request import urlretrieve
import pymysql  # 导入模块

# 导入数据库
db = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='951299034.glf',
    db='YYS',
    charset='utf8'
)

# 获取一个游标对象
cursor = db.cursor()


class ScrapyYysPipeline:
    def __init__(self):
        self.fb = None

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        name = item.get("name")
        path = f'../img/hellspawn/{name}'
        # 判断目录是否存在
        if os.path.exists(path) is False:
            # 不存在泽创建目录
            os.makedirs(path)
        # 下载icon头像
        urlretrieve(item["imgUrl"]["icon_1"], f'{path}/icon_1_{name}.png')
        # 判断是否有觉醒
        if item["imgUrl"]["icon_2"]:
            urlretrieve(item["imgUrl"]["icon_2"], f'{path}/icon_2_{name}.png')
        # 下载例会
        urlretrieve(item["imgUrl"]["subjectImg"], f'{path}/max_1_{name}.png')
        # 下载技能
        for v in item["imgUrl"]["skillIconArr"]: urlretrieve(v[1], f'{path}/{v[0]}.png')
        # 删除imgUrl
        del item["imgUrl"]
        # 插入数据库
        HellspawnData = item['HellspawnData']
        AttributeData = str(json.dumps(HellspawnData["AttributeData"]))
        RoyalSoul = str(json.dumps(HellspawnData["RoyalSoul"]))
        effectList = str(json.dumps(HellspawnData["effectList"]))
        skill_1 = str(json.dumps(HellspawnData["skill"]["变身前"]))
        if "变身后" in HellspawnData["skill"]:
            skill_2 = str(json.dumps(HellspawnData["skill"]["变身后"]))
        else:
            skill_2 = "Null"
        SQL = f"""INSERT INTO hellspawn_data(name,quality,positioning,AttributeData,RoyalSoul,effectList,skill_1,skill_2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor.execute(SQL, (item['name'],item['quality'],item['positioning'],AttributeData, RoyalSoul, effectList,skill_1,skill_2))
            # 提交
            db.commit()
        except:
            db.rollback()
        return item

    def close_spider(self, spider):
        pass
