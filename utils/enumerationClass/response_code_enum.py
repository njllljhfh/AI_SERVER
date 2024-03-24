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
    SUCCESS = 0
    UNKNOWN_ERROR = 1
    PARAMETER_ERROR = 2

    # 算法

    @classmethod
    def value_name(cls, value):
        value_map = {
            # 通用
            cls.SUCCESS.value: "成功",
            cls.UNKNOWN_ERROR.value: "未知错误",
            cls.PARAMETER_ERROR.value: "请求参数错误",
        }
        return value_map.get(value)
