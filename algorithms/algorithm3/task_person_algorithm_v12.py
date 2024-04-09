import json
import os  # 导入os模块
import random
import time

def read_json_file(filename):
    """通用函数从JSON文件读取数据"""
    if filename is None:
        raise TypeError("Filename cannot be None")
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def prepare_people_data(data):
    people_info = {}
    for people in data["person"]:
        people_info[people["number"]] = {
            "name": people["name"],
            "frequency": people.get("frequency", 0),
        }
        #print(f"- 编号: {people['number']}, 名字: {people['name']},派遣次数: {people['frequency']}")
    print("舰艇总人数:", len(people_info))
    return people_info

def prepare_matching_matrix_data(data):
    # 检查数据中是否存在"data"键
    if "data" in data:
        data = data["data"]  # 获取"data"键对应的值
    else:
        raise ValueError("Invalid JSON format: missing 'data' key")

    # 检查数据中是否存在"position"键
    if "position" in data:
        position_data = data["position"]  # 获取"position"键对应的值
    else:
        raise ValueError("Invalid JSON format: missing 'position' key")

    matching_matrix_info = {}

    # 遍历岗位数据
    for position in position_data:
        position_name = position["岗位名称"]  # 获取岗位名称
        matching_info = {}

        # 遍历岗位对应的匹配信息
        for key, value in position.items():
            # 忽略岗位名称键
            if key != "岗位名称":
                matching_info[key] = value

        matching_matrix_info[position_name] = matching_info
    # 输出读取和处理后的数据
    #print(matching_matrix_info)
    return  matching_matrix_info


def prepare_bushu_data(data):
    task_info = {}
    for position in data["岗位"]:
        task_info[position["岗位名称"]] = {
            "number": position["number"],
            "priority": position["优先级"]
        }
    print("任务需人数:", sum([position["number"] for position in data["岗位"]]))
    return task_info

def prepare_scheduling_data(data):
    scheduling_info = {}
    for scheduling in data["date"]:
        day = scheduling["day"]
        scheduling_info[day] = {}
        for time_data in scheduling["times"]:
            start_time, end_time = time_data["time"][0]
            time_range = f"{start_time.strip()} - {end_time.strip()}"
            scheduling_info[day][time_range] = {class_info["岗位名称"]: class_info["people"] for class_info in time_data["classes"]}
    return scheduling_info


def remove_queried_people(scheduling_info, day, target_time_range):
    available_friends = []
    # 确保指定的天存在于时间表中
    if day in scheduling_info:
        day_schedule = scheduling_info[day]
    else:
        print(f"没有找到指定的天：{day}")
        return []

        # 解析目标时间段
    target_start, target_end = target_time_range.split('-')
    target_start = target_start.strip()
    target_end = target_end.strip()
    #print(target_start, target_end)
        # 遍历指定天的所有时间段和岗位
    for time_range, positions in day_schedule.items():
        #检查时间段是否与目标时间段有交集
        range_start, range_end = time_range.split(' - ')
        range_start = range_start.strip()
        range_end = range_end.strip()
            # 检查时间段交集的逻辑
        if not (range_end <= target_start or range_start >= target_end):
                # 遍历岗位中的人员
            #print(range_start, range_end)
            for position, people in positions.items():
                for person in people:
                    #print(person)
                        # 添加符合条件的朋友的名字
                    available_friends.extend([person['number']])  # 确保这是向列表添加元素

    return available_friends  # 返回列表

# 示例使用
# 注意：您需要确保传入的scheduling_info、task_day和task_time_range与您的数据结构一致。


def update_remaining_people(queried_people, people_info):
    remaining_people_info = people_info.copy()
    for number in queried_people:
        remaining_people_info.pop(number, None)
    return remaining_people_info



def save_assignment_people_to_json(result,assignment_people_info, output_filename):
    """将剩余人员信息保存到JSON文件中"""
    # 合并两个字典
    merged_data = {}
    merged_data.update(result)
    merged_data.update(assignment_people_info)

    with open(output_filename, 'w', encoding='utf-8') as f:
        # 使用json.dump将数据写入文件，确保使用utf-8编码
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

    # 获取完整的文件路径
    full_path = os.path.abspath(output_filename)
    print(f"剩余人员信息已保存到 {output_filename}")
    print(f"文件位置: {full_path}")


