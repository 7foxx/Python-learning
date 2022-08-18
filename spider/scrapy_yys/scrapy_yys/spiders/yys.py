from time import sleep
from urllib.parse import urlencode
from selenium.webdriver.common.by import By

import scrapy
from selenium import webdriver

from scrapy_yys.items import ScrapyYysItem


class YysSpider(scrapy.Spider):
    name = 'yys'
    allowed_domains = ['act.ds.163.com']
    start_urls = ['http://act.ds.163.com/41bab2a03a354547/']

    def parse(self, response):
        div_list = response.xpath('//*[@id="root"]/div/div')
        # 删除前两个元素
        div_list.pop(0)
        div_list.pop(0)
        for li in div_list:
            # 名称
            name = li.xpath('.//div/div[2]/div/span[1]/text()').extract_first()
            CV = li.xpath('.//div/div[2]/div/span[2]/text()').extract_first()
            quality = li.xpath('.//div/div[2]/div/i[1]//@class').extract_first().split('___')[0].replace('quality', '')
            positioning = li.xpath('.//div/div[2]/p/text()').extract_first()
            iconUrl = li.xpath('.//div/div[1]/img//@src').extract_first()

            # 式神详细信息
            url = f'https://act.ds.163.com/41bab2a03a354547/item-detail?{urlencode({"id": name})}'

            yield scrapy.Request(url=url, callback=self.parse_item, meta={
                "name": name,
                "CV": CV,
                "quality": quality,
                "positioning": positioning,
                "iconUrl": iconUrl
            })

    def parse_item(self, response):
        driver = response.meta['driver']
        isform = response.xpath('//*[@id="root"]/div/div[2]/div[1]/span[2]')
        skill = {}
        # 当前式神所有技能图标
        skillIconArr = []

        # 获取技能信息函数
        def changeSkill(response, typeText):
            # 变身前
            container = response.xpath(
                '//*[@id="root"]//div[@class="skillContent___3IYll"]/div[@class="container___kfFAF"]')
            skillArr = []
            for div in container:
                # 技能图片ICON
                skillIcon = div.xpath('.//*[@class="skillIcon___2kIqu"]//@src').extract_first()
                # 技能名称
                skill = {}
                skillName = div.xpath('.//div[1]/span[1]/text()').extract_first()
                # 消耗
                skillCost = div.xpath('.//div[1]/span[2]/p/text()').extract_first()
                # 类型
                skillType = div.xpath('.//div[1]/span[3]/text()').extract_first()
                skill[skillType] = skillName
                skill["消耗"] = skillCost

                # 描述
                skillText = div.xpath('.//div[2]/p').extract_first()
                skill["描述"] = skillText

                # 升级
                skillLevelUp = []
                skillLevelUpUl = div.xpath('.//ul/li')
                for li in skillLevelUpUl:
                    key = li.xpath('.//span[1]/text()').extract_first()
                    value = li.xpath('.//span[2]/text()').extract_first()
                    skillLevelUp.append({
                        key: value
                    })
                skill["等级提升"] = skillLevelUp

                skillArr.append(skill)
                # 当前式神所有技能图标
                skillIconArr.append([f'{typeText}_{skillName}_{skillType}', skillIcon])

            return skillArr

        skill['变身前'] = changeSkill(response, '变身前')
        # 判断是否有有多种形态
        if isform != []:
            # 点击更新界面
            driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/span[2]').click()
            # 等待 0.5 秒，执行js
            sleep(0.5)
            # 变身后
            skill['变身后'] = changeSkill(response, '变身后')
            driver.quit()
            print('关闭 webdriver')
        else:
            driver.quit()
            print('关闭 webdriver')

        # 例会
        subjectImg = response.xpath('//*[@id="root"]/div/div[1]/div[1]/div[2]/img//@src').extract_first()

        # 属性
        AttributeData = []
        eleData = response.xpath('//*[@id="root"]/div/div[1]/div[1]/div[1]/ul/li')
        for i, li in enumerate(eleData):
            # 属性数值
            key = li.xpath('.//*[@class="leftFeature___3fDr2"]/text()').extract_first()
            value1 = li.xpath('.//*[@class="rightFeature___1uJ5q"]/text()[1]').extract_first()
            value2 = li.xpath('.//*[@class="rightFeature___1uJ5q"]/text()[2]').extract_first()
            if value2: value2.strip()

            # 属性评级
            val1 = \
                li.xpath(f'//*[@id="root"]/div/div[1]/div[2]/div/div[{i + 1}]/span[2]/@class').extract_first().split(
                    '___')[
                    0].replace('level', '')
            val2 = \
                li.xpath(f'//*[@id="root"]/div/div[1]/div[2]/div/div[{i + 1}]/span[4]/@class').extract_first()
            if val2:
                val2 = val2.split(
                    '___')[
                    0].replace('level', '')
            AttributeData.append({
                f"{key}": [value1, value2],
                "quality": [val1, val2]
            })

        # 觉醒后icon
        iconUrl2 = response.xpath('//*[@id="root"]/div/div[3]/div[2]/div[1]/span[3]/img/@src').extract_first()

        # 觉醒材料
        effectListArr = response.xpath('//*[@id="root"]/div/div[3]/div[2]/div[2]/ul/li')
        effectList = []
        for li in effectListArr:
            key = li.xpath('.//*[@class="name___1LkkY"]/text()').extract_first()
            value = li.xpath('.//*[@class="count___2NsWO"]/text()').extract_first()
            effectList.append({
                key: value
            })

        # 推荐御魂
        RoyalSoulArr = response.xpath('//*[@id="root"]/div/div[4]/div[@class="container___3BN3k"]')
        if RoyalSoulArr:
            RoyalSoul = []
            for div in RoyalSoulArr:
                # 方案
                soulCount1 = div.xpath('.//div[2]/span[2]/text()').extract_first()
                soulCount2 = div.xpath('.//div[2]/span[4]/text()').extract_first()
                # 主属性
                mainAttr = {}
                for v in [2, 4, 6]:  mainAttr[v] = div.xpath(
                    f'//*[@id="root"]/div/div[4]/div[2]/div[3]/span[{v + 1}]/text()').extract_first()

                RoyalSoul.append({
                    "方案": [soulCount1, soulCount2],
                    "主属性": mainAttr
                })
        else:
            RoyalSoul = []

        yield ScrapyYysItem(
            name=response.meta['name'],
            CV=response.meta['CV'],
            quality=response.meta['quality'],
            positioning=response.meta['positioning'],
            imgUrl={
                "icon_1": response.meta['iconUrl'],
                "icon_2": iconUrl2,
                "subjectImg": subjectImg,
                "skillIconArr": skillIconArr
            },
            HellspawnData={
                "AttributeData": AttributeData,
                "skill": skill,
                "effectList": effectList,
                "RoyalSoul": RoyalSoul
            }
        )

    def close(self, reason):
        pass
