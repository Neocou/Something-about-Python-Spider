# Something-about-Python-Spider
最近学习python写的一点爬虫，记录总结一些问题

## beautifultest.py
使用bs4爬取多张图片。

爬取目标站点:http://www.tuku.cn/bizhi/tuji2715_page1.aspx ~ http://www.tuku.cn/bizhi/tuji2715_page4.aspx 下的高清大图。

第一次尝试爬虫。
![beautifultest](https://github.com/Neocou/Something-about-Python-Spider/blob/master/pic/beautifultest1.PNG)

## pooltest.py
爬取目标站点:http://www.tuku.cn/

在前一爬虫的基础加入进程池

![pooltest1](https://github.com/Neocou/Something-about-Python-Spider/blob/master/pic/pooltest1.PNG)

![pooltest2](https://github.com/Neocou/Something-about-Python-Spider/blob/master/pic/pooltest2.PNG)


## novel.py

使用多进程爬取指定小说网，原本计划是爬完，但是本地数据库mysql装太多，加载太慢，不过按照进度应该是可以爬完的。

爬取目标站点: http://www.quanshuwang.com/
![novel1](https://github.com/Neocou/Something-about-Python-Spider/blob/master/pic/novel1.PNG)

![novel2](https://github.com/Neocou/Something-about-Python-Spider/blob/master/pic/novel2.PNG)

![novel3](https://github.com/Neocou/Something-about-Python-Spider/blob/master/pic/novel3.PNG)

![novel4](https://github.com/Neocou/Something-about-Python-Spider/blob/master/pic/novel4.PNG)

![novel5](https://github.com/Neocou/Something-about-Python-Spider/blob/master/pic/novel5.PNG)

![novel6](https://github.com/Neocou/Something-about-Python-Spider/blob/master/pic/novel6.PNG)


## Jiepai.py
使用多线程爬取今日头条图片下搜索'美女'的前80条结果里面的所有图片，并加入数据库(PS:美女项目可修改),主要是模拟请求然后分析异步返回的json结果。
爬取目标站点: https://www.toutiao.com/
![picture1](https://github.com/Neocou/Something-about-Python-Spider/blob/master/pic/picture1.PNG)

![picture2](https://github.com/Neocou/Something-about-Python-Spider/blob/master/pic/picture2.PNG)

![picture3](https://github.com/Neocou/Something-about-Python-Spider/blob/master/pic/picture3.PNG)

## Video.py

爬取目标站点：http://www.budejie.com/

使用requests库爬取小视频

![video1](https://github.com/Neocou/Something-about-Python-Spider/blob/master/pic/video1.PNG)

![video2](https://github.com/Neocou/Something-about-Python-Spider/blob/master/pic/video2.PNG)

### 源代码都有基本注释，应该比较清楚，另外我还有一个项目是使用scrapy框架爬取全站的图片,有兴趣的可以转战到[Python-Scrapy-Mzitu](https://github.com/Neocou/Python-Scrapy-Mzitu)

### 补充
novel.py涉及到两张表，原始表我也没有存，不过比较简单，一个是小说表，一个是章节表。
根据代码中的两条插入语句，应该是很好建表的，如有问题对应修改吧。另外其他代码如果有用到数据库部分，应该都在代码看得出来，没有复杂的建表过程。

insert ignore into novel(sort,sortname,novelname,imgurl,description,status,author)

insert ignore into chapter(novelid,title,content) values(%s,'%s','%s')

