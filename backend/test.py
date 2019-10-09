import base64
from urllib import parse
import requests

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)


@app.route('/', methods=['POST'])
def hello_world():
    image_data = request.files['file'].read()
    image_string = base64.b64encode(image_data)
    data = parse.urlencode({'image': image_string}).encode('utf-8')
    # response = requests.post(
    #     'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=24.ea04d58ba72c685e8238cf22de200bd2.2592000.1573126398.282335-16049065',
    #     data=data, 
    #     headers={'Content-Type':'application/x-www-form-urlencoded'}
    # )
    # body = response.json()
    # print(body)
    #'搜索结果并返回'
    result = {'tableData': [{
        'name': '活着',
        'author': '余华',
        'address': '人民出版社',
        'tag': '相同出版社',
        'description': 'haha',
        'img': 'http://img3m0.ddimg.cn/87/27/25260630-1_w_3.jpg'
      }, {
        'name': '人生海海',
        'author': '高小明',
        'address': '工业出版社',
        'tag': '相同作者',
        'description': 'baba',
        'img': 'http://img3m5.ddimg.cn/51/34/26921715-1_x_2.jpg'
      }, {
        'name': '全球最美的100个地方',
        'author': '国家地理',
        'address': '北京联合出版公司',
        'tag': '相同书名',
        'description': 'lala',
        'img': 'http://img3m7.ddimg.cn/54/27/22790547-1_x_1.jpg'
      }]}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
