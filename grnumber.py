#!/usr/bin/python
#coding:utf-8
#从来疯首页爬取正在直播的房间
#edit by niozhan, 25/6/2016


import urllib
import urllib2
import cookielib
import urlparse
import types
import re
from bs4 import BeautifulSoup
from bs4 import NavigableString

def get_soup_data():
    url="http://v.laifeng.com"
    cookie_jar = cookielib.LWPCookieJar() 

    #将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
    #urllib2.urlopen()函数不支持验证、cookie或者其它HTTP高级功能。要支持这些功能，必须使用build_opener()函数创建自定义Opener对象 
    # 对cookie进行处理，什么处理？   
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
    request_ = urllib2.Request(url)
    url_parse = urlparse.urlparse(url)  
    request_.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    request_.add_header('Accept-Language','zh-CN,zh;q=0.8') 
    request_.add_header('Host',url_parse.netloc)
    request_.add_header('Referer','http://www.laifeng.com/')
    request_.add_header('Upgrade-Insecure-Requests','1')
    request_.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36')
    content = opener.open(request_,timeout=7)#打开请求，设定相应时间
    soup=BeautifulSoup(content,'html.parser')
    return soup


def get_room_num():
    soup=get_soup_data()
    res_room_number=[]
    for tag in soup.find_all(target="_blank",href=re.compile("v.laifeng.com")):
      tmp=tag.get('href')
      tmp=tmp+'s'
      num= re.findall(r"m/(.+)s",tmp)
      res_room_number.append(num)
    return res_room_number


    









    
    
    




