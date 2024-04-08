# 这是用启发式算法求解排班问题的代码V0.1.0
# 虽然可能不够规范，为了方便起见，此版本不进行类的定义
# 同样可能不够规范，此版本在main.py中厘清并依次调用各个函数


# 首先是数据读入模块，先用数据生成模块代替
from algorithms.algorithm2 import data_read, GA_test, correction_test, data_output


# import data_read
# import GA_test
# import correction_test
# import data_output
# import data_read_test
# 读入数据，读入失败则报错
def algorithm2(task, opt_method, base_data, schedule_days, shift_nums, max_days, max_shifts):
    data = data_read.read_data(task, opt_method, base_data, schedule_days, shift_nums, max_days, max_shifts)
    # print(data)
    if data['type'] == 1:
        p_size = 10
        gen = 3
    else:
        p_size = 20
        gen = 100
    # if __name__ == '__main__':
    solution, solution_fitness = GA_test.ga(data, p_size, gen)
    # print(solution, solution_fitness)
    solution_out = correction_test.result_correction(solution, data)
    # solution_out_fitness = GA_test.calculate_fitness_vectorized(solution_out, data['skill_matrix'])
    json_data = data_output.output_data(data, solution_out)
    # print(solution_out)
    # print(solution_out_fitness)
    # print(json_data)
    return json_data


if __name__ == '__main__':
    import json

    # 读取JSON文件
    with open('matrix_to_json2.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # print(data)

    json_data = algorithm2(data['task'], data['opt_method'], data['base_data'], data['schedule_days'],
                           data['shift_nums'], data['max_days'], data['max_shifts'])

    print(json_data)
