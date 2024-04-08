# 第一版先用易于实现的遗传算法代替灰狼算法
import numpy as np
import random
from multiprocessing import Pool


def generate_schedule(K, positions_list, max_S):
    # 生成排班表，或者说生成种群，确保了每个岗位上都是合适的人
    #K, positions_list, max_S = args
    matrix = np.full((max_S, K), None)  # 创建空矩阵
    for position, workers in enumerate(positions_list):
        for shift in range(max_S):
            if workers:
                person_id, _ = random.choice(workers)
                matrix[shift, position] = person_id
    return matrix


'''
def generate_population_parallel(population_size, K, positions_list, max_S):
    args = [(K, positions_list, max_S) for _ in range(population_size)]
    with Pool() as pool:
        population = pool.map(generate_schedule, args)
    return population
'''


def generate_population_serial(population_size, K, positions_list, max_S):
    population = []
    #args = [K, positions_list, max_S]
    for _ in range(population_size):
        individual = generate_schedule(K, positions_list, max_S)
        population.append(individual)
    return population


'''
def calculate_fitness_vectorized(schedule, match_matrix):
    """
    使用向量化方法计算排班表的适应度。
    :param schedule: 排班表，其中schedule[i, j]是第i个班次第j个岗位的员工编号。
    :param match_matrix: 员工对岗位的匹配度矩阵。
    :return: 排班表的适应度。
    """
    # 获取匹配度
    fitness_values = match_matrix[schedule.astype(int), np.arange(match_matrix.shape[1])]
    # 计算总适应度
    total_fitness = np.sum(fitness_values)
    return total_fitness
'''


def calculate_fitness_vectorized(schedule, match_matrix, penalty=10, max_cd=2, additional_penalty=20,
                                 max_shift=5, shift_penalty=30):
    """
    计算排班表的适应度，考虑连续值班、总值班次数限制。

    :param schedule: 排班表矩阵，一个个体。
    :param match_matrix: 员工对岗位的匹配度矩阵。
    :param penalty: 连续值班的基本惩罚分数。
    :param max_cd: 允许的最大连续值班天数。
    :param additional_penalty: 超过max_cd天连续值班的额外惩罚分数。
    :param max_shift: 每个人允许的最大总值班次数。
    :param shift_penalty: 超过max_shift次值班的惩罚分数。
    :return: 考虑惩罚的排班表适应度。
    """
    total_fitness = 0
    shifts_counter = {}  # 跟踪每个员工的值班次数

    # 遍历每个岗位
    for column in range(schedule.shape[1]):
        consecutive_days = 0
        last_employee = -1

        # 遍历每个班次
        for row in range(schedule.shape[0]):
            employee_id = schedule[row, column]
            total_fitness += match_matrix[employee_id, column]

            # 更新员工的值班次数
            shifts_counter[employee_id] = shifts_counter.get(employee_id, 0) + 1

            if employee_id == last_employee:
                consecutive_days += 1
                if consecutive_days > max_cd:
                    total_fitness -= additional_penalty
            else:
                consecutive_days = 1
                last_employee = employee_id

            if consecutive_days > 1:
                total_fitness -= penalty

    # 应用总值班次数限制的惩罚
    for employee_id, shifts in shifts_counter.items():
        if shifts > max_shift:
            total_fitness -= (shifts - max_shift) * shift_penalty  # 每超出一次，惩罚累加

    return total_fitness


def selection(population_fitness, num_selected):
    """
    选择操作：根据适应度选择个体进入下一代。

    # 基于适应度进行选择，这里简单使用适应度比例选择
    fitness_sum = sum(population_fitness)
    selection_probs = [fitness / fitness_sum for fitness in population_fitness]
    selected_indices = np.random.choice(range(len(population_fitness)), size=num_selected, p=selection_probs)


       修改后的选择操作，适用于适应度值可能为负的情况。
       """
    # 将所有适应度平移到正数区间
    min_fitness = min(population_fitness)
    offset = -min_fitness + 1  # 保证所有适应度值为正
    adjusted_fitness = [fitness + offset for fitness in population_fitness]

    # 计算调整后的适应度总和
    adjusted_fitness_sum = sum(adjusted_fitness)

    # 计算选择概率
    selection_probs = [fitness / adjusted_fitness_sum for fitness in adjusted_fitness]
    selected_indices = np.random.choice(range(len(population_fitness)), size=num_selected, p=selection_probs)
    '''
    # 校正概率之和为1
    probs_sum = sum(selection_probs)
    selection_probs = [prob / probs_sum for prob in selection_probs]

    # 根据选择概率选择个体，确保不会因概率和不为1导致的错误
    selected_indices = np.random.choice(range(len(population_fitness)), size=num_selected, replace=False,
                                        p=selection_probs)
    '''

    return selected_indices


