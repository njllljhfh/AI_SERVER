# 这是用启发式算法求解排班问题的代码V0.1.0
# 虽然可能不够规范，为了方便起见，此版本不进行类的定义
# 同样可能不够规范，此版本在main.py中厘清并依次调用各个函数


# 首先是数据读入模块，先用数据生成模块代替
# import data_read
# import GA_test
# import correction_test
# import data_output
from algorithms.algorithm2 import data_read, GA_test, correction_test, data_output


# import data_read_test
# 读入数据，读入失败则报错
def algorithm2(task, opt_method, base_data, schedule_days, shift_nums, max_days, max_shifts):
    data = data_read.read_data(task, opt_method, base_data, schedule_days, shift_nums, max_days, max_shifts)
    if data['type'] == 1:
        p_size = 10
        gen = 3
    else:
        p_size = 20
        gen = 100

    solution, solution_fitness = GA_test.ga(data, p_size, gen)
    solution_out = correction_test.result_correction(solution, data)
    # json_data = data_output.output_data(data, solution_out)
    res = data_output.output_data(data, solution_out, to_json=False)  # 返回dict

    return res