#获取值班人员与机动人员信息
def execute_query_and_show_remaining(scheduling_info, time_info, people_info):

    query_day = time_info['task_day']
    query_time_range = time_info['task_time_range']

    queried_people=remove_queried_people(scheduling_info, query_day, query_time_range)

    remaining_people_info = update_remaining_people(queried_people, people_info)
    print("舰艇机动人员人数:", len(remaining_people_info))


    return remaining_people_info,queried_people

#根据历史派遣次数更新匹配矩阵
def update_matching_matrix_1(matching_matrix_info, people_info):
    updated_matching_matrix = {}
    for position_name, position_info in matching_matrix_info.items():
        updated_scores = {}
        for person_str, score in position_info.items():
            # 将字符串转换为整数
            person = int(person_str)
            if person in people_info:
                frequency = people_info[person]["frequency"]
                updated_score = max(score-frequency / 10, 0.01)
                # 保留三位小数
                updated_score = round(updated_score, 3)
                person_str = str(person)
                updated_scores[person_str] = updated_score
            else:
                # 如果人员编号不在people_info中，则直接将分数添加到更新的分数中
                updated_scores[person] = score
                updated_scores[person_str] = updated_score
        updated_matching_matrix[position_name] = updated_scores
    return updated_matching_matrix

#根据在岗信息更新匹配矩阵
def update_matching_matrix_2(updated_matching_matrix, queried_people):
    # 遍历匹配矩阵中的每个岗位
    for position_name, position_info in updated_matching_matrix.items():
        # 遍历已查询的人员列表
        for person in queried_people:
            # 如果该人员在当前岗位下有匹配度，则将其匹配度清零
            if str(person) in position_info:
                position_info[str(person)] = 0
    return updated_matching_matrix


def update_matching_matrix_2_1(updated_matching_matrix, queried_people):
    # 将queried_people列表中的元素转换为字符串类型，以匹配匹配矩阵中的键
    queried_people_str = [str(person) for person in queried_people]

    # 遍历匹配矩阵中的每个岗位
    for position_name, position_info in updated_matching_matrix.items():
        # 遍历当前岗位下的每个人员及其匹配度
        for person, match_score in position_info.items():
            # 如果该人员不在queried_people列表中，则将其匹配度清零
            if person not in queried_people_str:
                position_info[person] = 0

    return updated_matching_matrix


#把queried_people的信息清零
def update_data(queried_people,people_info,matching_matrix_info):
    # 更新匹配矩阵

    updated_matching_matrix = update_matching_matrix_1(matching_matrix_info, people_info)
    update_matching_matrix = update_matching_matrix_2(updated_matching_matrix, queried_people)

    return update_matching_matrix

# 现在，updated_matching_matrix 中包含了更新后的匹配矩阵信息

#把除queried_people外的人员匹配信息清零
def update_data_2(queried_people,people_info,matching_matrix_info):
    # 更新匹配矩阵
    # updated_matching_matrix = update_matching_matrix(matching_matrix_info, people_info)
    #根据历史派遣信息更新矩阵
    updated_matching_matrix = update_matching_matrix_1(matching_matrix_info, people_info)
    #
    update_matching_matrix = update_matching_matrix_2_1(updated_matching_matrix, queried_people)

    return update_matching_matrix


# 任务可行性检测
def assignment_check(A, B):
    if A >= B:
        result = {"result": "任务可以完成"}
    else:
        result = {"result": "现有人员不足以完成任务"}
    return result

#选择合适的岗位
def select_position_by_priority(task_info):
    positions = list(task_info.keys())  # 获取所有岗位名称
    priority_map = {pos: task_info[pos] for pos in positions}  # 生成岗位优先级映射

    # 过滤掉没有优先级的岗位
    filtered_positions = [pos for pos in positions if pos in priority_map]

    if not filtered_positions:
        return None  # 如果没有符合条件的岗位，则返回 None

    # 获取优先级最高的岗位
    max_priority = max([priority_map[pos]["priority"] for pos in filtered_positions])

    # 获取所有优先级最高的岗位
    max_priority_positions = [pos for pos in filtered_positions if priority_map[pos]["priority"] == max_priority]

    # 如果有多个优先级最高的岗位，则随机选择一个
    selected_position = random.choice(max_priority_positions)

    # 记录该岗位所需人数
    required_people = priority_map[selected_position]["number"]

    return selected_position, required_people


