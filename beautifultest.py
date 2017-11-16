import requests
from bs4 import BeautifulSoup


#使用bs4爬取多张图片
#目标http://www.tuku.cn/bizhi/tuji2715_page1.aspx~http://www.tuku.cn/bizhi/tuji2715_page4.aspx下的高清大图

#headers request的请求头，防止被认出是爬虫请求被禁止
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
 'Cookie':'td_cookie=18446744069694360802; td_cookie=18446744073473691510; __cfduid=d3c82ddb98a603fb7fdff368278b6672a1506862174; cf_clearance=6cc99c976e6cdae345fadd5797d8dcb89ac34909-1507376519-14400; ASP.NET_SessionId=ffcz0a2kcuvanwfqhtibxdwv; AJSTAT_ok_pages=2; AJSTAT_ok_times=2'
}
#n用来给图片编号
n=1
for i in range(1,5):
    url='http://www.tuku.cn/bizhi/tuji2715_page{}.aspx'.format(i) # format还是挺好的，用好了可以简化代码很多
    res=requests.get(url,headers=headers)
    soup=BeautifulSoup(res.text,'html.parser')
    img_urls=soup.find_all('div',class_='disp_img1')
    for img_url in img_urls:
        next_url = '{}/{}'.format('http://www.tuku.cn/bizhi',img_url.find('a')['href'])
        print(next_url)
        img_soup =BeautifulSoup(requests.get(next_url,headers=headers).text,'html.parser')
        pic_res = requests.get(img_soup.find('img',id='Image2')['src'],headers=headers)
        filepath='{}.{}'.format(n,'jpg') #文件路径
        with open(filepath,'wb') as f: #打开文件
            print('写入%s'%(filepath))
            f.write(pic_res.content)
        n+=1


        