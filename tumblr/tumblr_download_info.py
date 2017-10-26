#!/usr/bin/python
# -*- coding: UTF-8 -*-
# nohup python -u run.py > log.txt 2>&1 &

import json
import time
import os
import urllib2


api_key = "jrsCWX1XDuVxAFO4GkK147syAoN8BJZ5voz8tS80bPcj26Vc5Z"
limit = 50

def getUser(users):
    for i , user in enumerate(users):
        is_continue = True
        param = {'user': user, 'offset': 0}
        while is_continue:
            is_continue = getUserdata(param)
            param['offset'] += limit

def getUserdata(param):
    user = param['user']
    offset = param['offset']
    url = 'https://api.tumblr.com/v2/blog/' + user + '.tumblr.com/posts'
    parme = {'api_key': api_key, 'limit': limit, 'offset': offset}
    t = time.time()
    content = ''
    try:
        print '\n',user, ' 网络请求', offset / limit + 1,time.asctime(time.localtime(time.time()))
        url  = '%s?api_key=%s&limit=%d&offset=%d' % (url,api_key,limit,offset)
        request = urllib2.Request(url)
        request.get_method = lambda: 'GET'
        response = urllib2.urlopen(request)
        content = response.read()
    except Exception as e:
        print e
        getUserdata(param)
    dict = json.loads(content)
    total_posts = 0
    if dict['meta']['status'] != 200:
        print "服务器数据异常"
        print dict['meta']['msg']
        return
    total_posts = dict['response']['total_posts']
    print user,' 网络请求成功',offset/limit + 1 ,'/',total_posts/limit + 1,'/',total_posts,"耗时:",time.time() - t
    t = time.time()
    if len(dict['response']['posts']) == 0:
        print "已达到上限"
        return False
    else:
        save_file(dict,user,offset)
        print "文件数据处理完毕；", "耗时:", time.time() - t
        return True

def save_file(dict,user,offset):
    txt = json.dumps(dict['response'])
    model = 'w'
    if offset > 0: model = 'a'
    if setup_data_dir('data'):
        with open('data/' + user + '.txt', model) as f:
            f.write(txt)
            f.write('\n')

def setup_data_dir(directory):
    """ 设置文件夹，文件夹名为传入的 directory 参数，若不存在会自动创建 """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            pass
    return True

def run(users):
    print "程序开始运行"
    print len(users), "个用户名"
    print users
    simplyRun(users)
    print "所有用户获取完毕"

def simplyRun(users):
    print "使用单线程开始任务"
    if setup_data_dir('data'):
        getUser(users)
    return
    try:
        if setup_data_dir('data'):
            getUser(users)
    except Exception as e:
        print e

if __name__ == '__main__':
    users = ['wei--liang','hd08116', 'godmmm',  'hinbsksksbjdjd', 'lonely-start', 'hb-loli', 'liu5375', "zhling1994",
             "mjj1024"]
    run(users)