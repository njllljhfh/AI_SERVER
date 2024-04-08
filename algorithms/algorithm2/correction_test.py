import numpy as np


def result_correction(schedule_matrix, data):
    # 对每一行（每个班次）进行检查和修正
    for shift in range(schedule_matrix.shape[0]):
        # 获取当前班次的安排
        current_shift_arrangement = schedule_matrix[shift, :]
        # 找到重复的员工编号
        unique, counts = np.unique(current_shift_arrangement, return_counts=True)
        duplicates = unique[counts > 1]

        for duplicate in duplicates:
            # 找到重复员工编号在当前班次中的岗位索引
            positions = np.where(current_shift_arrangement == duplicate)[0]

            # 为重复的岗位找到替换人选
            for position in positions[1:]:  # 保留第一个岗位的安排，为后续的岗位找替代人选
                # 假设positions_list已按适应度排序，尝试找到一个未被当前班次使用的替代人选
                for candidate, _ in data['skill_list'][position]:
                    if candidate not in current_shift_arrangement:
                        # 找到替代人选，更新排班表，并停止搜索
                        schedule_matrix[shift, position] = candidate
                        break
    return schedule_matrix
