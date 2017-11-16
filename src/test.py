import urllib
from urllib import  request
import requests

request_headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
'Referer':'http://www.quanshuwang.com/'
}
html1 = urllib.request.urlopen('http://www.quanshuwang.com/list/1_1.html').read().decode('GBK')

html2 = requests.get('http://www.quanshuwang.com/list/1_1.html',headers=request_headers)
html2.encoding = 'gbk'
print(html2.text)