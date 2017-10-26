#!/usr/bin/python
# -*- coding: UTF-8 -*-


import json
import requests
import sqlite3
import time
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

DB_NAME = 'taobaomm.db'

def get_data():
    is_continue = True
    url = 'https://mm.taobao.com/tstar/search/tstar_model.do'
    dict = {'_input_charset':'utf-8',"currentPage":1}
    while is_continue:
        response = requests.post(url,dict)
        if response.status_code == 200:
            str = response.content
            di = json.loads(str,encoding="GBK")
            if di['status'] == 1:
                ls = di['data']['searchDOList']
                print t(), "开始保存第%d页",dict['currentPage'];
                if True:
                    save_data(ls)
                else:
                    try:
                        save_data(ls)
                    except Exception as e:
                        print e
                        exit()
                print t(), "保存完毕第%d页",dict['currentPage'];
                dict['currentPage'] += 1
            else:
                is_continue = False

def save_data(ls):
    conn = sqlite3.connect(DB_NAME)
    for dict in ls:
        userId = dict.get('userId')
        totalFanNum = dict.get('totalFanNum', 0)
        totalFavorNum = dict.get('totalFavorNum', 0)
        avatarUrl = dict.get('avatarUrl', '')
        cardUrl = dict.get('cardUrl', '')
        city = dict.get('city', '')
        height = dict.get('height', '')
        identityUrl = dict.get('identityUrl', '')
        modelUrl = dict.get('modelUrl', '')
        realName = dict.get('realName', '').replace("'", '"')
        viewFlag = dict.get('viewFlag', '')
        weight = dict.get('weight', '')
        is_exists = userid_exists(conn,dict)
        if is_exists:
            #"UPDATE COMPANY set SALARY = 25000.00 where ID=1"
            sql = "UPDATE MM set totalFanNum = %d where userId=%d"% (totalFanNum,userId)
            conn.cursor().execute(sql)
            sql = "UPDATE MM set totalFavorNum = %d where userId=%d"% (totalFavorNum,userId)
            conn.cursor().execute(sql)
            sql = "UPDATE MM set avatarUrl = '%s' where userId=%d"% (avatarUrl,userId)
            conn.cursor().execute(sql)
            sql = "UPDATE MM set cardUrl = '%s' where userId=%d" % (cardUrl,userId)
            conn.cursor().execute(sql)
            sql = "UPDATE MM set city = '%s' where userId=%d"% (city,userId)
            conn.cursor().execute(sql)
            sql = "UPDATE MM set height = '%s' where userId=%d"% (height,userId)
            conn.cursor().execute(sql)
            sql = "UPDATE MM set identityUrl = '%s' where userId=%d"% (identityUrl,userId)
            conn.cursor().execute(sql)
            sql = "UPDATE MM set modelUrl = '%s' where userId=%d"% (modelUrl,userId)
            conn.cursor().execute(sql)
            sql = "UPDATE MM set realName = '%s' where userId=%d"% (realName,userId)
            conn.cursor().execute(sql)
            sql = "UPDATE MM set viewFlag = '%s' where userId=%d"% (viewFlag,userId)
            conn.cursor().execute(sql)
            sql = "UPDATE MM set weight = '%s' where userId=%d"% (weight,userId)
            conn.cursor().execute(sql)
        else:
            sql = "INSERT INTO MM (userId,totalFanNum,totalFavorNum,avatarUrl,cardUrl,city,height,identityUrl,modelUrl,realName,viewFlag,weight) " \
                  "VALUES (%d,%d,%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s') " \
                  % (userId, totalFanNum, totalFavorNum, avatarUrl, cardUrl, city, height, identityUrl, modelUrl,realName,viewFlag, weight)
            conn.cursor().execute(sql)
    conn.commit()
    conn.close()

def t():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def replace(s):
    return s.replace('\\','')

def userid_exists(conn,dict):
    sql = "SELECT userId FROM MM where userId=%d" % dict['userId']
    ls = conn.cursor().execute(sql).fetchall()
    if len(ls) > 0:
        return  True
    else:
        return False

def creat_db():
    conn = sqlite3.connect(DB_NAME)
    print t(),"Opened database successfully";
    sql = '''CREATE TABLE MM
               (userId INT PRIMARY KEY   NOT NULL,
               totalFanNum     INT,
               totalFavorNum     INT,
               avatarUrl     TEXT,
               cardUrl     TEXT,
               city        TEXT,
               height        TEXT,
               identityUrl     TEXT,
               modelUrl     TEXT,
               realName     TEXT,
               viewFlag     TEXT,
               weight     TEXT)'''

    try:
        conn.cursor().execute(sql)
        print t(),"Table created successfully";
    except Exception as e:
        print t(),e
        if e.message != 'table MM already exists':
            exit()
    conn.close()


def main():
    creat_db()
    get_data()
    pass

if __name__ == '__main__':
    print t(), "程序开始完毕"
    main()
    print t(),"程序运行完毕"