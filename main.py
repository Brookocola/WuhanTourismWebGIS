from flask import render_template

from flask import make_response

from flask import Flask, session, redirect, url_for, escape, request

import chardet
import jieba

import os
from os import path
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
from matplotlib import pyplot as plt
# from scipy.misc import imread
import random

import requests
import json
import csv

from flask import abort
from flask import jsonify
from flask.helpers import make_response
from flask_cors import *

import psycopg2
from psycopg2 import extras
import uuid
import hashlib
import datetime


# CONSTANT

USERNAME = 'postgres'
PASSWORD = '051914'
SALT = '\h33wf_asef-9*^&II#2'
MAX_INT = 2147483647

def getcomments(poiID,Name,path):
    postUrl = "https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList"

    # 将景点poiId和名称添加到此处
    urls = [
        [poiID, Name]
    ]

    for id in urls:
        print("正在爬取景点：", id[1])
        # 通过返回值判断总评论数，每页9条，计算出总页数，对大于2000条的数据只爬取两千条

        data_pre = {
            "arg": {
                "channelType": 2,
                "collapseType": 0,
                "commentTagId": 0,
                "pageIndex": 1,
                "pageSize": 10,
                "poiId": id[0],
                "sourceType": 1,
                "sortType": 3,
                "starType": 0
            },
            "head": {
                "cid": "09031027214030973865",
                "ctok": "",
                "cver": "1.0",
                "lang": "01",
                "sid": "8888",
                "syscode": "09",
                "auth": "",
                "xsid": "",
                "extension": []
            }
        }

        html = requests.post(postUrl, data=json.dumps(data_pre)).text
        html = json.loads(html)

        # 确定总页数总页数
        total_page = int(html['result']['totalCount']) / 9
        if total_page > 111:
            total_page = 111
        # 2000条太多，运行太慢，爬1000不够再加
        # 遍历查询评论
        print("总页数:", total_page, "爬取中")

        # # 创建写入txt文件
        # path = "/result/"+str(id[1]) + 'comments.txt'
        xuhao = 0
        with open(path, 'w', newline='', encoding='utf-8') as f:
            file = csv.writer(f)
            file.writerow(['序号', '景区ID', '景区名称', '评论'])
            for page in range(1, total_page + 1):
                data = {
                    "arg": {
                        "channelType": 2,
                        "collapseType": 0,
                        "commentTagId": 0,
                        "pageIndex": page,
                        "pageSize": 10,
                        "poiId": id[0],
                        "sourceType": 1,
                        "sortType": 3,
                        "starType": 0
                    },
                    "head": {
                        "cid": "09031027214030973865",
                        "ctok": "",
                        "cver": "1.0",
                        "lang": "01",
                        "sid": "8888",
                        "syscode": "09",
                        "auth": "",
                        "xsid": "",
                        "extension": []
                    }
                }
                html = requests.post(postUrl, data=json.dumps(data)).text
                html = json.loads(html)
                # 获取评论
                for j in range(1, 10):
                    result = html['result']['items'][j]['content']
                    file.writerow([xuhao, id[0], id[1], result])
                    xuhao += 1
        print(id[1], "爬取完成")



