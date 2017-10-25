import re
import datetime
import scrapy
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
import requests
import json
from sina.items import InformationItem, TweetsItem, FollowsItem, FansItem

class SinaspiderSpider(CrawlSpider):
    name = "sinaSpider"
    allowed_domains=['https://m.weibo.cn']
    # start_urls=[
    #   5340337769,1642630543,1704116960,1310630777,
    # ]
    # headers={
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Accept-Language": "en,zh-CN;q=0.8,zh;q=0.6",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    #     "Host": "www.douban.com",
    # }
    ids=[
        "6311254871",
    ]
    scrawl_ID=set(ids) #记录待爬的微博ID
    finish_ID=set() #记录已爬的微博ID

    def start_requests(self):
        while self.scrawl_ID.__len__():
            ID=self.scrawl_ID.pop()
            self.finish_ID.add(ID)
            
            #个人信息
            url_information0="https://m.weibo.cn/api/container/getIndex?type=uid&value=%s" %ID
            print url_information0
            yield Request(url=url_information0, meta={"ID": ID}, callback=self.parseInformation)

    def parseInformation(self,response):
        """ 抓取个人信息1 """
        if len(response.body) > 50:
            print "###########################"
            print "Fetch information0 Success"
            print "###########################"

            informationItems=InformationItem()
            informations=json.loads(response.body)
            if informations.get("userInfo",""):
                informationItems["_id"]=informations["userInfo"]["id"]
                informationItems["NickName"]=informations["userInfo"]["screen_name"]
                informationItems["Signature"]=informations["userInfo"]["description"]
                informationItems["Num_Tweets"]=informations["userInfo"]["statuses_count"]
                informationItems["Num_Follows"]=informations["userInfo"]["follow_count"]
                informationItems["Num_Fans"]=informations["userInfo"]["followers_count"]
                yield informationItems

            #微博入口
            tweets_container_id=informations["tabsInfo"]["tabs"][1]["containerid"]
            url_tweets = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=%s" % (response.meta["ID"],tweets_container_id)
            yield Request(url=url_tweets, meta={"ID": response.meta["ID"]}, callback=self.parseTweets, dont_filter=True)


            #关注者入口
            if informations.get("follow_scheme",""):
                follow_scheme=informations["follow_scheme"]
                follow_container_id=re.findall(r"containerid=(.*)",follow_scheme)
                follow_container_id[0]=follow_container_id[0].replace('followersrecomm','followers')
                url_follow="https://m.weibo.cn/api/container/getIndex?containerid="+follow_container_id[0]
                yield Request(url=url_follow, meta={"ID": response.meta["ID"]}, callback=self.parseFollows, dont_filter=True)

            #粉丝入口
            if informations.get("fans_scheme",""):
                fans_scheme=informations["fans_scheme"]
                fans_container_id=re.findall(r"containerid=(.*)",fans_scheme)
                fans_container_id[0]=fans_container_id[0].replace('fansrecomm','fans')
                url_fans="https://m.weibo.cn/api/container/getIndex?containerid="+fans_container_id[0]
                yield Request(url=url_fans,meta={"ID": response.meta["ID"]},callback=self.parseFans, dont_filter=True)
        else:
            print "###########################"
            print "Fetch information0 Fail"
            print "###########################"
            return 

        

    def parseTweets(self,response):
        if len(response.body) > 50:
            print "###########################"
            print "Fetch Tweets Success"
            print "###########################"

            tweets=json.loads(response.body)
            ID=response.meta["ID"]
            page=''
            containerid=''
            if tweets.get("cards",""):
                cards=tweets["cards"]
                if tweets["cardlistInfo"].get("page",""):
                    page=tweets["cardlistInfo"]["page"]
                    page=str(page)
                else:
                    return
                if tweets["cardlistInfo"].get("containerid",""):
                    containerid=tweets["cardlistInfo"]["containerid"]
                for card in cards:
                    mblog=card.get('mblog','')
                    if mblog:
                        tweetsItems=TweetsItem()
                        tweetsItems["_id"]=card["itemid"]
                        tweetsItems["ID"]=ID
                        tweetsItems["Content"]=json.dumps(mblog)
                        tweetsItems["PubTime"]=mblog["created_at"]
                        tweetsItems["Like"]=mblog["attitudes_count"]
                        tweetsItems["Comment"]=mblog["comments_count"]
                        tweetsItems["Transfer"]=mblog["reposts_count"]
                    yield tweetsItems           
                print "###########################"
                print "Tweetspage: "+page
                print "###########################"
                url_tweets="https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=%s&page=%s" % (ID,containerid,page)
                yield Request(url=url_tweets,meta={"ID": ID},callback=self.parseTweets,dont_filter=True)
            else:
                return 
        else:
            print "###########################"
            print "Fetch Tweets Finish"
            print "###########################"
            return 

    def parseFollows(self,response):
        if len(response.body) > 50:
            print "###########################"
            print "Fetch Follows Success"
            print "###########################"

            page=''
            containerid=''
            follow=json.loads(response.body)
            if follow.get("cardlistInfo",""):
                if follow["cardlistInfo"].get("page",""):
                    page=follow["cardlistInfo"]["page"]
                    page=str(page)
                else:
                    return
                if follow["cardlistInfo"].get("containerid",""):
                    containerid=follow["cardlistInfo"]["containerid"]
            else:
                return

            ID=response.meta["ID"]
            if follow.get("cards",""):
                cards=follow["cards"]           
                card_group=cards[len(cards)-1]["card_group"]
                for card in card_group:
                    if card:
                        followsItems=FollowsItem()
                        followsItems["ID"]=ID
                        followsItems["_id"]=card["user"]["id"]
                        followsItems["NickName"]=card["user"]["screen_name"]
                        followsItems["Signature"]=card["desc1"]
                        followsItems["Num_Tweets"]=card["user"]["statuses_count"]
                        followsItems["Num_Follows"]=card["user"]["follow_count"]
                        followsItems["Num_Fans"]=card["user"]["followers_count"]
                        followsItems["profile_url"]=card["user"]["profile_url"]
                        yield followsItems
                print "###########################"
                print "Followspage: "+page
                print "###########################"
                url_follow="https://m.weibo.cn/api/container/getIndex?containerid=%s&page=%s" % (containerid,page)
                yield Request(url=url_follow,meta={"ID": ID},callback=self.parseFollows,dont_filter=True)
            else:
                return
        else:
            print "###########################"
            print "Fetch Follows Finish"
            print "###########################"
            return

    def parseFans(self,response):
        if len(response.body) > 50:
            print "###########################"
            print "Fetch Fans Success"
            print "###########################"

            fans=json.loads(response.body)
            ID=response.meta["ID"]
            containerid=''
            since_id=''
            if fans.get("cardlistInfo",""):
                if fans["cardlistInfo"].get("since_id",""):
                    since_id=fans["cardlistInfo"]["since_id"]
                    since_id=str(since_id)
                else:
                    return
                if fans["cardlistInfo"].get("containerid",""):
                    containerid=fans["cardlistInfo"]["containerid"]

            if fans.get("cards",""):
                cards=fans["cards"]
                for card in cards:
                    card_group=card["card_group"]
                    for element in card_group:
                        if element:
                            fansItems=FansItem()
                            fansItems["_id"]=element["user"]["id"]
                            fansItems["ID"]=ID
                            fansItems["NickName"]=element["user"]["screen_name"]
                            fansItems["Signature"]=element["user"]["description"]
                            fansItems["Num_Tweets"]=element["user"]["statuses_count"]
                            fansItems["Num_Follows"]=element["user"]["follow_count"]
                            fansItems["Num_Fans"]=element["user"]["followers_count"]
                            fansItems["profile_url"]=element["user"]["profile_url"]
                            yield fansItems
            
                print "###########################"
                print "Fas_since_id: "+since_id
                print "###########################"
                fans_url="https://m.weibo.cn/api/container/getIndex?containerid=%s&since_id=%s" % (containerid,since_id)
                yield Request(url=fans_url,meta={'ID':ID},callback=self.parseFans,dont_filter=True)
            else:
                return
        else:
            print "###########################"
            print "Fetch Fans Finish"
            print "###########################"
            return