import requests
import re
import urllib
import os


#要爬取的目录
#正则表达式
#该项目爬取多个.mp4文件并保存在d:/video下，请先建立video
#未使用header
start_urls = ['http://www.budejie.com/{}'.format(i) for i in range(1,12)]

def get_response(url):
    response = requests.get(url,timeout = 20).text
    return response

def get_content(html):
    reg = re.compile(r'(<div class="j-r-list-c">.*?</div>.*?</div>)',re.S)
    return re.findall(reg, html)

def get_mp4_url(response):
    reg = r'data-mp4="(.*?)"'
    return re.findall(reg, response)

def get_mp4_name(response):
    reg = re.compile('<a href="/detail-\d{8}.html">(.*?)</a>',re.S)#加了re.S后可以检测换行
    return re.findall(reg, response)
    
def download_mp4(mp4_url,path):
    path = 'D:/video/{}.mp4'.format(path)#先video这里我就不检测创建了
    if not os.path.exists(path):
        urllib.request.urlretrieve(mp4_url,path)
        print("downloading:{}".format(path))
    else:
        print("---------------------")
        print("已经下载过了")
def video_download(url):
    content = get_content(get_response(url))
    for i in content:
            mp4_url = get_mp4_url(i)
            print("查看链接")
            print(mp4_url)
            print('-------------------------------')
            if  mp4_url:
                mp4_name = get_mp4_name(i)
                print(mp4_name)
                try:
                    download_mp4(mp4_url[0], mp4_name[0])
                except Exception as e:
                    print(e)
                    continue
def start():
    for url in start_urls:
        video_download(url)
    print("结束任务!")    
if __name__ == '__main__':
    start()
            