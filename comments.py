import requests
import json
import csv


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

		# 创建写入txt文件
		# path = str(id[1]) + 'comments.txt'
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

poiID = '77593'
Name = '黄鹤楼'
tpath = "C:/Users/86157/Desktop/compnent1/result/" + Name + 'comments.txt'
getcomments(poiID,Name,tpath)



