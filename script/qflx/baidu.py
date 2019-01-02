"""
简单爬虫，爬百度搜索图片“风暴”
"""
#objURL 百度图片的链接
from urllib.request import *
# 用来处理网络访问
import re
url='http://image.baidu.com/search/index?tn=baiduimage&ct=201326592&cl=2&lm=-1&pv=&word=%E9%A3%8E%E6%9A%B4&z=0&ie=utf-8'
html=urlopen(url) # 用来打开一个网页
# html代码
obj=html.read().decode()  #获取html代码，并解码
urls=re.findall(r'"objURL":"(.*?)"',obj)  #
print(urls)
# 下载资源
index=0
for url in urls:
    try:
        urlretrieve(url,'pic'+str(index)+'.jpg')
        index +=1
    except Exception:
        print("download erro....%d"%index)
    finally:
        print("download complete")