def myWordCloud(fData,fImg,fResult):
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # 用chardet监测编码
    # text = open(path.join(d,'外卖评论.txt'),'rb').read()
    # text_charInfo = chardet.detect(text.encode)
    # print(text_charInfo)
    # # 结果{'encoding': 'UTF-8-SIG', 'confidence': 1.0, 'language': ''}

    text = open(path.join(d, fData), encoding='utf-8').read()

    stopwords = open(path.join(d, r'停用词库.txt'), encoding='utf-8').read()

    content_after = ''
    for word in text:
        if word not in stopwords:
            if word != '\t' and '\n':
                content_after += word

    content_after = content_after.replace("   ", " ").replace("  ", " ")
    # print(content_after)
    # 写入去停止词后生成的新文本
    with open('previewDatatmp.txt', 'w', encoding='utf-8') as f:
        f.write(content_after)

    text = open(path.join(d, r'previewDatatmp.txt'), encoding='utf-8').read()
    print(text)

    text += ' '.join(jieba.cut(text, cut_all=False))  # cut_all=False 表示采用精确模式
    print(text)

    # 读取背景图片
    background_Image = np.array(Image.open(path.join(d, fImg)))
    # 提取背景图片颜色
    img_colors = ImageColorGenerator(background_Image)
    # 设置中文停止词
    stopwords = set('')
    stopwords.update(
        ['武汉','吃', '挺', '错', '味', '送', '太', '的', '了', '我', '还', '都', '就', '是', '啊', '但是', '一个', '自己', '因此', '没有', '很多', '可以',
         '这个', '虽然', '因为', '这样', '已经', '现在', '一些', '比如', '不是', '当然', '可能', '如果', '就是', '同时', '比如', '这些', '必须', '由于',
         '而且', '并且', '他们'])

    wc = WordCloud(
        # font_path = font_path,
        font_path='simhei.ttf',  # 中文需设置路径
        margin=2,  # 页面边缘
        mask=background_Image,
        scale=2,

        max_words=200,  # 最多词个数
        min_font_size=4,  #
        stopwords=stopwords,
        random_state=42,
        background_color='white',  # 背景颜色
        # background_color = '#C3481A', # 背景颜色
        max_font_size=100,
        repeat=True
    )
    wc.generate(text)

    # 获取文本词排序，可调整 stopwords
    # process_word = WordCloud.process_text(wc,text)
    # sort = sorted(process_word.items(),key=lambda e:e[1],reverse=True)
    # print(sort[:50]) # 获取文本词频最高的前50个词

    # 设置为背景色，若不想要背景图片颜色，就注释掉
    wc.recolor(color_func=img_colors)
    # 存储图像
    wc.to_file(fResult)

    # # 显示图像
    # plt.imshow(wc,interpolation='bilinear')
    # plt.axis('off')
    # plt.tight_layout()
    # plt.show()


def wordcloud2(Data,fImg,fRes):
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    # t = open(path.join(d, fData), encoding='utf-8').read()
    s=Data.split(',')



    text={s[0]:0.5,s[1]:0.4,s[2]:0.3,s[3]:0.2,s[4]:0.1}

    # print(text)




    # 读取背景图片
    background_Image = np.array(Image.open(path.join(d, fImg)))
    # 提取背景图片颜色
    img_colors = ImageColorGenerator(background_Image)

    wc = WordCloud(
        # font_path = font_path,
        font_path='simhei.ttf',  # 中文需设置路径
        margin=2,  # 页面边缘
        mask=background_Image,
        scale=2,
        max_words=200,  # 最多词个数
        min_font_size=13,  #
        # # stopwords=stopwords
        collocations=True,
        random_state=42,
        background_color='white',  # 背景颜色
        # # background_color = '#C3481A', # 背景颜色
        max_font_size=100,
        repeat=True
    )

    wc.generate_from_frequencies(text)

    # 获取文本词排序，可调整 stopwords
    # process_word = WordCloud.process_text(wc,text)
    # sort = sorted(process_word.items(),key=lambda e:e[1],reverse=True)
    # print(sort[:50]) # 获取文本词频最高的前50个词

    # 设置为背景色，若不想要背景图片颜色，就注释掉
    wc.recolor(color_func=img_colors)
    # 存储图像
    wc.to_file(fRes)

    # # 显示图像
    # plt.imshow(wc, interpolation='bilinear')
    # plt.axis('off')
    # plt.tight_layout()
    # plt.show()

def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream  = base64.b64encode(img_f.read()).decode()

    return img_stream



app = Flask(__name__)

app.secret_key = 'fkdjsafjdkfdlkjfadskjfadskljdsfklj'

@app.route('/')
def foo():

   return  render_template('layout.html')



@app.route('/layout', methods = ['GET', 'POST'])

def layout():
    return render_template('layout.html')

@app.route('/ourword', methods = ['GET', 'POST'])

def ourword():

   return render_template('ourword.html')


@app.route('/lou',methods = ['GET', 'POST'])
def lou():
   return render_template('lou.html')

@app.route('/xue',methods = ['GET', 'POST'])
def xue():
   return render_template('xue.html')
@app.route('/guan',methods = ['GET', 'POST'])
def guan():
   return render_template('guan.html')

# 更新词云图
@app.route('/updatewc',methods = ['GET', 'POST'])
def updatewc():
    fResult = "result/黄鹤楼词云.jpg"
    # 需要修改前面的静态路径
    img_path = "C:/Users/86157/Desktop/WuhanTourismWebGIS/" + fResult

    fimg = "static/img/黄鹤楼mask.jpg"
    poiID = '77593'
    Name = '黄鹤楼'
    # 需要修改前面的静态路径
    tpath = "C:/Users/86157/Desktop/WuhanTourismWebGIS/result/" + Name + 'comments.txt'

    getcomments(poiID,Name,tpath)
    myWordCloud(tpath, fimg, fResult)
    img_stream = return_img_stream(img_path)
    return render_template('show2.html', img_stream=img_stream)