def crossover(schedule_a, schedule_b, crossover_rate=0.5):
    """
    交叉操作：两个排班表交换一些行。

    :param schedule_a: 第一个排班表。
    :param schedule_b: 第二个排班表。
    :param crossover_rate: 交叉率，决定了有多少行会被交换。
    :return: 两个新的排班表。
    """
    if np.random.rand() > crossover_rate:
        # 根据交叉率决定是否进行交叉
        return schedule_a.copy(), schedule_b.copy()

    num_rows = schedule_a.shape[0]
    # 选择一个随机点进行行交换
    crossover_point = np.random.randint(1, num_rows)  # 避免选择第0行或最后一行，确保至少交换一行

    # 生成新的排班表
    new_schedule_a = np.vstack((schedule_a[:crossover_point, :], schedule_b[crossover_point:, :]))
    new_schedule_b = np.vstack((schedule_b[:crossover_point, :], schedule_a[crossover_point:, :]))

    return new_schedule_a, new_schedule_b


def mutate(schedule, mutation_rate=0.1):
    """
    变异操作：随机选择一些列并重新排列这些列内部元素的顺序。

    :param schedule: 排班表矩阵，一个个体。
    :param mutation_rate: 变异率，决定了有多少列会被重新排列。
    :return: 经过变异操作的新排班表矩阵。
    """
    num_columns = schedule.shape[1]  # 获取列数
    mutated_schedule = schedule.copy()  # 复制排班表以避免直接修改原始数据

    for column in range(num_columns):
        if np.random.rand() < mutation_rate:  # 根据变异率决定是否对该列进行变异
            # 选择该列并随机排列内部元素
            mutated_column = np.random.permutation(mutated_schedule[:, column])
            mutated_schedule[:, column] = mutated_column

    return mutated_schedule


