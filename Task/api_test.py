# -*- coding:utf-8 -*-
import requests

IP = '127.0.0.1'
PORT = '8888'


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
        print(f'api_myTest 请求成功！')
    else:
        print(f'api_myTest 请求失败！ 响应码：{response.status_code}')

    # 解析JSON响应（如果返回的是JSON数据）
    json_response = response.json()
    print(f'api_myTest-后端返回数据：{json_response}')
    print('- ' * 30)


def api_algorithm1():
    url = f'http://{IP}:{PORT}/api/task/algorithm1'
    print(f"测试url: {url}")

    data = {
        'a': 1,
        'b': 2,
    }

    # 如果发送的是 JSON 数据，使用 json 参数；如果是表单数据，使用 data 参数
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print(f'api_algorithm1 请求成功！')
    else:
        print(f'api_algorithm1 请求失败！ 响应码：{response.status_code}')

    # 解析 JSON 响应（如果返回的是 JSON 数据）
    json_response = response.json()
    print(f'api_algorithm1-后端返回数据：{json_response}')
    print('- ' * 30)


if __name__ == '__main__':
    # get 测试接口
    api_myTest()

    # post 算法1测试接口
    api_algorithm1()
