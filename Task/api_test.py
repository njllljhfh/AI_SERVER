# -*- coding:utf-8 -*-
import json
import os
import random

import requests
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# print(sys.path)

from utils.enumerationClass.common_enum import Option, OptMethod, PersonChoice

IP = '127.0.0.1'
PORT = '8888'


# def api_algorithm1(option=None):
#     url = f'http://{IP}:{PORT}/api/task/algorithm1'
#     print(f"测试url: {url}")
#
#     with open('../test_data/algo1/persons.json', 'r', encoding='utf-8') as f:
#         persons_data = json.loads(f.read())
#     with open('../test_data/algo1/positions.json', 'r', encoding='utf-8') as f:
#         positions_data = json.loads(f.read())
#
#     if option == Option.person_rec.value:
#         params = {
#             'option': option,
#             'task': '任务1',
#             'positions': [
#                 positions_data['position_id_0'],
#             ],
#             'persons': [
#                 persons_data['person_id_0'],
#                 persons_data['person_id_1'],
#             ],
#         }
#     elif option == Option.position_rec.value:
#         params = {
#             'option': option,
#             'task': '任务1',
#             'positions': [
#                 positions_data['position_id_0'],
#                 positions_data['position_id_1'],
#             ],
#             'persons': [
#                 persons_data['person_id_0'],
#             ],
#         }
#     else:
#         params = {
#             'option': option,
#             'task': '任务1',
#             'positions': random.sample(list(positions_data.values()), 2),
#             'persons': random.sample(list(persons_data.values()), 2),
#         }
#
#     # 如果发送的是 JSON 数据，使用 json 参数；如果是表单数据，使用 data 参数
#     response = requests.post(url, json=params, timeout=300)
#
#     if response.status_code == 200:
#         print(f'api_algorithm1 http请求成功！')
#     else:
#         print(f'api_algorithm1 http请求成功！ 响应码：{response.status_code}')
#
#     # 解析 JSON 响应（如果返回的是 JSON 数据）
#     json_response = response.json()
#     print(f'api_algorithm1-后端返回数据：{json_response}')
#     print('- ' * 30)


def api_algorithm1(option=None):
    url = f'http://{IP}:{PORT}/api/task/algorithm1'
    print(f"测试url: {url}")

    if option == Option.person_rec.value:
        person_info_path = '../test_data/algo1/all_data/persons.json'
        position_info_path = '../test_data/algo1/position_data/position_35.json'

    elif option == Option.position_rec.value:
        person_info_path = '../test_data/algo1/person_data/person_13.json'
        position_info_path = '../test_data/algo1/all_data/positions.json'
    else:
        person_info_path = '../test_data/algo1/all_data/persons.json'
        position_info_path = '../test_data/algo1/position_data/position.json'

    with open(person_info_path, 'r', encoding='utf-8') as f:
        persons_data = json.loads(f.read())
    with open(position_info_path, 'r', encoding='utf-8') as f:
        positions_data = json.loads(f.read())

    params = {
        'option': option,
        'task': '任务1',
        'positions': persons_data,
        'persons': positions_data,
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


def api_algorithm2(opt_method=None):
    url = f'http://{IP}:{PORT}/api/task/algorithm2'
    print(f"测试url: {url}")

    with open('../test_data/algo1/r3.json', 'r', encoding='utf-8') as f:
        task = json.loads(f.read())

    params = {
        'task': task,
        'opt_method': opt_method,
        'base_data': None,
        'schedule_days': 25,
        'max_days': 5,
        'max_shifts': 30,
        'shift_nums': [],
    }

    if opt_method == OptMethod.assistant_decision.value:
        with open('../test_data/algo2/输出结果排班表&辅助决策输入人工排班表.json', 'r', encoding='utf-8') as f:
            # 中船的决策数据（格式为算法二输出的json格式）
            algo2_res = json.loads(f.read())
        params['base_data'] = algo2_res['data']

    # 如果发送的是 JSON 数据，使用 json 参数；如果是表单数据，使用 data 参数
    response = requests.post(url, json=params, timeout=300)

    if response.status_code == 200:
        print(f'api_algorithm2 http请求成功！')
    else:
        print(f'api_algorithm2 http请求成功！ 响应码：{response.status_code}')

    # 解析 JSON 响应（如果返回的是 JSON 数据）
    json_response = response.json()
    print(f'api_algorithm2-后端返回数据：{json_response}')
    print('- ' * 30)


def api_algorithm3(person_choice=None):
    url = f'http://{IP}:{PORT}/api/task/algorithm3'
    print(f"测试url: {url}")

    task = {'task': '算法提供测试数据'}  # 算法提供测试数据
    persons = {'persons': '算法提供测试数据'}  # 算法提供测试数据

    with open('../test_data/algo2/输出结果排班表&辅助决策输入人工排班表.json', 'r', encoding='utf-8') as f:
        algo2_res = json.loads(f.read())
        scheduling = algo2_res['data']

    with open('../test_data/algo1/r3.json', 'r', encoding='utf-8') as f:
        persons_value = json.loads(f.read())

    params = {
        'task': task,
        'persons': persons,
        'scheduling': scheduling,
        'task_time': "13:00-14:00",
        'persons_value': persons_value,
        'person_choice': person_choice,
        'manual_choice': None,
    }

    if person_choice == PersonChoice.need.value:
        manual_choice = {'manual_choice': "算法提供测试数据"}  # 算法提供测试数据
        params['manual_choice'] = manual_choice

    # 如果发送的是 JSON 数据，使用 json 参数；如果是表单数据，使用 data 参数
    response = requests.post(url, json=params, timeout=300)

    if response.status_code == 200:
        print(f'api_algorithm3 http请求成功！')
    else:
        print(f'api_algorithm3 http请求成功！ 响应码：{response.status_code}')

    # 解析 JSON 响应（如果返回的是 JSON 数据）
    json_response = response.json()
    print(f'api_algorithm3-后端返回数据：{json_response}')
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
    # -------------------------------------------------------

    # # opt_method = OptMethod.assistant_decision.value  # 辅助决策
    # opt_method = OptMethod.global_opt.value  # 全局优化
    # api_algorithm2(opt_method=opt_method)
    # # -------------------------------------------------------
    #
    # person_choice = PersonChoice.no_need.value  # 人员不需要逐个确认
    # # person_choice = PersonChoice.need.value  # 人员需要逐个确认
    # api_algorithm3(person_choice=person_choice)
