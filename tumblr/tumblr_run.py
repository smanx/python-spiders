#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tumblr_download_info
import download_res
import download_res_aria2


#需要爬的用户数组，请根据需要修改
#users = ['hd08116','godmmm','wei--liang','hinbsksksbjdjd','lonely-start',,'liu5375',"zhling1994","mjj1024"]
users = ['hb-loli','hd08116','wei--liang']
try:
    #下载数据
    tumblr_download_info.run(users)
    #下载资源
    #普通下载
    download_res.run()
    # aria2下载，需安装aria2
    #download_res_aria2.run()
except Exception as e:
    print e

print "程序运行完毕"
