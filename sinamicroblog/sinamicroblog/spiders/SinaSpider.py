import re
import datetime
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from sinamicroblog.items import FansItem
from scrapy.conf import settings
"""
参考网址
1.http://blog.csdn.net/qq_30242609/article/details/52822190 //Scrapy定向爬虫教程(五)——保持登陆状态
2.http://blog.csdn.net/qq_30242609/article/details/54581674 //Scrapy请求头文件教程
3.http://blog.csdn.net/qq_30242609/article/details/54581674 //Scrapy shell 如何cookies,headers请求
4.http://blog.csdn.net/peihaozhu/article/details/53022236   //Scrapy中关于Export Unicode字符集问题解决
5.https://github.com/wly2014/ImageSpider/blob/master/ImgInWebsite/spiders/ImgSpider.py //scrapy迭代
"""

class Spider(CrawlSpider):
    name = "sinaSpider"
    host = "http://weibo.cn"
    start_urls = [5601402881,]
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    'Connection': 'keep-alive',
    }
    # meta = {
    #     'dont_redirect': True,  # 禁止网页重定向
    #     'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    # }
    scrawl_ID = set(start_urls)  # 记录待爬的微博ID
    finish_ID = set()            # 记录已爬的微博ID
    cookie = settings['COOKIE']  # 带着Cookie向网页发请求

    def start_requests(self):
        """
        访问地址和微博的登陆
        """
        while self.scrawl_ID.__len__():
            ID = self.scrawl_ID.pop()   # 将待爬取ID获取后删除
            self.finish_ID.add(ID)      # 加入已爬队列
            ID = str(ID)                # ID信息转换为字符串
            # follows = []
            # followsItems = FollowsItem()
            # followsItems["_id"] = ID
            # followsItems["follows"] = follows
            fans = []
            fansItems = FansItem()
            fansItems["_id"] = ID
            fansItems["fans"] = fans
            # url_follows = "http://weibo.cn/%s/follow" % ID
            url_fans = "http://weibo.cn/%s/fans" % ID
            # url_tweets = "http://weibo.cn/%s/profile?filter=1&page=1" % ID
            # url_information0 = "http://weibo.cn/attgroup/opening?uid=%s" % ID
            # yield Request(url=url_follows, meta={"item": followsItems, "result": follows},
            #             callback=self.parse3)  # 去爬关注人
            yield Request(url=url_fans, meta={"item": fansItems, "result": fans}, 
                        callback=self.parse3, cookies=self.cookie, headers=self.headers, dont_filter=True)  # 去爬粉丝
            # yield Request(url=url_information0, meta={"ID": ID}, 
            #             callback=self.parse0)  # 去爬个人信息
            # yield Request(url=url_tweets, meta={"ID": ID}, 
            #             callback=self.parse2)  # 去爬微博

    def parse3(self, response):
        """ 抓取关注或粉丝 """
        items = response.meta["item"]
        selector = Selector(response)
        text2 = selector.xpath('//table/tr/td/a/text()').extract()
        """
        text2 return :
        ['重庆大学城市科技学院网络中心', '移除', '也关注他', '私信', 
        'Sylvia_77-', '备注', '移除', '私信', 
        '3043815940QRt', '移除', '也关注她', '私信', 
        '严沁188', '移除', '也关注她', '私信',
        '连美慧1981', '移除', '也关注她', '私信', 
        '热情黎浩贤', '移除', '也关注她', '私信', 
        '222pm飞烟', '移除', '也关注他', '私信',
        '地盘井上织姬1981', '移除', '也关注她', '私信',
        '再见侠客1983', '移除', '也关注她', '私信',
        '丽华Joanna', '移除', '也关注她', '私信']
        """
        count=0
        for IDS in selector.xpath('//td/a/@href').extract():
            IDS = re.findall('uid=(\d+)', IDS)
            if IDS:
                ID = int(IDS[0])
                if ID not in self.finish_ID:
                    self.scrawl_ID.add(ID)
        for elem in text2:
            if count%2==0 and count<len(text2):
                response.meta["result"].append(text2[count])
                count+= 1
            # ID = int(elem[0])
                # if ID not in self.finish_ID:  # 新的ID，如果未爬则加入待爬队列
                #     self.scrawl_ID.add(ID)
            count+= 1


        url_next = selector.xpath(
            'body//div[@id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        
        if url_next:
            yield Request(url=self.host + url_next[0], meta={"item": items, "result": response.meta["result"]},
                          callback=self.parse3)
        else:  # 如果没有下一页即获取完毕
            # ID = self.scrawl_ID.pop()
            # url_fans = "http://weibo.cn/%s/fans" % ID
            # yield Request(url_fans,meta={"item": items, "result": response.meta["result"]},callback=self.start_requests,cookies=self.cookie)
            yield items
        if self.scrawl_ID:
            ID = self.scrawl_ID.pop()
            url_fans = "http://weibo.cn/%s/fans" % ID
            yield Request(url_fans,meta={"item": items, "result": response.meta["result"]},callback=self.parse3
                ,cookies=self.cookie, headers=self.headers, dont_filter=True)
        else:  # 如果没有下一页即获取完毕
            # ID = self.scrawl_ID.pop()
            # url_fans = "http://weibo.cn/%s/fans" % ID
            # yield Request(url_fans,meta={"item": items, "result": response.meta["result"]},callback=self.start_requests,cookies=self.cookie)
            yield items