# 自定义词云视图
@app.route('/show2',methods = ['GET', 'POST'])
def show2():
  if request.method == 'POST':
      txt=request.form['txt1']+","+request.form['txt2']+","+request.form['txt3']+","+request.form['txt4']+","+request.form['txt5']+","

      fResult = "result/黄鹤楼自定义词云.jpg"
      # 需要修改前面的静态路径
      img_path="C:/Users/86157/Desktop/WuhanTourismWebGIS/"+fResult

      fimg="static/img/黄鹤楼mask.jpg"

      wordcloud2(txt,fimg,fResult)
      img_stream = return_img_stream(img_path)
      return render_template('show2.html',img_stream=img_stream)
  else:return '<h2>erro</h2>'

@app.route('/selfword', methods = ['GET', 'POST'])

def selfword():

    if request.method == 'POST':

        return redirect(url_for('show2'))

    return render_template('selfword.html')

# 功能2地图标记评论
@app.route('/mark',methods = ['GET', 'POST'])
def mark():
   return render_template('mark2.html')

@app.route('/baidumap', methods = ['GET', 'POST'])

# 功能3路径规划和附近POI查找
def baidumap():
    return render_template('baidu.html')

@app.route('/firstshow', methods = ['GET', 'POST'])

def firstshow():
    return render_template('Firstshow.html')


# flask app






'''
    POST /api/login

    Params:
    =======================================
    Parameter  |   Type   |   Description
    =======================================
    username   |  string  |   
    password   |  string  |   

    Returns:

    200 -> OK
    400 -> Bad Request
    with a JSON object containing
    =======================================
    Property   |   Type   |   Description
    =======================================
    status_code|   int    |

    Possible values of status_code:
    0   successfully logged in
    1   password incorrect
    2   user not registered 
'''
#
@app.route('/tosignup',methods = ['GET', 'POST'])
def tosignup():
    return render_template('signup.html')
@app.route('/tosignin',methods = ['GET', 'POST'])
def tosignin():
    return render_template('signin.html')

@app.route('/api/login', methods=['POST'])
@cross_origin(origins=["*"])
def login():
    print(request.form)
    username = request.form['username']
    password = request.form['password']
    conn = psycopg2.connect(
        'dbname=webgis user={} password={}'.format(USERNAME, PASSWORD))
    cur = conn.cursor()
    try:
        cur.execute('''
                SELECT password, uuid
                from "user".username
                WHERE username = (%s)
        ''', (username, ))
        query = cur.fetchall()
        uuid = query[0][1]
    except psycopg2.OperationalError:
        app.logger.error('Error: psycopg2.errors.UndefinedColumn')
        abort(500)
    if(len(query) == 0):
        cur.close()
        conn.close()
        return {
            "status_code": 2
        }
    if password == query[0][0]:
        uuid = query[0][1]
        resp = jsonify(status_code=0)
        sha1 = hashlib.sha1()
        sha1.update(bytes(username + SALT, encoding='utf-8'))
        resp.set_cookie('ssid', sha1.hexdigest(), MAX_INT)
        cur.execute('''
                INSERT INTO "user".session
                VALUES (%s, %s, %s)
        ''', (uuid, sha1.hexdigest(), int(datetime.datetime.now().timestamp())))  #
        conn.commit()
        cur.close()
        conn.close()
        return resp
    if(len(query) == 0):
        cur.close()
        conn.close()
        return {
            "status_code": 2
        }

    else:
        cur.close()
        conn.close()
        return {
            "status_code": 1
        }



'''
    POST /api/register

    Params:
    =======================================
    Parameter  |   Type   |   Description
    =======================================
    username   |  string  |   
    password   |  string  |   

    Returns:

    200 -> OK
    400 -> Bad Request 
    with a JSON object containing
    =======================================
    Property   |   Type   |   Description
    =======================================
    status_code|   int    |

    Possible values of status_code:
    0   successfully registered
    1   username has existed
    2   username or password is empty
'''