def update_matching_matrix_3(updated_matching_matrix, position, people_position):
    if position in updated_matching_matrix:
        # 获取更新后的当前岗位的人员信息
        position_info = updated_matching_matrix[position]

        # 将people_position中的所有人员的适配度设为0
        for position, people_list in people_position.items():
            for person in people_list:
                #print(person + "删除")
                if person in position_info:
                    position_info[person] = 0

        # 按照适配度降序排列人员
        sorted_people = sorted(position_info.items(), key=lambda x: x[1], reverse=True)
        # 更新当前岗位下的人员信息
        updated_matching_matrix[position] = {person[0]: person[1] for person in sorted_people}
        # 获取当前岗位的人员信息
        position_info = updated_matching_matrix[position]

        return position_info

    return None  # 如果岗位不在任务信息中，则返回 None
# 选择某岗位派遣人员
def people_group_selection(position_info, required_people):
    selected_people = []
    remaining_required_people = required_people
    # 遍历岗位信息
    for person, suitability in position_info.items():
        # 如果适配度不为0且还需要更多人员
        if suitability != 0 and remaining_required_people > 0:
            selected_people.append(person)
            remaining_required_people -= 1
    return selected_people, max(0, remaining_required_people)

#更新任务信息与机动人员信息
def remove_selected_position(task_info, selected_position):
    # 从 task_info 中移除 selected_position 的信息
    if selected_position in task_info:
        del task_info[selected_position]
#按照岗位顺序更新派遣信息
def sort_people_position_by_position(people_position):
    sorted_people_position = {}
    # 将people_position中的岗位按照字母顺序排序
    sorted_positions = sorted(people_position.keys())
    for position in sorted_positions:
        sorted_people_position[position] = people_position[position]
    return sorted_people_position

#
def update_remaining_people_info(remaining_people_info, people_position):
    """
    移除 remaining_people_info 中被 people_position 指定的人员信息。
    :param remaining_people_info: 包含人员信息的字典。
    :param people_position: 指定需要移除的人员编号的字典。
    :return: 更新后的人员信息字典。
    """
    # 遍历 people_position 中的所有岗位
    for positions in people_position.values():
        # 遍历每个岗位中的人员编号
        for person_id in positions:
            person_id_int = int(person_id)  # 确保编号是整数类型
            # 如果该编号在 remaining_people_info 中，就移除对应的人员信息
            if person_id_int in remaining_people_info:
                del remaining_people_info[person_id_int]

    return remaining_people_info

def out(people_position, position_remaining_required_people):
    total_remaining_required_people = sum(position_remaining_required_people.values())
    sorted_position_remaining_required_people = dict(
        sorted(position_remaining_required_people.items(), key=lambda x: int(x[0].replace("岗位", ""))))
    # 将数据存储到一个字典中
    data = {
        "任务状态": "任务可以完成" if total_remaining_required_people == 0 else f"任务不可以完成，任务缺失{total_remaining_required_people}人",
        "岗位信息": []
    }

    # 遍历每个岗位，并将信息存储到字典中
    for position, remaining_required_people in sorted_position_remaining_required_people.items():
        assigned_people = people_position[position]
        position_data = {
            "岗位名称": position,
            "已派遣人员": assigned_people,
            "缺失人数": remaining_required_people
        }
        data["岗位信息"].append(position_data)

        # 最后，将 data 字典封装到最外层的结构中，并加上 "code" 和 "msg" 字段
    output = {
        "code": 1,  # 1表示成功
        "msg": "成功",
        "data": data
    }
    return output


def check_task_completion(people_position, position_remaining_required_people):
    total_remaining_required_people = sum(position_remaining_required_people.values())
    sorted_position_remaining_required_people = dict(sorted(position_remaining_required_people.items(), key=lambda x: int(x[0].replace("岗位", ""))))
    if total_remaining_required_people == 0:
        print("任务可以完成")
        print("每个岗位派遣人员为：")
        for position, remaining_required_people in sorted_position_remaining_required_people.items():
            assigned_people = people_position[position]
            print(f"{position}: {', '.join(assigned_people)}")
    else:
        print(f"任务不可以完成，任务缺失{total_remaining_required_people}人")
        print("每个岗位派遣人数和缺失人数：")
        for position, remaining_required_people in sorted_position_remaining_required_people.items():
            assigned_people = people_position[position]
            print(f"{position}: {', '.join(assigned_people)}, 缺失人数: {remaining_required_people}")

