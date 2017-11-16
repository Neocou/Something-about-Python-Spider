import requests
from bs4 import BeautifulSoup
import os
from multiprocessing import Pool #导入所需模块

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
         'Cookie':'td_cookie=18446744069699913059; td_cookie=18446744073473691510; __cfduid=d3c82ddb98a603fb7fdff368278b6672a1506862174; cf_clearance=b7c9ed4f96e90f9b5ba57725427e210fd50d00c9-1507604344-14400; AJSTAT_ok_pages=1; AJSTAT_ok_times=3'
        }

def parser_index(index_url):
    res=request(index_url)
    soup=BeautifulSoup(res.text,'html.parser')
    img_urls=soup.find_all('div',class_='disp_img1')
    for img_url in img_urls:
        number=img_url.find_all('img')[0]['alt'][12:-9] #解析出数字给图片命名
        download(img_url.find_all('img')[0]['src'],number)
def download(img_url,number): #下载保存
    content=request(img_url).content
    filepath='{}.{}'.format(number,'jpg')
    if not os.path.exists(filepath): #判断是否有重复图片
        with open(filepath,'wb') as f:
            f.write(content)
            
def request(url):
    content=requests.get(url,headers=headers,timeout = 20)
    return content

if __name__ == '__main__':
    print('父进程    %s.' % os.getpid()) #父进程ID
    p=Pool(4) #创建进程池
    for i in range(1,5):
        url='http://www.tuku.cn/bizhi/tuji2715_page{}.aspx'.format(i)
        p.apply_async(parser_index,args=(url,))#子进程任务函数和参数
    print('等待子进程结束...')
    p.close()
    p.join()
    print('所有进程结束 .')