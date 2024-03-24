# -*- coding:utf-8 -*-
from enum import Enum


class InterfaceEnumClass(object):
    """接口-枚举类"""

    @classmethod
    def value_exists(cls, value) -> bool:
        """
        判断枚举值是否存在
        :param value: 枚举值
        :return:
        """
        raise NotImplementedError()

    @classmethod
    def value_list(cls) -> list:
        """
        获取枚举值列表
        :return: 枚举值列表
        """
        raise NotImplementedError()

    @classmethod
    def value_name(cls, value: int):
        """
        由子类实现的映射: 枚举值 -> 枚举值对应的描述
        :param value: 枚举值
        :return: 枚举值对应的描述
        """
        raise NotImplementedError()

    @classmethod
    def value_name_list(cls) -> list:
        """
        获取所有枚举值名称的列表
        :return:
        """
        raise NotImplementedError()

    @classmethod
    def items(cls):
        """返回 (枚举,名称) 的列表"""
        raise NotImplementedError()


class BaseEnum(InterfaceEnumClass, Enum):
    """基类-枚举类"""

    @classmethod
    def value_exists(cls, value):
        for member in cls.__members__.values():
            if member.value == value:
                return True
        return False

    @classmethod
    def value_list(cls):
        return [member.value for member in cls.__members__.values()]

    @classmethod
    def value_name(cls, value: int):
        raise NotImplementedError()

    @classmethod
    def value_name_list(cls):
        return [cls.value_name(member.value) for member in cls.__members__.values()]

    @classmethod
    def items(cls):
        """返回 (枚举,名称) 的列表"""
        return [
            (member.value, cls.value_name(member.value))
            for member in cls.__members__.values()
        ]