@app.route('/api/register', methods=['POST'])
@cross_origin(origins=["*"])
def register():
    username = request.form['username']
    password = request.form['password']

    conn = psycopg2.connect(
        'dbname=webgis user={} password={}'.format(USERNAME, PASSWORD))
    cur = conn.cursor()
    extras.register_uuid()
    # try:
    cur.execute('''
                SELECT username
                FROM "user".username
                WHERE username = (%s)
        ''', (username, ))
    query = cur.fetchall()
    # except psycopg2.Error:
    #     app.logger.error('Error: psycopg2.Error')
    #     abort(500)

    # if user is existed
    if(len(query) != 0):
        cur.close()
        conn.close()
        return {
            'status_code': 1
        }, 200

    if(len(username) == 0 or username.isspace() or len(password) == 0 or username.isspace()):
        cur.close()
        conn.close()
        return {
            'status_code': 2
        }, 200
    else:
        cur.execute('''
                INSERT INTO "user".username
                VALUES (%s, %s, %s)
            ''', (uuid.uuid1(), username, password))
        conn.commit()
        return {
                'status_code': 0
            }
        # except psycopg2.Error:
        #     app.logger.error('Error: psycopg2.Error')
        #     abort(500)
        # finally:
        #     cur.close()
        #     conn.close()


'''
    POST /api/logout

    Params:
    =======================================
    Parameter  |   Type   |   Description
    =======================================
    username   |  string  |   

    Returns:

    200 -> OK
    400 -> Bad Request 
    with a JSON object containing
    =======================================
    Property   |   Type   |   Description
    =======================================
    status_code|   int    |

    Possible values of status_code:
    0   successfully logged out
    1   no cookies passed
    2   user hasnot logged in 
'''


@app.route('/api/logout')
def logout():
    username = request.args.get('username', '')
    ssid = request.cookies.get('ssid')
    if ssid is None:
        return {
            'status_code': 1
        }

    sha1 = hashlib.sha1()
    sha1.update(bytes(username + SALT, encoding='utf-8'))
    if ssid == sha1.hexdigest():
        resp = jsonify(status_code=0)
        resp.set_cookie('ssid', '', 0)
        with psycopg2.connect('dbname=webgis user={} password={}'.format(USERNAME, PASSWORD)) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                            DROP FROM "user".session
                            WHERE cookie = {}
                ''', (ssid, ))
        return resp
    else:
        return {
            'status_code': 2
        }

@app.route('/api/getUsername')
@cross_origin()
def getUsername():
    cookie = request.cookies.get('ssid')
    with psycopg2.connect('dbname=webgis user={} password={}'.format(USERNAME, PASSWORD)) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        SELECT uuid
                        FROM "user".session
                        WHERE cookie = (%s)
            ''', (cookie, ))
            query = cur.fetchall()
            if(len(query)==0):
                return {
                        'username': None
                }
            else:
                uuid = query[0][0]
            cur.execute('''
                        SELECT uuid
                        FROM "user".username
                        WHERE uuid = (%s)
            ''', (uuid, ))
    return {
            'username': query[0][0]
    }

@app.route('/api/addComment', methods=['POST'])
@cross_origin()
def addComment():
    lng = request.form['poi_lng']
    lat = request.form['poi_lat']
    pl = request.form['poi_pl']
    imgurl = request.form['poi_img']


    # conn = psycopg2.connect(
    #     'dbname=webgis user={} password={}'.format(USERNAME, PASSWORD))
    # cur = conn.cursor()
    # extras.register_uuid()
    # # try:
    # cur.execute('''
    #             SELECT username
    #             FROM "user".username
    #             WHERE username = (%s)
    #     ''', (username, ))
    # query = cur.fetchall()

    cookie = request.cookies.get('ssid')
    with psycopg2.connect('dbname=webgis user={} password={}'.format(USERNAME, PASSWORD)) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        SELECT uuid
                        FROM "user".session
                        WHERE cookie = (%s)
            ''', (cookie, ))
            query = cur.fetchall()
            uuid = query[0][0]
            cur.execute('''
                        INSERT INTO "user".comment
                        VALUES
                        (%s, %s, %s, %s, %s)
            ''', (lng, lat, pl, imgurl, uuid))
            conn.commit()
    return 0

@app.route('/api/getComment',methods=['POST'])
@cross_origin()
def getComment():
    cookie = request.cookies.get('ssid')
    with psycopg2.connect('dbname=webgis user={} password={}'.format(USERNAME, PASSWORD)) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT uuid
                            FROM "user".session
                            WHERE cookie = (%s)
                ''', (cookie,))
            query = cur.fetchall()
            uuid = query[0][0]
            cur.execute('''
                        SELECT *
                        FROM "user".comment
                        WHERE uuid = (%s)
            ''', (uuid, ))
            query = cur.fetchall()
            data = []
            for q in query:
                data.append({
                    "poi_lng": q[0],
                    "poi_lat": q[1],
                    "poi_pl": q[2],
                    "poi_img": q[3]
                })
            return jsonify(data)








if __name__ == '__main__':

    # app.run(debug = True,host="0.0.0.0", port=8090)
    app.run(debug = True)