import numpy as np
import json


# 给定的矩阵和S_day向量
def output_data(data, matrix, to_json=True):
    S = data['S']  # 每个岗位每天的班次数，使用NumPy数组以便进行矩阵运算
    D = data['D']  # 天数
    max_S = np.max(S)  # 每天最大班次数

    # 计算每个岗位需要在哪些班次设置为-1
    adjust = max_S - S

    # 生成一个用于标记需要设置为-1的位置的掩码矩阵
    mask = np.zeros_like(matrix, dtype=bool)

    for i, a in enumerate(adjust):
        if a > 0:
            for d in range(D):
                mask[d * max_S + S[i]:d * max_S + max_S, i] = True

    # 使用掩码矩阵设置对应位置为-1
    matrix[mask] = -1

    K = data['K']
    person_ids = data['person_ids']
    position_ids = data['position_ids']

    # 构建JSON结构
    result = []
    for d in range(D):
        day_data = {
            "day": f"第{d + 1}天",
            "times": []
        }
        for s in range(max_S):
            time_data = {
                "time": f"第{s + 1}更",
                "classes": []
            }
            for k in range(K):
                class_data = {
                    "岗位名称": position_ids[k],
                    "people": []
                }
                person_index = matrix[d * max_S + s][k]
                if person_index != -1:  # -1表示没有人分配
                    class_data["people"].append({
                        "number": person_index + 1,  # 输出的编号从1开始
                        "name": person_ids[person_index]  # 直接使用索引从person_ids中获取人员名称
                    })
                time_data["classes"].append(class_data)
            day_data["times"].append(time_data)
        result.append(day_data)
    final_result = {
        "code": 1,
        "msg": "成功",
        "data": result  # 将之前构建的result列表作为data条目的值
    }

    if to_json:
        # 将整个结构转换为JSON字符串
        json_data = json.dumps(final_result, indent=4, ensure_ascii=False)
        # print(json_data)
        return json_data
    else:
        return final_result
