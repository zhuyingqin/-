import requests
import threading
from bs4 import BeautifulSoup
"""

proxy.txt —— 所有爬到的代理
verified.txt —— 所有可用代理

"""
lock = threading.Lock()
inFile = open('proxy.txt')
outFile = open('verified.txt', 'w')

def getProxyList(targeturl="http://www.xicidaili.com/nn/"):
    countNum = 0
    proxyFile = open('proxy.txt', 'a')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/62.0.3202.62 Safari/537.36'}
    for page in range(1, 10):
        url = targeturl + str(page)
        request = requests.get(url, headers=headers).text
        soup = BeautifulSoup(request, "html.parser")
        trs = soup.find('table', id='ip_list').find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            if tds[0].find('img') is None:      # 国家的图片
                nation = '未知'
                locate = '未知'
            else:
                nation = tds[0].find('img')['alt'].strip()  # 国家
                locate = tds[3].text.strip()    # 服务器地址
            ip = tds[1].text.strip()            # IP地址获取
            port = tds[2].text.strip()          # 端口号
            anony = tds[4].text.strip()         # 是否高匿IP
            protocol = tds[5].text.strip()      # 类型 HTTP
            speed = tds[6].find('div')['title'].strip()     # 速度
            time = tds[8].text.strip()
            proxyFile.write('%s|%s|%s|%s|%s|%s|%s|%s\n' % (nation, ip, port, locate, anony, protocol, speed, time))
            print('%s=%s:%s' % (protocol, ip, port))
            countNum += 1

    proxyFile.close()
    return countNum


def verifyProxyList():
    """
    验证代理IP的有效性
    并保存入txt格式中
    :return:
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/62.0.3202.62 Safari/537.36'}
    while True:
        lock.acquire()
        ll = inFile.readline().strip()
        lock.release()
        if len(ll) == 0:
            break
        line = ll.strip().split('|')
        protocol = line[5]
        ip = line[1]
        port = line[2]
        proxies = {protocol: ip+":"+port}
        try:
            requests.get('https://www.baidu.com/',
                         timeout=5.0,
                         headers=headers,
                         proxies=proxies,
                         )
        except:
            print('connect failed')
        else:
            lock.acquire()
            outFile.write(ll + "\n")
            lock.release()


if __name__ == '__main__':
    tmp = open('proxy.txt', 'w')
    tmp.write("")
    tmp.close()
    getProxyList(targeturl="http://www.xicidaili.com/nn/")
    all_thread = []

    for i in range(30):     # 修改线程数
        t = threading.Thread(target=verifyProxyList)
        all_thread.append(t)
        t.start()
    for t in all_thread:
        t.join()

    inFile.close()
    outFile.close()
    print("All Done.")