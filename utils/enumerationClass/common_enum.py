# -*- coding:utf-8 -*-
from enum import unique

from utils.enumerationClass.base_enum import BaseEnum


@unique
class Option(BaseEnum):
    person_rec = 1
    position_rec = 2
    match_matrix = 3

    @classmethod
    def value_name(cls, value):
        return option_value_map.get(value)


option_value_map = {
    Option.person_rec.value: "船员推荐",
    Option.position_rec.value: "战位推荐",
    Option.match_matrix.value: "匹配矩阵",
}


@unique
class OptMethod(BaseEnum):
    assistant_decision = 1
    global_opt = 2

    @classmethod
    def value_name(cls, value):
        return opt_method_value_map.get(value)


opt_method_value_map = {
    OptMethod.assistant_decision.value: "辅助决策",
    OptMethod.global_opt.value: "全局优化",
}


@unique
class PersonChoice(BaseEnum):
    no_need = 0
    need = 1

    @classmethod
    def value_name(cls, value):
        return person_choice_value_map.get(value)


person_choice_value_map = {
    PersonChoice.no_need.value: "人员不需要进行选择",
    PersonChoice.need.value: "人员需要进行选择",
}
