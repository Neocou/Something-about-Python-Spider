#coding:UTF-8
import requests
import re
import pymysql
import multiprocessing
from multiprocessing import Pool
import time




#爬取目标站点: http://www.quanshuwang.com/
#小说总的分类
sort_dic = {
    1:'玄幻魔法',
    2:'武侠修真',
    3:'纯爱耽美',
    4:'都市言情',
    5:'职场校园',
    6:'穿越重生',
    7:'历史军事',
    8:'网游动漫',
    9:'恐怖灵异',
    10:'科幻小说',
    11:'美文名著'
    }


#请求头
request_headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
'Referer':'http://www.quanshuwang.com/'
}

#已爬小说网页列表
down_novel_list =[]
#已爬章节网页列表
down_chapter_list =[]
#数据库类
class Sql(object):
    conn = pymysql.connect('127.0.0.1','root','password','novel',use_unicode=True, charset="utf8")
    #增加小说
    def addnovel(self,sort,sortname,novelname,imgurl,description,status,author):
        try:   
            cur = self.conn.cursor()
            sql = "insert ignore into novel(sort,sortname,novelname,imgurl,description,status,author) values(%s,'%s','%s','%s','%s','%s','%s')" %(sort,sortname,novelname,imgurl,description,status,author)
            cur.execute(sql)
            lastrowid = cur.lastrowid
            cur.close()
            self.conn.commit()
        except Exception as e:
            print(e)
        return lastrowid #返回创建的主键(自增长的)
    #增加章节
    def addchapter(self,novelid,title,content):
        try:
            cur = self.conn.cursor()
            cur.execute("insert ignore into chapter(novelid,title,content) values(%s,'%s','%s')" %(novelid,title,content))
            cur.close()
            self.conn.commit()
        except Exception as e:
            print(e)
            
            
mysql = Sql()#拿到数据库实例

#编码处理
def get(url):
    html = requests.get(url,headers=request_headers,timeout = 8)
    html.encoding = 'gbk'
    return html.text


#得到小说信息并加入数据库
def get_novel(url,sort_id,sort_name):
    html = get(url)
    reg = r'<meta property="og:novel:book_name" content="(.*?)"/>'
    book_name = re.findall(reg,html)[0]
    reg = r'<meta property="og:description" content="(.*?)"/>'
    book_description = re.findall(reg,html,re.S)[0]
    reg = r'<meta property="og:image" content="(.*?)"/>'
    book_img = re.findall(reg,html)[0]
    reg = r'<meta property="og:novel:author" content="(.*?)"/>'
    book_author = re.findall(reg,html)[0]
    reg = r'<meta property="og:novel:status" content="(.*?)"/>'
    book_status = re.findall(reg,html)[0]
    reg = r'<a href="(.*)?" class="reader"'
    book_url = re.findall(reg,html)[0]
    novelid = mysql.addnovel(sort_id,sort_name,book_name,book_img,book_description,book_status,book_author)
    print('获得小说编号%s基本信息' %(novelid))
    get_chapter_list(book_url,novelid)

#得到每本小说的章节目录，并依次进行数据库插入
def get_chapter_list(url,novelid):
    print('爬取小说编号：%s章节列表' %(novelid))
    html = get(url)
    reg = r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>'
    chapter_info = re.findall(reg, html)
    for url_detail,title in chapter_info:
        get_chapter_content(url, url_detail,novelid,title)
    print('爬取小说编号：%s章节完毕' %(novelid))
#获得每本小说下的章节内容被加入数据库
def get_chapter_content(url,url_detail,novelid,title):
    chapter_url = '%s/%s'%(url,url_detail)
    if chapter_url not in down_chapter_list: 
        down_chapter_list.append(chapter_url)
        print("爬取小说编号：%s '%s'章节内容" %(novelid,title))
        html = get(chapter_url)
        reg =r'style5\(\);</script>(.*?)<script type="text/javascript">style6'
        content = re.findall(reg, html, re.S)[0]
        mysql.addchapter(novelid, title, content)
        print("爬取小说编号：%s '%s'章节内容完毕" %(novelid,title))
#获得每一分类下的小说列表
def get_list(sort_id,sort_name):
    i = 1
    while('true'):
        html = get('http://www.quanshuwang.com/list/%s_%s.html' %(sort_id,i))
        reg = r'<a target="_blank" href="(.*?)" class="l mr10">'   
        url_list = re.findall(reg, html)
        if url_list:
            print('开始爬取%s_%s'%(sort_id,i))
            for url in url_list:
                if url not in down_novel_list:
                    down_novel_list.append(url)
                    try:
                        get_novel(url,sort_id,sort_name)
                    except Exception as e:
                        print(e)
            i +=1
            print('爬取%s_%s完毕'%(sort_id,i))
        else:
            print('%s分类已爬完' %(sort_id))
            return
    
#程序入口，使用进程池
if __name__ == '__main__':
    p = Pool(multiprocessing.cpu_count())
    for sort_id,sort_name in sort_dic.items():
        p.apply_async(get_list,args =(sort_id,sort_name))
    print('开启小说进程池')
    p.close()
    p.join()
    print('进程全部结束')