def check_task_completion_1(people_position, position_remaining_required_people,remaining_people_info):
    total_remaining_required_people = sum(position_remaining_required_people.values())
    sorted_position_remaining_required_people = dict(sorted(position_remaining_required_people.items(), key=lambda x: int(x[0].replace("岗位", ""))))
    if total_remaining_required_people == 0:
        print("任务可以完成")
        print("该方案每个岗位派遣人数为：")
        for position, remaining_required_people in sorted_position_remaining_required_people.items():
            assigned_people = people_position[position]
            print(f"{position}: {', '.join(assigned_people)}")
        print("该方案目前最多可替换人数为:",len(remaining_people_info))
    else:
        print(f"任务不可以完成，任务缺失{total_remaining_required_people}人")
        print("该方案每个岗位派遣人数和缺失人数：")
        for position, remaining_required_people in sorted_position_remaining_required_people.items():
            assigned_people = people_position[position]
            print(f"{position}: {assigned_people}, 缺失人数: {remaining_required_people}")

def out_1(people_position, position_remaining_required_people,remaining_people_info):
    total_remaining_required_people = sum(position_remaining_required_people.values())
    sorted_position_remaining_required_people = dict(
        sorted(position_remaining_required_people.items(), key=lambda x: int(x[0].replace("岗位", ""))))
    # 将数据存储到一个字典中
    data = {
        "任务可调整人数":len(remaining_people_info),
        "任务状态": "任务可以完成" if total_remaining_required_people == 0 else f"任务不可以完成，任务缺失{total_remaining_required_people}人",
        "岗位信息": [],
        "机动人员信息":[]
    }

    # 遍历每个岗位，并将信息存储到字典中
    for position, remaining_required_people in sorted_position_remaining_required_people.items():
        assigned_people = people_position[position]
        position_data = {
            "岗位名称": position,
            "已派遣人员": assigned_people,
            "缺失人数": remaining_required_people
        }
        data["岗位信息"].append(position_data)
     # 填充机动人员信息
    for person_id, info in remaining_people_info.items():
        data["机动人员信息"].append({
            "number": person_id,
            "name": info['name'],
            "frequency": info['frequency']})

        # 最后，将 data 字典封装到最外层的结构中，并加上 "code" 和 "msg" 字段
    output = {
        "code": 1,  # 1表示成功
        "msg": "成功",
        "data": data
    }
    return output

def task_assignment_choice(data):

    # 初始化两个字典用于存储保留岗位信息和需替换岗位信息
    people_position_or = {}
    people_position_de = {}
    # 遍历读取到的数据，并填充上面定义的两个字典
    for item in data["保留岗位信息"]:
        # 由于示例中的"已派遣人员"是人员编号的列表，如果需要转换为名字，需要额外的信息或步骤
        people_position_or[item["岗位名称"]] = item["已派遣人员"]

    for item in data["需替换岗位信息"]:
        # 同上，这里直接存储人员编号列表
        people_position_de[item["岗位名称"]] = item["已派遣人员"]

    # 打印结果以验证
    print("保留岗位信息 (people_position_or):")
    for position, people in people_position_or.items():
        print(f'{position}: {", ".join(people)}')

    print("\n需替换岗位信息 (people_position_de):")
    for position, people in people_position_de.items():
        print(f'{position}: {", ".join(people)}')
    return people_position_or,people_position_de

#将人员筛选数据补齐
def update_positions_with_priority(initial_positions, full_positions):
    # 创建最终的岗位列表
    final_positions = {}

    # 遍历初始岗位信息
    for position, person_ids in initial_positions.items():
        if position in full_positions:
            # 根据初始岗位信息更新人数和优先级
            final_positions[position] = {
                "number": len(person_ids),  # 人员ID数量作为number
                "priority": full_positions[position]['priority']  # 从full_positions获取优先级
            }
    return final_positions

#选择人员后检验
def check_task_completion_2(people_position,people_position_de,change_people_position, remaining_people_info):
    # 准备一个消息模板用于显示置换方案
    print("任务可以完成,任务分配新方案是")
    print("每个岗位派遣人员为：")
    # 遍历people_position打印当前人员安排
    for position, people in people_position.items():
        msg_parts = [f"{position}: {', '.join(people)}"]
        # 检查是否存在需置换的人员
        if position in people_position_de:
            # 准备需置换的人员信息
            to_be_replaced = ', '.join(people_position_de[position])
            # 准备新派遣的人员信息
            new_people = ', '.join(change_people_position[position] if position in change_people_position else [])
            # 格式化显示置换方案
            if to_be_replaced and new_people:  # 确保两边都有信息才显示置换方案
                msg_parts.append(f"置换人员: {to_be_replaced} -> {new_people}")
            # 打印完整的信息，包括岗位、现有人员和置换方案
        print(' '.join(msg_parts))
    print("该方案目前最多可替换人数为:", len(remaining_people_info))
