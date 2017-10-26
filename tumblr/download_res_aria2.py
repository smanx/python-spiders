#!/usr/bin/python
# -*- coding: UTF-8 -*-
# nohup python -u download_res_aria2.py > download_res_aria2.log 2>&1 &

import time
import json
import os


ALLCOUNT = 0
COUNT = 0
RETRY = 0
DOWNLOADERROR = []
DIRECTORY = '/Users/htc/Pictures/test'


def get_info():
    """ 获取所有图片组的信息 """
    res = []
    t = time.time()
    with open('data/hb-loli.txt', 'r') as f:
        for line in f:
            data = json.loads(line)
            res.extend(data['posts'])
    print time.time() - t
    print len(res)
    return res


def get_info_res(filenames):
    """ 获取要下载的所有图片url、目录名、要存储的名字 """
    res = []

    for idx, filename in enumerate(filenames):
        print "开始导入 %s  %d/%d" % (filename, idx + 1, len(filenames))
        with open('data/' + filename, 'r') as f:
            for line in f:
                data = json.loads(line)
                posts = data['posts']
                for post in posts:
                    name = post['blog']['name']
                    title = post['blog']['title']
                    uuid = post['blog']['uuid']
                    id = post['id']
                    file_name = name + '----' + title
                    slug = post['slug']
                    summary = post['summary']
                    urls = []
                    directory = os.path.join(DIRECTORY, uuid)
                    if post.has_key('photos'):
                        for i, photo in enumerate(post['photos']):
                            url = photo['original_size']['url']
                            footer = url[url.rfind("."):len(url)]
                            filepath = os.path.join(directory, "%d_%d%s" % (id, i + 1, footer))
                            res.append((directory, filepath, url))
                    if post.has_key('video'):
                        url = post['video']['sizes']['original']['url']
                        footer = url[url.rfind("."):len(url)]
                        filepath = os.path.join(directory, "%d%s" % (id, footer))
                        res.append((directory, filepath, url))
        print "导入完成 %s  %d/%d" % (filename, idx + 1, len(filenames))
    return res


# 下载所有资源
def download(res):
    start_time = time.time()
    global ALLCOUNT, COUNT, DOWNLOADERROR, RETRY
    ALLCOUNT = len(res)
    COUNT = 0
    setup_download_dir('res')
    singleDownload(res)
    end_time = time.time()
    print'下载完毕,用时:%s秒' % (end_time - start_time)


def singleDownload(res):
    print "用单线程任务开始"
    for i, r in enumerate(res):
        download_one(r)


def download_one(res):
    """ 下载一张图片 """
    directory, filepath, url = res
    global ALLCOUNT, COUNT, DOWNLOADERROR, RETRY
    COUNT = COUNT + 1
    # print "\n"
    # 如果文件已经存在，放弃下载
    print time.asctime(time.localtime(time.time())), '准备下载', url, "==>", filepath,
    setup_download_dir(directory)
    if os.path.exists(filepath) == 1 and os.path.exists(filepath + '.aria') == 0:
        print time.asctime(time.localtime(time.time())), "资源存在跳过", COUNT, ALLCOUNT
        return
    try:
        print time.asctime(time.localtime(time.time())), "资源开始下载", COUNT, ALLCOUNT

        str = 'aria2c --check-certificate=false -c -x16 -s20 -j20 -o ' + '"' + filepath + '" "' + url + '"'
        # print '===================>',str
        print '===================>', os.system(str)
    except Exception as e:
        print "资源下载出错，总计:", len(DOWNLOADERROR), "重试次数:", RETRY
        print e
        DOWNLOADERROR.append(res)
        print e


def setup_download_dir(directory):
    """ 设置文件夹，文件夹名为传入的 directory 参数，若不存在会自动创建 """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            pass
    return True


def run():
    list = os.listdir('data/')
    users = []
    for filename in list:
        if filename[len(filename) - 4:len(filename)] == '.txt':
            users.append(filename)
    res = get_info_res(users)
    download(res)


if __name__ == "__main__":
    # 参数为线程数，0为单线程
    run()