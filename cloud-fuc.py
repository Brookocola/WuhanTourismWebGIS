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


def getcomments(poiID,Name):
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
		total_page = int(int(html['result']['totalCount']) / 9)
		if total_page > 111:
			total_page = 111
		# 2000条太多，运行太慢，爬1000不够再加
		# 遍历查询评论
		print("总页数:", total_page, "爬取中")

		# 创建写入txt文件
		path = str(id[1]) + 'comments.txt'
		xuhao = 0
		with open(path, 'w', newline='', encoding='utf-8') as f:
			file = csv.writer(f)
			file.writerow(['序号', '景区ID', '景区名称', '评论'])
			for page in range(1, total_page -1):
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
        ['武汉','吃', '挺', '错', '味', '送', '太', '的', '了', '我', '还', '都', '就', '是', '啊', '但是', '湖北', '自己', '博物馆', '没有', '很多', '可以',
         '这个', '虽然', '因为', '这样', '已经', '闭馆', '一些', '比如', '不是', '当然', '可能', '如果', '就是', '同时', '比如', '这些', '武', '学武',
         'ct', '学', '学号'])

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

    # 显示图像
    plt.imshow(wc,interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def wordcloud2(fData,fImg,fRes):
	d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
	t = open(path.join(d, fData), encoding='utf-8').read()
	s=t.split(',')



	text={s[0]:0.5,s[1]:0.4,s[2]:0.3,s[3]:0.2,s[4]:0.1}

	print(text)




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
	wc.to_file(fResult)

	# 显示图像
	plt.imshow(wc, interpolation='bilinear')
	plt.axis('off')
	plt.tight_layout()
	plt.show()

# poiID = '77593'
# Name = '黄鹤楼'
# poiID = '10558912'
# Name = '武汉大学'
poiID = '77591'
Name = '湖北省博物馆'

# #爬去评论
# getcomments(poiID,Name)

fData=Name+"comments.txt"
# fData="test.txt"
fImg="湖北省博物馆mask.jpg"
fResult="湖北省博物馆nor.jpg"

myWordCloud(fData,fImg,fResult)
#wordcloud2(fData,fImg,fResult)


