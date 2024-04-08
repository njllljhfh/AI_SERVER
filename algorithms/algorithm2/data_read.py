import numpy as np

def json_to_matrix(task):
    # 假设 task_data 是从 JSON 文件中提取的 task 部分
    task_data = task["data"]
    header = task_data["header"]
    positions = task_data["position"]

    # 初始化匹配矩阵和邻接表
    fitness_matrix = np.zeros((len(header), len(positions)))
    adjacency_list = []
    person_index = {person_id: index for index, person_id in enumerate(header)}

    person_ids = header  # 因为header已经按顺序列出了所有人员ID
    position_ids = [position["position_id"] for position in positions]
    # 同时填充匹配矩阵和构建邻接表
    for col_index, position in enumerate(positions):
        # 对于列表形式的邻接表，每个岗位开始时先添加一个空列表
        current_position_list = []
        for person_id, fitness in position.items():
            if person_id == "position_id":
                continue  # 跳过position_id项
            row_index = person_index[person_id]
            fitness_matrix[row_index, col_index] = fitness
            # 如果匹配度不为0，则将(索引, 适应度)添加到当前岗位的列表中
            if fitness != 0:
                current_position_list.append((row_index, fitness))
        # 将当前岗位的列表添加到列表形式的邻接表中
        adjacency_list.append(current_position_list)
    # 此时，fitness_matrix 是人员和岗位的适应度矩阵，adjacency_list 是邻接表
    return fitness_matrix, adjacency_list, person_ids, position_ids

def read_data(task, opt_method, base_data, D, S, max_cd, max_shift):
    fitness_matrix, adjacency_list, person_ids, position_ids = json_to_matrix(task)
    data = {
        'type': opt_method,
        'N': len(person_ids),
        'K': len(position_ids),
        'D': D,
        'S': S,
        'skill_matrix': fitness_matrix,
        'skill_list': adjacency_list,
        'max_cd': max_cd,
        'max_shift': max_shift,
        'test_schedule': np.array(base_data),
        'person_ids': person_ids,
        'position_ids': position_ids
    }
    return data
