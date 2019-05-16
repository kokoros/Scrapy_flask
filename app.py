from flask import Flask, render_template
#导入redis
import redis

from random import choice
from flask import Flask, jsonify, request

#导入mongo
import pymongo

import json
import re

import os

import requests

import csv


app = Flask(__name__)

# 连接mongo数据库
conn = pymongo.MongoClient('localhost', 27017)
# 库名
db = conn['spider']
# 集合对象
myset = db['job']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_ip')
def find_ip():
    os.chdir("/home/koro/Scrapy_ip/Ippool")
    os.system("gnome-terminal -e 'python3 begin.py'")
    return "终端正在爬取可用ip,请稍等..."

@app.route('/find_job')
def find_job():
    os.chdir("/home/koro/Scrapy_job/Job")
    # path = os.getcwd()
    # print(path)
    os.system("gnome-terminal -e 'python3 begin.py'")
    return "请在终端输入要查询的岗位,正在爬取前程无忧,请稍等..."

@app.route('/show_job')
def show_job():
    return render_template('table.html')


def job_location(address, city):
    '''利用高德地图api实现地址和经纬度的转换'''
    parameters = {'address': address, 'key': 'a94b95d38e56af49e9098c22efe8afb1'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    print('answer', answer)
    # res = answer['geocodes'][0]['location']
    print(address + "的经纬度：")
    return res


@app.route('/job_all_map')
def job_all_map():
    '''生成地图'''
    #生成csv文件
    with open('location.csv', 'w') as f:
        #岗位名称,城市,区,坐标
        fieldnames = ["name", "city", "area", "company", "center"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        #写入表头
        writer.writeheader()
        # 查找全部
        cursor = myset.find()
        for d in cursor:
            name = d['job_name']
            company = d['company'].replace('.', '')
            if '-' in d['address']:
                address_list = d['address'].split('-')
                # print(address_list)
                city = address_list[0]
                area = ''
                if '.' not in address_list[1]:
                    area = address_list[1]
            count = 0
            while count < 3:
                print(company)
                #获取location值
                center = job_location(address=company, city=city)
                # print(center)
                # print(name, city, area, company, center)
                count += 1

            #写入一行
            # writer.writerow({"name": name, "city": city, "area": area, "company": company, "center": center})
    return render_template('map.html')




@app.route('/jsondata', methods=['POST', 'GET'])
def infos():
    #查找全部
    cursor = myset.find()
    #一个列表来放数据
    data = []

    for d in cursor:
        data.append(d)

    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        print('get', limit)
        print('get  offset', offset)
        return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
    # 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
    # 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了
    elif request.method == 'POST':
        # print('searchString')
        # 一个列表来放数据
        data = []
        key = request.form.get('key', '')
        print(key)
        # 用正则来模糊查询
        # 查询job_name中包含key的记录：
        for u in myset.find({'job_name': re.compile(key)}):
            data.append(u)
        print(data)
        # json_str = json.dumps(data)

        return jsonify({'total': len(data), 'rows': data})

@app.route('/ip')
def get_ip():
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    ip_list = r.srandmember('ip', 1)
    return ip_list[0]



if __name__ == '__main__':
    app.run()
