import base64
from urllib import parse
import requests

from flask import Flask, request, jsonify
from flask_cors import CORS

import pymongo
from bson import ObjectId
import hashlib
import json
import itertools

author_dict = {}
publisher_dict = {}
title_hash_dict = {}


def get_title_hash(title):
    temp = hashlib.md5()
    temp.update(title.encode('utf-8'))
    return str(int('0x' + temp.hexdigest(), 16) % 100000)


def get_data():
    global author_dict, publisher_dict, title_hash_dict
    with open('author.txt') as f:
        line = f.readline()
        author_dict = json.loads(line)
    with open('publisher.txt') as f:
        line = f.readline()
        publisher_dict = json.loads(line)
    with open('title.txt') as f:
        line = f.readline()
        title_hash_dict = json.loads(line)


def search(title, author, publisher):
    global author_dict, publisher_dict, title_hash_dict

    my_client = pymongo.MongoClient('mongodb://localhost:27017/')
    my_db = my_client['book_data']
    my_table = my_db['book']

    if len(author_dict) == 0 or len(publisher_dict) == 0 or len(title_hash_dict) == 0:
        get_data()

    # 这本书的书名的hash值
    title_hash = get_title_hash(title)
    # 该作者的所有作品的id的list
    if author in author_dict:
        author_list = author_dict[author]
    else:
        author_list = []
    # 该出版社的所有作品的id的list
    if publisher in publisher_dict:
        publisher_list = publisher_dict[publisher]
    else:
        publisher_list = []
    # 该书名hash值的所有作品的id的list（这些书只是书名的hash值相同，书名不一定相同）
    if title_hash in title_hash_dict:
        title_hash_list = title_hash_dict[title_hash]
    else:
        title_hash_list = []
    # 上面三个list的交集，即最终结果集的id
    result_id_list = list(set(author_list).intersection(set(publisher_list)).intersection(set(title_hash_list)))
    # 结果集合
    result_accurate = []
    # 根据最终结果集id，验证书名，得到最终结果集
    if len(result_id_list) > 100:
        result_id_list = result_id_list[0:100]
    for result_id in result_id_list:
        temp = my_table.find_one({'_id': ObjectId(result_id)})
        if temp['title'] == title:
            result_accurate.append(temp)

    # 以下3个集合彼此可以重复，但结果集合的书不会在以下三个集合出现
    # 相当于是"同xx的[其他]作品"
    # 同作者的集合
    result_same_author = []
    # 同出版社的集合
    result_same_publisher = []
    # 同书名的集合
    result_same_title = []
    # 把最终结果集的id从待遍历列表里删掉。
    author_list = list(set(author_list).difference(set(result_id_list)))
    if len(author_list) > 100:
        author_list = author_list[0:100]
    publisher_list = list(set(publisher_list).difference(set(result_id_list)))
    if len(publisher_list) > 100:
        publisher_list = publisher_list[0:100]
    title_hash_list = list(set(title_hash_list).difference(set(result_id_list)))
    if len(title_hash_list) > 100:
        title_hash_list = title_hash_list[0:100]

    for same_author_id in author_list:
        temp = my_table.find_one({'_id': ObjectId(same_author_id)}, {'_id': 0, 'title_hash': 0})
        result_same_author.append(temp)

    for same_publisher_id in publisher_list:
        temp = my_table.find_one({'_id': ObjectId(same_publisher_id)}, {'_id': 0, 'title_hash': 0})
        result_same_publisher.append(temp)

    for same_title_hash_id in title_hash_list:
        temp = my_table.find_one({'_id': ObjectId(same_title_hash_id)}, {'_id': 0, 'title_hash': 0})
        if temp['title'] == title:
            result_same_title.append(temp)

    return {
        'length': len(result_accurate) + len(result_same_title) + len(result_same_author) + len(result_same_publisher),
        'data': [result_accurate, result_same_title, result_same_author, result_same_publisher]}


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)


