#coding=utf-8
import json
import requests
import urllib
import os
from multiprocessing import Pool
import pymysql

#加入多线程
#加入存入数据库
#目标今日头条图片下搜索'美女'的前80条结果里面的所有图片


#mysql数据库test 表为 pic(pic_id,pidc_name,pidc_path) 请对应更改密码
conn = pymysql.connect('127.0.0.1',user ='root',password = 'root',db='test',use_unicode=True, charset="utf8")
cur = conn.cursor()

root_dir = 'D:\picture' #保存在D:\picture 这里不做检测创建

request_headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
'Referer':'https://www.toutiao.com/search/?keyword=%E7%BE%8E%E5%A5%B3'
}

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print("创建文件夹{}成功".format(path.split('\\')[-1]))
    return path

def get_query_string(data):
    return urllib.parse.urlencode(data)

def get_article_urls(req):
    res = urllib.request.urlopen(req).read()
    d = json.loads(res.decode('utf-8')).get('data')
    if d is None:
        print('数据请求完毕')
        return
    titles = [article.get('title') for article in d]
    for i in range(20):
        try:
            img_li = d[i]['image_detail']
            for j in img_li:
                save_photo(j.get('url'), titles[i])
        except Exception as e:
            print(e)
            continue
    return titles

def save_photo(photo_url,save_dir):
    photo_name = photo_url.rsplit('/',1)[-1]+'.jpg'
    res = requests.get(photo_url,timeout = 20)
    save_path = root_dir +'\\'+save_dir
    create_dir(save_path)
    with open (save_path+'\\'+photo_name,'wb') as f:
        path = save_path+'\\'+photo_name
        path = path.replace('\\', '\\\\')
        f.write(res.content)
        sql = "insert ignore into pic(pic_name,pic_path) values('{pic_name}','{pic_path}')".format(pic_name=photo_name,pic_path=path)
        cur.execute(sql)
        conn.commit()
        print('已下载图片并加入数据库：{dir_name}/{photo_name}'.format(dir_name=save_dir,photo_name=photo_name))


def once(start,end):
    offset = start
    while offset<end:
            query_data = {
            'offset':offset,
            'format':'json',
            'keyword':'美女',#搜索项目可以更改
            'autoload':'true',
            'count':'20',
            'cur_tab':'1'
            }
            query_url = 'https://www.toutiao.com/search_content/?'+get_query_string(query_data)
            try:
                article_req = urllib.request.Request(query_url,headers=request_headers,timeout = 20)
            except Exception as e:
                print(e)
                continue
            title = get_article_urls(article_req)
            if not title:
                break
            offset+=20
            

if __name__ == '__main__':
    p = Pool(4)
    for i in range(4):
        p.apply_async(once,args=(i*20,20+i*20))
    print('测试进程池')
    p.close()
    p.join()
    print('进程全部结束')
    cur.close()
    conn.close()




