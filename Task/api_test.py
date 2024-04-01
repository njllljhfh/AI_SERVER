# -*- coding:utf-8 -*-
import json
import os
import random

import requests
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# print(sys.path)

from utils.enumerationClass.common_enum import Option

IP = '127.0.0.1'
PORT = '8888'


def api_algorithm1(option=None):
    url = f'http://{IP}:{PORT}/api/task/algorithm1'
    print(f"测试url: {url}")

    # 测试数据
    # params = {
    #     'a': 1,
    #     'b': 2,
    # }

    with open('../test_data/algo1/persons.json', 'r', encoding='utf-8') as f:
        persons_data = json.loads(f.read())
    with open('../test_data/algo1/positions.json', 'r', encoding='utf-8') as f:
        positions_data = json.loads(f.read())

    if option == Option.person_rec.value:
        params = {
            'option': option,
            'task': '任务1',
            'positions': [
                positions_data['position_id_0'],
            ],
            'persons': [
                persons_data['person_id_0'],
                persons_data['person_id_1'],
            ],
        }
    elif option == Option.position_rec.value:
        params = {
            'option': option,
            'task': '任务1',
            'positions': [
                positions_data['position_id_0'],
                positions_data['position_id_1'],
            ],
            'persons': [
                persons_data['person_id_0'],
            ],
        }
    else:
        params = {
            'option': option,
            'task': '任务1',
            'positions': random.sample(list(positions_data.values()), 2),
            'persons': random.sample(list(persons_data.values()), 2),
        }

    # 如果发送的是 JSON 数据，使用 json 参数；如果是表单数据，使用 data 参数
    response = requests.post(url, json=params, timeout=300)

    if response.status_code == 200:
        print(f'api_algorithm1 http请求成功！')
    else:
        print(f'api_algorithm1 http请求成功！ 响应码：{response.status_code}')

    # 解析 JSON 响应（如果返回的是 JSON 数据）
    json_response = response.json()
    print(f'api_algorithm1-后端返回数据：{json_response}')
    print('- ' * 30)


def api_myTest():
    # 定义接口的URL
    url = f'http://{IP}:{PORT}/api/task/myTest'
    print(f'测试url: {url}')

    # 定义GET请求参数（如果需要的话）
    params = {
        'a': 1,
        'b': 0.1,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        print(f'api_myTest http请求成功！')
    else:
        print(f'api_myTest http请求成功！ 响应码：{response.status_code}')

    # 解析JSON响应（如果返回的是JSON数据）
    json_response = response.json()
    print(f'api_myTest-后端返回数据：{json_response}')
    print('- ' * 30)


if __name__ == '__main__':
    # get 测试接口
    # api_myTest()

    # post 算法1测试接口
    option = Option.person_rec.value  # 1 船员推荐
    # option = Option.position_rec.value  # 2 战位推荐
    # option = Option.match_matrix.value  # 3 匹配矩阵
    api_algorithm1(option=option)
