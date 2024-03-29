# -*- coding:utf-8 -*-
from enum import unique

from utils.enumerationClass.base_enum import BaseEnum


def jsonify(code, msg=None, data=None):
    """
    生成响应报文
    :param code: 响应码
    :param msg: 响应信息
    :param data: 返回给前端的数据
    :return:
    """
    res = {"code": code}

    if msg is not None:
        res["msg"] = msg
    else:
        res["msg"] = f"{ResponseCode.value_name(code)}"

    if data is not None:
        res["data"] = data

    return res


@unique
class ResponseCode(BaseEnum):
    # 通用
    SUCCESS = 1
    UNKNOWN_ERROR = 2
    PARAMETER_ERROR = 3

    # 算法
    ALGORITHM_ERROR = 1000

    @classmethod
    def value_name(cls, value):
        return response_code_value_map.get(value)


response_code_value_map = {
    # 通用
    ResponseCode.SUCCESS.value: "成功",
    ResponseCode.UNKNOWN_ERROR.value: "未知错误",
    ResponseCode.PARAMETER_ERROR.value: "请求参数错误",
    # 算法
    ResponseCode.ALGORITHM_ERROR.value: "算法错误",
}
