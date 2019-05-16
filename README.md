Pro_web:爬取岗位信息的web接口
===================

Getting Started
--------------
* 进入外层目录: 
     cd spider_flask
* 开启Django2.1服务:
     python3 app.py

Prerequisites(先决条件)
----------------------
* Flask
* python3
* Scrapy

Running the tests
-----------------
* 打开chrome firefox 等浏览器
* 输入网址:http://127.0.0.1:5000/

main
----------------
* 先爬取西刺至少一天内可用的ip,存储到redis中
* 读取redis中的ip,存为爬取工作文件的Scarpy的中间件
* 利用动态ip爬取前程无忧网站并存入mongodb中
* 利用Bootstrap-table 展示数据
* 利用高德API标记工作地点

Built With
------
* Flask
* python3
* Redis
* Bootstrap
* 高德API

Authors
-----------
kokoros
