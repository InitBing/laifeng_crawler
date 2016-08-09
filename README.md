# laifeng_crawler
爬取来疯首页所有正在直播的房间里的聊天信息
##client
创建单个聊天房间聊天client，调用run（）函数，参数为正在直播的房间号。当直播停止，client自动关闭。运行前安装websocket-client。
##grnumber
爬去来疯直播首页上所有正在直播的房间号。
##muti_client
可以直接运行，通过多进程同时爬去所有正在直播的房间的聊天信息，并输出到文件。