#选择人员后的输出
def out_2(people_position, people_position_de,change_people_position, remaining_people_info):
    # 对岗位信息按岗位编号进行排序
    sorted_change_people_position = dict(
        sorted(change_people_position.items(), key=lambda x: int(x[0].replace("岗位", ""))))
    # 初始化数据字典
    data = {
        "任务可调整人数":  len(remaining_people_info),
        "任务状态": "任务可以完成,新方案是:",
        "岗位信息": [],
        "置换方案": [],
        "机动人员信息": []
    }
    # 遍历每个岗位，并将信息存储到字典中
    for position, remaining_required_people in sorted_change_people_position.items():
        assigned_people = people_position.get(position, [])
        position_data = {
            "岗位名称": position,
            "已派遣人员": assigned_people,
            "缺失人数": remaining_required_people
        }
        data["岗位信息"].append(position_data)

        # 如果当前岗位有需置换的人员信息
        if position in people_position_de:
            # 遍历每个需置换的人员编号，构建置换方案
            for person_id in people_position_de[position]:
                # 找到相应的新派遣人员编号
                new_person_id = change_people_position.get(position, [])
                # 添加置换方案到数据字典
                data["置换方案"].append({
                    "岗位名称": position,
                    "置换人员": f"{person_id} -> {', '.join(new_person_id)}"
                })
    # 填充机动人员信息
    for person_id, info in remaining_people_info.items():
        data["机动人员信息"].append({
            "number": person_id,
            "name": info['name'],
            "frequency": info['frequency']
        })

        # 最后，将 data 字典封装到最外层的结构中，并加上 "code" 和 "msg" 字段
    output = {
        "code": 1,  # 1表示成功
        "msg": "成功",
        "data": data
    }
    return output

def get_people_position_data(task_info):
    data_1 = task_info['data']
    # 提取岗位信息，将岗位名称映射到已派遣人员
    people_position = {item["岗位名称"]: item["已派遣人员"] for item in data_1["岗位信息"]}
    # 提取每个岗位的缺失人数
    position_remaining_required_people = {item["岗位名称"]: item["缺失人数"] for item in data_1["岗位信息"]}
    # 提取机动人员信息，包括编号、名字和频率
    remaining_people_info = {person["number"]: {"name": person["name"], "frequency": person["frequency"]} for person in
                             data_1["机动人员信息"]}
    return people_position, position_remaining_required_people, remaining_people_info


def task_person_algorithm(task_data,people_data,scheduling_data,matching_data,time_data,choice_data):
    #load数据
    task_info = prepare_bushu_data(task_data)

    people_info = prepare_people_data(people_data)

    scheduling_info = prepare_scheduling_data(scheduling_data)

    matching_info = prepare_matching_matrix_data(matching_data)

    position_completed = {}  # 已分配岗位
    people_position = {}  # 已分配人员
    position_remaining_required_people = {}


    # 获取值班人员和机动人员信息
    remaining_people_info, queried_people = execute_query_and_show_remaining(scheduling_info, time_data,
                                                                             people_info)
    # 更新匹配矩阵，把值更人员信息清0
    update_matching_matrix_zhigeng = update_data(queried_people, people_info, matching_info)
    READY = task_info.copy()

    while len(position_completed) < len(task_info):
        # 选择岗位，以及该岗位人数
        selected_position, required_people = select_position_by_priority(READY)
        # print(selected_position, required_people)
        # 更新目标岗位的匹配矩阵
        position_info = update_matching_matrix_3(update_matching_matrix_zhigeng, selected_position, people_position)
        selected_people, remaining_required_people = people_group_selection(position_info, required_people)
        people_position[selected_position] = selected_people
        position_remaining_required_people[selected_position] = remaining_required_people

        position_completed[selected_position] = True
        remove_selected_position(READY, selected_position)


    if choice_data['code'] == 0:
        check_task_completion(people_position, position_remaining_required_people)
        return out(people_position, position_remaining_required_people)
    else:
        remaining_people_info = update_remaining_people_info(remaining_people_info, people_position)
        check_task_completion_1(people_position, position_remaining_required_people, remaining_people_info)
        return out_1(people_position, position_remaining_required_people, remaining_people_info)