def genetic_algorithm1(K, positions_list, max_S, population_size, generations, match_matrix, test_schedule):
    # 生成初始种群
    #print('----------------------------')
    #print("here1")
    population = generate_population_serial(population_size - 1, K, positions_list, max_S)
    population.append(test_schedule)
    best_fitness = float('-inf')
    best_individual = None


    for generation in range(generations):
        population_fitness = np.zeros(population_size)
        ii = 0
        # 计算适应度
        '''
        with Pool() as pool:
            #population_fitness = pool.map(lambda schedule: calculate_fitness_vectorized(schedule, match_matrix),
            #                              population)
            population_fitness = pool.map(calculate_fitness_vectorized(schedule, match_matrix), population)
        '''

        for schedule in population:
            population_fitness[ii] = calculate_fitness_vectorized(schedule, match_matrix)
            ii = ii + 1

        # 使用NumPy函数找到最高适应度的索引
        current_best_idx = np.argmax(population_fitness)
        current_best_fitness = population_fitness[current_best_idx]
        # 更新最优适应度和最优个体
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_individual = population[current_best_idx]

        # 选择
        selected_indices = selection(population_fitness, population_size // 2)
        selected_population = [population[i] for i in selected_indices]

        # 交叉
        new_population = []
        crossover_rate = 0.7  # 可以调整这个交叉率
        for i in range(0, len(selected_population), 2):
            if i + 1 < len(selected_population):
                parent_a = selected_population[i]
                parent_b = selected_population[i + 1]
                # 根据交叉率决定是否进行交叉
                if np.random.rand() < crossover_rate:
                    child_a, child_b = crossover(parent_a, parent_b)
                else:
                    child_a, child_b = parent_a, parent_b
                new_population.extend([child_a, child_b])
            else:
                # 如果选中的个体数量是奇数，将最后一个个体直接加入新种群
                new_population.append(selected_population[i])

        # 更新种群为新一代

        # 变异
        mutation_rate = 0.05  # 设置变异率，可以根据需要调整
        for i in range(len(new_population)):
            # 对每个个体应用变异操作
            new_population[i] = mutate(new_population[i], mutation_rate)

        # 生成新一代种群
        elite_size = max(1, int(population_size * 0.1))  # 保留10%的精英个体，至少保留1个
        elite_indices = np.argpartition(-population_fitness, elite_size)[:elite_size]
        elite_individuals = [population[i] for i in elite_indices]

        # 更新种群：新生成的种群加上精英个体
        population = new_population + elite_individuals

        # 确保新种群大小不超过设定的种群大小，如果超过了，可以根据适应度进行裁剪
        if len(population) > population_size:
            fitnesses = [calculate_fitness_vectorized(individual, match_matrix) for individual in population]
            sorted_indices = np.argsort(-np.array(fitnesses))
            population = [population[i] for i in sorted_indices[:population_size]]

        # print(f"Generation {generation + 1}: Best Fitness = {max(population_fitness)}")
        while len(population) < population_size:
            # 从现有种群中随机选择两个个体进行交叉
            parents = random.sample(population, 2)
            child_a, child_b = crossover(parents[0], parents[1])

            # 对生成的子代进行变异
            child_a = mutate(child_a)
            child_b = mutate(child_b)

            # 将新生成的子代添加到种群中
            population.append(child_a)
            # 检查是否还需要更多个体，如果是，再添加一个
            if len(population) < population_size:
                population.append(child_b)

    # 返回最终种群和适应度
    return best_individual, best_fitness


def genetic_algorithm2(K, positions_list, max_S, population_size, generations, match_matrix):
    # 生成初始种群
    #print('----------------------------')
    #print("here2")
    population = generate_population_serial(population_size, K, positions_list, max_S)
    best_fitness = float('-inf')
    best_individual = None
    for generation in range(generations):
        population_fitness = np.zeros(population_size)
        ii = 0
        # 计算适应度
        '''
        with Pool() as pool:
            #population_fitness = pool.map(lambda schedule: calculate_fitness_vectorized(schedule, match_matrix),
            #                              population)
            population_fitness = pool.map(calculate_fitness_vectorized(schedule, match_matrix), population)
        '''

        for schedule in population:
            population_fitness[ii] = calculate_fitness_vectorized(schedule, match_matrix)
            ii = ii + 1

        # 使用NumPy函数找到最高适应度的索引
        current_best_idx = np.argmax(population_fitness)
        current_best_fitness = population_fitness[current_best_idx]
        # 更新最优适应度和最优个体
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_individual = population[current_best_idx]

        # 选择
        selected_indices = selection(population_fitness, population_size // 2)
        selected_population = [population[i] for i in selected_indices]

        # 交叉
        new_population = []
        crossover_rate = 0.7  # 可以调整这个交叉率
        for i in range(0, len(selected_population), 2):
            if i + 1 < len(selected_population):
                parent_a = selected_population[i]
                parent_b = selected_population[i + 1]
                # 根据交叉率决定是否进行交叉
                if np.random.rand() < crossover_rate:
                    child_a, child_b = crossover(parent_a, parent_b)
                else:
                    child_a, child_b = parent_a, parent_b
                new_population.extend([child_a, child_b])
            else:
                # 如果选中的个体数量是奇数，将最后一个个体直接加入新种群
                new_population.append(selected_population[i])

        # 更新种群为新一代

        # 变异
        mutation_rate = 0.05  # 设置变异率，可以根据需要调整
        for i in range(len(new_population)):
            # 对每个个体应用变异操作
            new_population[i] = mutate(new_population[i], mutation_rate)

        # 生成新一代种群
        elite_size = max(1, int(population_size * 0.1))  # 保留10%的精英个体，至少保留1个
        elite_indices = np.argpartition(-population_fitness, elite_size)[:elite_size]
        elite_individuals = [population[i] for i in elite_indices]

        # 更新种群：新生成的种群加上精英个体
        population = new_population + elite_individuals

        # 确保新种群大小不超过设定的种群大小，如果超过了，可以根据适应度进行裁剪
        if len(population) > population_size:
            fitnesses = [calculate_fitness_vectorized(individual, match_matrix) for individual in population]
            sorted_indices = np.argsort(-np.array(fitnesses))
            population = [population[i] for i in sorted_indices[:population_size]]

        # print(f"Generation {generation + 1}: Best Fitness = {max(population_fitness)}")
        while len(population) < population_size:
            # 从现有种群中随机选择两个个体进行交叉
            parents = random.sample(population, 2)
            child_a, child_b = crossover(parents[0], parents[1])

            # 对生成的子代进行变异
            child_a = mutate(child_a)
            child_b = mutate(child_b)

            # 将新生成的子代添加到种群中
            population.append(child_a)
            # 检查是否还需要更多个体，如果是，再添加一个
            if len(population) < population_size:
                population.append(child_b)

    # 返回最终种群和适应度
    return best_individual, best_fitness


def ga(data, population_size, generations):
    if data['type'] == 1:
        #print(data)
        population, population_fitness = genetic_algorithm1(data['K'], data['skill_list'], max(data['S']) * data['D'],
                                                            population_size, generations,
                                                            data['skill_matrix'], data['test_schedule'])
        #(K, positions_list, max_S, population_size, generations, match_matrix, test_schedule)
    elif data['type'] == 2:
        population, population_fitness = genetic_algorithm2(data['K'], data['skill_list'], max(data['S']) * data['D'],
                                                            population_size, generations,
                                                            data['skill_matrix'])
    else:
        print("优化类型type有误")
        population = []
        population_fitness = []
    return population, population_fitness


if __name__ == '__main__':
    import data_read_test

    data = data_read_test.data_read()
    population_size = 10
    generations = 3
    # 运行遗传算法
    population, population_fitness = ga(data, population_size, generations)
    print(population)
    print(population_fitness)
