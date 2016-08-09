#! /usr/bin/env python
# coding:utf-8
# author:wenhui

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re          #正则表达式
import urlparse    #urlparse模块主要是把url拆分为6部分，并返回元组。并且可以把拆分后的部分再组成一个url。主要有函数有urljoin、urlsplit、urlunsplit、urlparse等
import urllib
import urllib2
import socket
import cookielib
import websocket
import grnumber
import threading


try:
    import thread
except ImportError:  # TODO use Threading instead of _thread in python3
    import _thread as thread

import time
'''
import logging
import logging.handlers
import logging.config


cur_path_ = os.path.dirname(__file__)
LOG_FILE = os.path.join(cur_path_, 'logs/main.log')  
handler = logging.handlers.RotatingFileHandler(LOG_FILE, \
    maxBytes = 500*1024*1024, backupCount = 3)  
fmt = "%(name)s %(levelname)s %(filename)s:%(lineno)s %(asctime)s %(process)d:%(thread)d  %(message)s"  
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)    

logger = logging.getLogger('main')    
#logger.addHandler(handler)  
#logger.setLevel(logging.DEBUG)

#ws_logger = logging.getLogger('webs')
'''


def unzipData(zipped_data):
    import StringIO, gzip, zlib
    uzfile = gzip.GzipFile(mode='rb', fileobj=StringIO.StringIO(zipped_data))
    content = uzfile.read()
    uzfile.close()
    return content


def on_message(ws, message):
    init_send_data=ws.init_send_data
    ws.fp.write("message\t%s\t%s\n"% (init_send_data['roomid'],message))
    print("message\t%s" % message)
    if message == "1:::":
        global init_send_data

        ws.send('5:::{"name":"enter","args":[{"token":"%s","uid":"%s","roomid":"%s","isPushHis":"1","yktk":"","endpointtype":"ct_,dt_1_1000|0|%s_%s"}]}' % (init_send_data['token'],init_send_data['userid'],init_send_data['roomid'],init_send_data['mk'],int(time.time()*1000)))
        ws.send('5:::{"name":"PatronSaint","args":[{"rid":"%s"}]}' % init_send_data['roomid'])
        ws.send('5:::{"name":"PondData","args":[{"_sid":"PondData%s"}]}' % int(time.time()*1000))
        ws.send('5:::{"name":"GroupColorInit","args":[{"_sid":"GroupColorInit%s"}]}' % int(time.time()*1000))
        ws.send('5:::{"name":"TaskRedPointCount","args":[{"_sid":"TaskRedPointCount%s"}]}' % int(time.time()*1000))
        ws.send('5:::{"name":"DailyTaskInit","args":[{"t":0,"_sid":"DailyTaskInit%s"}]}'% int(time.time()*1000))
        ws.send('5:::{"name":"subscribe","args":[{"msgName":"vipuserlist","isSub":"false"}]}')
        ws.send('5:::{"name":"subscribe","args":[{"msgName":"BubbleUserList","isSub":"false"}]}')
    elif message == "2:::":
        ws.send("2::")


def on_error(ws, error):
    print("error:%s" % error)


def on_close(ws):
    print("close ...")


def on_open(ws):
    print("open ...")


def prepare_request(url):
    request_ = urllib2.Request(url)
    url_parse = urlparse.urlparse(url)   #将url分解

    request_.add_header('Accept',
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    request_.add_header('Accept-Encoding','gzip,deflate,sdch')
    request_.add_header('Accept-Language','zh-CN,zh;q=0.8') 
    request_.add_header('Host',url_parse.netloc)
    request_.add_header('Referer','http://www.laifeng.com/')
    request_.add_header('Upgrade-Insecure-Requests','1')
    request_.add_header('User-Agent',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36')
    return request_


    
def run(roomid,fp):
    
    userid,token,mk,ws_host = '','','',''
    room_url = "http://v.laifeng.com/%s" % roomid   

    #room_id_match = re.search(r"http://v.laifeng.com/(\d+)",room_url)
    #roomid = room_id_match.group(1)

     #获取一个保存cookie的对象 
    cookie_jar = cookielib.LWPCookieJar() 

    #将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
    #urllib2.urlopen()函数不支持验证、cookie或者其它HTTP高级功能。要支持这些功能，必须使用build_opener()函数创建自定义Opener对象 
    # 对cookie进行处理，什么处理？
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))  

    request_ = prepare_request(room_url)                                    #prepare_request?

    ret_1 = opener.open(request_,timeout=7)                                 #打开请求，设定相应时间

    content = unzipData(ret_1.read())                                       #解包

    
    room_info_match = re.search(r"DDS.baseInfo = (\{.*?\});",content,re.S)

    if room_info_match:
        room_info = room_info_match.group(1)
        token_match = re.search(r"token:'(.*?)',",room_info)
        token = token_match.group(1) if token_match else ""
        """
        roomid_match = re.search(r"roomId:'(.*?)',",room_info)
        roomid = roomid_match.group(1) else ""
        """
    user_info_match = re.search(r"DDS.userInfo = (\{.*?\});",content,re.S)

    if user_info_match:
        user_info = user_info_match.group(1)
        userid_match = re.search(r"userId:'(.*?)',",user_info)
        userid = userid_match.group(1) if userid_match else ""

    request_ = prepare_request('http://dispatcher.notify.laifeng.com/%s?callback=jQuery11020597382007260167_1468918114859&_=%s' % (roomid,int(time.time()*1000)))
    ret_2 = opener.open(request_,timeout=7)
    content = unzipData(ret_2.read())
    ws_host_match = re.search(r"jQuery11020597382007260167_1468918114859\(\{\"host\":\"(.*?)\"\}\)",content)
    if ws_host_match:ws_host = ws_host_match.group(1)

    for cookie in cookie_jar:
        if cookie.name == 'mk':mk=cookie.value
        
  
    
    init_send_data = {'roomid':roomid,'userid':userid,'token':token,'mk':mk,'ws_host':ws_host}
    
    print("init send_data:%s" % init_send_data)

    
    
    websocket.enableTrace(True)
    
    ws = websocket.WebSocketApp('ws://%s/socket.io/1/websocket/' % ws_host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.init_send_data = init_send_data
    ws.fp=fp
    ws.on_open = on_open
    ws.run_forever()
    
   




#if __name__ == "__main__":
 #       run()