def task_person_algorithm_choice(task_data,people_data,matching_data,people_position_data,task_assignment_choice_data,choice_data):
    # 检查 'data' 键是否存在，然后再访问 '任务可调整人数'
    if 'data' in people_position_data and '任务可调整人数' in people_position_data['data']:
        adjustable_number = people_position_data['data']['任务可调整人数']
        print(f"任务可调整人数: {adjustable_number}")
        people_position, position_remaining_required_people, remaining_people_info = get_people_position_data(
            people_position_data)
        if choice_data['code'] == 1 and len(remaining_people_info) > 0:
            task_info = prepare_bushu_data(task_data)
            people_info = prepare_people_data(people_data)
            people_position_or, people_position_de = task_assignment_choice(task_assignment_choice_data)

            matching_info = prepare_matching_matrix_data(matching_data)
            # 更新匹配矩阵，只保留剩余机动人员的匹配度
            update_matching_matrix_choice = update_data_2(remaining_people_info, people_info, matching_info)
            READY_1 = update_positions_with_priority(people_position_de, task_info)
            # 将people_position中的内容转为数组
            assignmen_person_ids = []
            for person_ids in people_position.values():
                assignmen_person_ids.extend(person_ids)
            assignmen_person_ids = sorted(set(int(id) for id in assignmen_person_ids))

            change_position_completed = {}  # 已分配待替换岗位
            change_people_position = {}  # 待替换已分配人员
            while len(change_position_completed) < len(people_position_de):
                selected_position, required_people = select_position_by_priority(READY_1)
                position_info = update_matching_matrix_3(update_matching_matrix_choice, selected_position,
                                                         change_people_position)
                selected_people, remaining_required_people = people_group_selection(position_info, required_people)
                change_people_position[selected_position] = selected_people
                position_remaining_required_people[selected_position] = remaining_required_people
                change_position_completed[selected_position] = True
                remove_selected_position(READY_1, selected_position)
            remaining_people_info = update_remaining_people_info(remaining_people_info, change_people_position)
            # 将补充人员添加到保留人员分配方案里
            for position, new_person_ids in change_people_position.items():
                # 如果岗位已存在于people_position_or中，则更新该岗位的人员编号列表
                if position in people_position_or:
                    # 直接添加新的人员编号到对应岗位的列表中
                    people_position_or[position].extend(new_person_ids)
                else:
                    # 如果岗位不存在于people_position_or中，则直接添加岗位和其人员编号列表
                    people_position_or[position] = new_person_ids
            check_task_completion_2(people_position_or, people_position_de, change_people_position,
                                    remaining_people_info)
            return out_2(people_position, people_position_de, change_people_position, remaining_people_info)
        else:
            output = {
                "code": 2,  # 1表示成功
                "msg": "目前无机动人员可进行替换", }
            print('目前无机动人员可进行替换')
            return output
        if people_position_data['data']['任务可调整人数'] == 0:
            output = {
                "code": 2,  # 1表示成功
                "msg": "目前无机动人员可进行替换", }
            return output

    else:
        output = {
            "code": 2,  # 1表示成功
            "msg": "目前无机动人员可进行替换", }
        return output



if __name__ == '__main__':

    # 读入任务数据
    task_data = read_json_file("/home/phytium/projects/AI_SERVER/test_data/algo3/task.json")
    # 读入人员信息
    people_data = read_json_file("/home/phytium/projects/AI_SERVER/test_data/algo3/persons.json")
    #读入排班数据
    scheduling_data=read_json_file("/home/phytium/projects/AI_SERVER/test_data/algo3/scheduling.json")
    #读入任务时间
    time_data = read_json_file("/home/phytium/projects/AI_SERVER/test_data/algo3/task_time.json")
    #读入匹配数据
    matching_data = read_json_file("/home/phytium/projects/AI_SERVER/test_data/algo3/persons_value.json")
    # 读取人员是否进行选择
    choice_data = read_json_file('/home/phytium/projects/AI_SERVER/test_data/algo3/persons_choice.json')
    #运行函数task_person_algorithm，返回任务人员匹配结果
    task_person_algorithm(task_data, people_data, scheduling_data, matching_data, time_data, choice_data)

    #读取当前任务人员分配方案
    people_position_data = read_json_file("/home/phytium/projects/AI_SERVER/test_data/algo3/output_suc_choice.json")
    # 读入人员选择结果
    task_assignment_choice_data = read_json_file('/home/phytium/projects/AI_SERVER/test_data/algo3/manual_choice.json')
    #print('task_assignment_choice_data',task_assignment_choice_data)
    # 运行函数task_person_algorithm_choice，更新任务人员匹配结果
    task_person_algorithm_choice(task_data, people_data, matching_data,  people_position_data,task_assignment_choice_data,choice_data)