@app.route('/', methods=['POST'])
def hello_world():
    image_data = request.files['file'].read()
    image_string = base64.b64encode(image_data)
    data = parse.urlencode({'image': image_string}).encode('utf-8')
    response = requests.post(
        'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=24.ea04d58ba72c685e8238cf22de200bd2.2592000.1573126398.282335-16049065',
        data=data,
        headers={'Content-Type':'application/x-www-form-urlencoded'}
    )
    body = response.json()
    # print(body)
    # temp = {
    #     'log_id': 6634321049862195363,
    #     'words_result_num': 5,
    #     'words_result': [
    #         {'words': '〔英〕莫欣·哈米德著咏梅译'},
    #         {'words': '末日迁徙'},
    #         {'words': ' Exit West'},
    #         {'words': '南海出公司'},
    #         {'words': '■■■■'}]
    # }
    words = []
    for word in body['words_result']:
        if word['words'][-1] == "著":
            words.append(word['words'][:-1].strip())
        else:
            words.append(word['words'].strip())
    print(words)
    while len(words) < 3:
        words.append("")
    # 构建所有可能的排列组合
    permutations = itertools.permutations(words, 3)
    max_length = -1
    # 搜索结果并返回
    for item in permutations:
        print(item)
        result_once = search(item[0], item[1], item[2])
        if result_once['length'] > max_length:
            max_length = result_once['length']
            result = {'data': result_once['data']}
    # result = {'data': [
    #     [{
    #         'title': '人间失格',
    #         'author': '太宰治',
    #         'publisher': '作家出版社',
    #         'source': '京东网',
    #         'coverUrl': 'http://img3m0.ddimg.cn/87/27/25260630-1_w_3.jpg'
    #     }],
    #     [{
    #         'title': '人间失格',
    #         'author': '[日] 太宰治',
    #         'publisher': '人民出版社',
    #         'source': '当当网',
    #         'coverUrl': 'http://img3m0.ddimg.cn/87/27/25260630-1_w_3.jpg'
    #     }, {
    #         'title': '人间失格',
    #         'author': '太宰治',
    #         'publisher': '商务印书馆',
    #         'source': '豆瓣网',
    #         'coverUrl': 'http://img3m5.ddimg.cn/51/34/26921715-1_x_2.jpg'
    #     }],
    #     [{
    #         'title': '太宰治的另一个作品',
    #         'author': '太宰治',
    #         'publisher': '人民出版社',
    #         'source': '京东网',
    #         'coverUrl': 'http://img3m0.ddimg.cn/87/27/25260630-1_w_3.jpg'
    #     }, {
    #         'title': '太宰治的又一个作品',
    #         'author': '太宰治',
    #         'publisher': '作家出版社',
    #         'source': '豆瓣网',
    #         'coverUrl': 'http://img3m7.ddimg.cn/54/27/22790547-1_x_1.jpg'
    #     }],
    #     [{
    #         'title': '作家出版社的作品一',
    #         'author': '李白',
    #         'publisher': '作家出版社',
    #         'source': '京东网',
    #         'coverUrl': 'http://img3m0.ddimg.cn/87/27/25260630-1_w_3.jpg'
    #     }, {
    #         'title': '作家出版社的作品二',
    #         'author': '杜甫',
    #         'publisher': '作家出版社',
    #         'source': '京东网',
    #         'coverUrl': 'http://img3m0.ddimg.cn/87/27/25260630-1_w_3.jpg'
    #     }]
    # ]}
    # result = {'tableData': [{
    #     'name': '活着',
    #     'author': '余华',
    #     'address': '人民出版社',
    #     'tag': '相同出版社',
    #     'description': 'haha',
    #     'img': 'http://img3m0.ddimg.cn/87/27/25260630-1_w_3.jpg'
    #   }, {
    #     'name': '人生海海',
    #     'author': '高小明',
    #     'address': '工业出版社',
    #     'tag': '相同作者',
    #     'description': 'baba',
    #     'img': 'http://img3m5.ddimg.cn/51/34/26921715-1_x_2.jpg'
    #   }, {
    #     'name': '全球最美的100个地方',
    #     'author': '国家地理',
    #     'address': '北京联合出版公司',
    #     'tag': '相同书名',
    #     'description': 'lala',
    #     'img': 'http://img3m7.ddimg.cn/54/27/22790547-1_x_1.jpg'
    #   }]}
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
