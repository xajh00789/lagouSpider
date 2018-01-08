#coding:utf8
import requests
from urllib.parse import urlencode
import json
import pymongo
from multiprocessing import Pool

#从MongoDB导出csv表格
#mongoexport -d job  -c Python实习 -f city,company,companySize,positionName,salary,workYear,companyLabelList,district,createTime,education,url,longitude,latitude    --csv -o ./拉钩网python实习.csv

MONGO_TABLE = 'Python实习'
client=pymongo.MongoClient('localhost')
db=client['job']


query='python实习'

headers={
    'Host': 'www.lagou.com',
    'Connection': 'keep-alive',
    'Content-Length': '74',
    'Origin': 'https://www.lagou.com',
    'Referer':'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%AE%9E%E4%B9%A0?oquery=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&fromSearch=true&labelWords=relative',
    'X-Anit-Forge-Code': '0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Anit-Forge-Token': 'None',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'user_trace_token=20171209190124-f18000ec-da34-4751-a24e-ae53e9e3f33b; LGUID=20171209190126-4d6bb41e-dcd0-11e7-8bfe-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAAAFCAAEGC5D2C44EB8B28F6A60BFAB1F84A37A3E; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; SEARCH_ID=a0f360aff5884f529be264d48cb23dbf; TG-TRACK-CODE=search_code; _gid=GA1.2.1718525176.1512817289; _ga=GA1.2.209780080.1512817288; LGSID=20171210095515-2a95cddd-dd4d-11e7-8d30-525400f775ce; LGRID=20171210100602-ac3435f5-dd4e-11e7-9cae-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512817289,1512817360,1512870918; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512871562'
}

'''
headers2={
    'Host': 'a.lagou.com',
    'Connection': 'keep-alive',
    'Content-Length': '74',
    'referer':'https://www.lagou.com/jobs/3828899.html',
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Anit-Forge-Token': 'None',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'user_trace_token=20171209190124-f18000ec-da34-4751-a24e-ae53e9e3f33b; LGUID=20171209190126-4d6bb41e-dcd0-11e7-8bfe-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAAAFCAAEGC5D2C44EB8B28F6A60BFAB1F84A37A3E; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; SEARCH_ID=a0f360aff5884f529be264d48cb23dbf; TG-TRACK-CODE=search_code; _gid=GA1.2.1718525176.1512817289; _ga=GA1.2.209780080.1512817288; LGSID=20171210095515-2a95cddd-dd4d-11e7-8d30-525400f775ce; LGRID=20171210100602-ac3435f5-dd4e-11e7-9cae-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512817289,1512817360,1512870918; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512871562'
}
'''

#根据post请求获取页面返回结果
def get_main_page(query,page):
#    global query
    url='https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
    data={
        'first': 'false',
        'pn': page,
        'kd': query
    }
    response=requests.post(url,data=data,headers=headers)
  #  print(response.text)
    return response.text

#通过json格式导入页面请求返回含有工作信息的数据，筛选出有用数据部分
def parse_main_page(content):
    try:
        items=json.loads(content)
        if items and 'content' in items.keys():
            results=items.get('content').get('positionResult').get('result')
            for result in results:
                print(result)
#json格式筛选出的内容是以字典格式显示
#{'isSchoolJob': 0, 'stationname': '太阳宫', 'secondType': '后端开发', 'longitude': '116.448914', 'city': '北京', 'district': '朝阳区', 'latitude': '39.96391', 'positionId': 3740864, 'companyShortName': '光量科技', 'workYear': '3-5年', 'formatCreateTime': '2017-12-12', 'firstType': '开发/测试/运维类', 'imState': 'today', 'adWord': 0, 'industryField': '移动互联网,金融', 'gradeDescription': None, 'jobNature': '全职', 'explain': None, 'companySize': '15-50人', 'positionLables': ['金融', '支付', '高级', '后端开发'], 'subwayline': '10号线', 'lastLogin': 1515403989000, 'promotionScoreExplain': None, 'pcShow': 0, 'companyId': 68596, 'education': '本科', 'businessZones': ['西坝河', '三元桥', '国展', '三元桥', '国展'], 'companyLogo': 'i/image/M00/49/45/CgqKkVeW4RWAUfnqAACQTfdfPsI789.jpg', 'companyFullName': '北京鼓掌移动科技有限公司', 'publisherId': 5228687, 'positionAdvantage': '行业先锋,快速发展,优秀团队,灵活开放', 'plus': None, 'appShow': 0, 'linestaion': '10号线_太阳宫;10号线_三元桥;13号线_柳芳;机场线_三元桥', 'deliver': 0, 'createTime': '2017-12-12 14:26:31', 'score': 0, 'companyLabelList': ['股票期权', '扁平管理', '管理规范', '五险一金'], 'positionName': 'Python/Go工程师', 'salary': '18k-35k', 'industryLables': ['金融', '支付', '高级', '后端开发'], 'approve': 1, 'financeStage': 'A轮'}
                yield result
    except ValueError:
        pass


#获取返回数据字典相关键对应的值赋值给变量
def get_detail_inform(item):
    city=item['city']
    district=item['district']
    company=item['companyFullName']
    companyLabelList=item['companyLabelList']
    companySize=item['companySize']
    createTime=item['createTime'][0:10]
    education=item['education']
    positionName=item['positionName']
    workYear=item['workYear']
    salary=item['salary']
    latitude=item['latitude']
    longitude=item['longitude']
    urlId=item['positionId']
    url='https://www.lagou.com/jobs/'+str(urlId)+'.html' #工作页面链接
    print(city,district,company,companyLabelList,companySize,createTime,education,positionName,workYear,salary,latitude,longitude,urlId)
    return({'city':city,'district':district,'company':company,'companyLabelList':companyLabelList,'companySize':companySize,'createTime':createTime,\
            'education':education,'positionName':positionName,'workYear':workYear,'salary':salary,'latitude':latitude,'longitude':longitude,\
            'url':url})

#company，positionName，workYear，city，district，createTime，education，companySize，salary，latitude，longitude，url，companyLabelList


#将数据内容存储到mongo数据库
def save_to_mongo(data):
    if db[MONGO_TABLE].insert(data):
        print('Successfully save to mongo')
        return True
    else:
        return False




def main(page):
    content = get_main_page(query,page)
    for item in parse_main_page(content):
        information=get_detail_inform(item)
        save_to_mongo(information)


if __name__=='__main__':
    p=Pool(3)
    p.map(main,range(1,31))