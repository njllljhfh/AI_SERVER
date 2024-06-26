import json
import logging

from django.http import JsonResponse
from django.views import View

from algorithms.algorithm2.algorithm2 import algorithm2
from algorithms.algorithm3.task_person_algorithm_v12 import task_person_algorithm, task_person_algorithm_choice
from algorithms.person_position_match import recommend_person, recommend_position, recommend_matrix, NpEncoder
from utils.enumerationClass.common_enum import Option, OptMethod, PersonChoice
from utils.enumerationClass.response_code_enum import jsonify, ResponseCode

logger = logging.getLogger(__name__)


class Algorithm1(View):

    def post(self, request):
        try:
            params = json.loads(request.body)
            option = int(params['option'])  # 算法一的那种请求
            positions = params['positions']  # 战位数据
            persons = params['persons']  # 舰员数据

            if not positions:
                msg = f'战位数据，不能为空'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if not persons:
                msg = f'舰员数据，不能为空'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if not Option.value_exists(option):
                msg = f'option 参数不支持 {option}'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            logger.info(f"Option：{Option.value_name(option)}")
            if option == Option.person_rec.value:
                if len(positions) != 1:
                    msg = f'战位个数应为 1，实际个数为 {len(positions)}'
                    return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

                persons_min_num = 2
                if len(persons) < persons_min_num:
                    msg = f'舰员个数应大于等于 {persons_min_num}，实际个数为 {len(persons)}'
                    return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))
            elif option == Option.position_rec.value:
                positions_min_num = 2
                if len(positions) < positions_min_num:
                    msg = f'战位个数应大于等于 {positions_min_num}，实际个数为 {len(positions)}'
                    return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

                if len(persons) != 1:
                    msg = f'舰员个数应为 1，实际个数为 {len(persons)}'
                    return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))
            elif option == Option.match_matrix.value:
                min_num = 2
                if len(positions) < min_num:
                    msg = f'战位个数应大于等于 {min_num}，实际个数为 {len(positions)}'
                    return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

                if len(persons) < min_num:
                    msg = f'舰员个数应大于等于 {min_num}，实际个数为 {len(persons)}'
                    return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))
        except KeyError as e:
            logger.error(e, exc_info=True)
            msg = f"请求参数缺失: {e}"
            return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse(jsonify(code=ResponseCode.UNKNOWN_ERROR.value))

        try:
            # 测试数据
            # with open('./test_data/algo1/r1.json', 'r') as f:
            #     res = json.loads(f.read())
            # ---
            if option == Option.person_rec.value:
                res = recommend_person(model_path=r"./algorithms/bert-base-chinese",
                                       person_data=persons,
                                       position_data=positions)
            elif option == Option.position_rec.value:
                res = recommend_position(model_path='./algorithms/bert-base-chinese',
                                         person_data=persons,
                                         position_data=positions)
            else:
                res = recommend_matrix(model_path='./algorithms/bert-base-chinese',
                                       person_data=persons,
                                       position_data=positions)

            if res['code'] == ResponseCode.SUCCESS.value:
                logger.info(f'algorithm1 执行返回成功')
                return JsonResponse(jsonify(code=ResponseCode.SUCCESS.value, data=res['data']), encoder=NpEncoder)
            else:
                logger.info(f'algorithm1 执行返回失败，code 为 {res["code"]}')
                return JsonResponse(jsonify(code=res['code'], msg=res['message']))
        except Exception as e:
            msg = f'algorithm1 执行报错: {e}'
            logger.error(msg, exc_info=True)
            return JsonResponse(jsonify(code=ResponseCode.ALGORITHM_ERROR.value))
        finally:
            logger.info("-" * 3)


class Algorithm2(View):

    def post(self, request):
        try:
            params = json.loads(request.body)
            task = params['task']  # 部署任务，包括任务名，和json数据（result3输出的结果）
            opt_method = int(params['opt_method'])  # 优化方式
            base_data = params.get('base_data', None)  # 中船的决策数据（格式为算法二输出的json格式）
            schedule_days = int(params['schedule_days'])  # 排班天数
            max_days = int(params['max_days'])  # 最大连续工作天数
            max_shifts = int(params['max_shifts'])  # 最大工作班次
            # 预留字段：每一个岗位每天有几班：数组长度跟算法1的 result3 中的站位个数相同，每个值是站位的班次 ，目前先给空数组
            shift_nums = params.get('shift_nums', [])

            if not task:
                msg = f'部署任务，不能为空'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if not OptMethod.value_exists(opt_method):
                msg = f'opt_method 参数不支持 {opt_method}'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            logger.info(f"Option：{OptMethod.value_name(opt_method)}")
            if opt_method == OptMethod.assistant_decision.value:
                if not base_data:
                    msg = f"优化方式为{OptMethod.value_name(opt_method)}, 必须传递 base_data（中船的决策数据）"
                    return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))
            else:
                base_data = None

            if not task:
                msg = f'部署任务，不能为空'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if not (0 < schedule_days <= 365):
                msg = f"排班天数应大于 0 小于等于 365"
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if not (0 < max_days <= 365):
                msg = f"最大连续工作天数应大于 0 小于等于 20"
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if not (0 < max_shifts <= 365):
                msg = f"最大工作班次应大于 0 小于等于 365"
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))
        except KeyError as e:
            logger.error(e, exc_info=True)
            msg = f"请求参数缺失: {e}"
            return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse(jsonify(code=ResponseCode.UNKNOWN_ERROR.value))

        try:
            res = algorithm2(task, opt_method, base_data, schedule_days, shift_nums,
                             max_days, max_shifts)
            # 测试数据
            # with open('./test_data/algo2/输出结果排班表&辅助决策输入人工排班表.json', 'r', encoding='utf-8') as f:
            #     res = json.loads(f.read())
            # ---

            if res['code'] == ResponseCode.SUCCESS.value:
                logger.info(f'algorithm2 执行返回成功')
                return JsonResponse(jsonify(code=ResponseCode.SUCCESS.value, data=res['data']))
            else:
                logger.info(f'algorithm2 执行返回失败，code 为 {res["code"]}')
                return JsonResponse(jsonify(code=res['code'], msg=res['msg']))
        except Exception as e:
            msg = f'algorithm2 执行报错: {e}'
            logger.error(msg, exc_info=True)
            return JsonResponse(jsonify(code=ResponseCode.ALGORITHM_ERROR.value))
        finally:
            logger.info("-" * 3)


class Algorithm3(View):

    def post(self, request):
        try:
            params = json.loads(request.body)
            task = params['task']  # 部署任务：中船提供的数据（测试时，算法提供测试数据）
            persons = params['persons']  # 舰上所有人员以及被派遣次数：中船提供的数据（测试时，算法提供测试数据）
            scheduling = params['scheduling']  # 当前值更表：算法二的输出结果，json数据。
            task_time = params['task_time']  # 从 scheduling 里面选择某一天。选择时间段
            persons_value = params['persons_value']  # 舰上所有人员对任务中岗位的匹配矩阵：算法一的result3输出结果，json数据。
            person_choice = params['person_choice']  # 人员是否需要逐个确认
            # 人工选择过的数据,
            # 当 person_choice 为 1 时：如果接口返回数据中 "任务可调整人数" 字段为 0 表明没有可用于调整的人员了，不需要再次发送请求。
            manual_choice = params.get('manual_choice', None)
            people_position_data = params.get('people_position_data', None)  # 上次调用算法返回的任务人员分配方案

            if not task:
                msg = f'部署任务，不能为空'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if not persons:
                msg = f'舰上所有人员以及被派遣次数，不能为空'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if not manual_choice and not scheduling:
                msg = f'当前值更表，不能为空'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if manual_choice and not people_position_data:
                msg = f'上次调用算法返回的任务人员分配方案，不能为空'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if not manual_choice and not task_time:
                msg = f'任务时间，不能为空'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if not persons_value:
                msg = f'舰上所有人员对任务中岗位的匹配矩阵，不能为空'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if not PersonChoice.value_exists(person_choice):
                msg = f'person_choice 参数不支持 {person_choice}'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            logger.info(f"person_choice：{PersonChoice.value_name(person_choice)}")
            if person_choice == PersonChoice.need.value:
                choice_data = {
                    "code": person_choice,
                    "message": "人员需要进行选择"
                }
                # if not manual_choice:
                #     msg = f"{PersonChoice.value_name(person_choice)}, 必须传递 manual_choice（人工选择过的数据）"
                #     return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))
            else:
                choice_data = {
                    "code": person_choice,
                    "message": "人员不需要进行选择"
                }

        except KeyError as e:
            logger.error(e, exc_info=True)
            msg = f"请求参数缺失: {e}"
            return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse(jsonify(code=ResponseCode.UNKNOWN_ERROR.value))

        try:
            # 测试数据
            # with open('./test_data/algo3/algo3_result.json', 'r', encoding='utf-8') as f:
            #     res = json.loads(f.read())
            # ---

            if not manual_choice:
                res = task_person_algorithm(task, persons, scheduling, persons_value, task_time, choice_data)
            else:
                res = task_person_algorithm_choice(task, persons, persons_value,
                                                   people_position_data, manual_choice, choice_data)

            if res['code'] == ResponseCode.SUCCESS.value:
                logger.info(f'algorithm3 执行返回成功')
                return JsonResponse(jsonify(code=ResponseCode.SUCCESS.value, data=res['data']))
            else:
                logger.info(f'algorithm3 执行返回失败，code 为 {res["code"]}')
                return JsonResponse(jsonify(code=res['code'], msg=res['msg']))
        except Exception as e:
            msg = f'algorithm3 执行报错: {e}'
            logger.error(msg, exc_info=True)
            return JsonResponse(jsonify(code=ResponseCode.ALGORITHM_ERROR.value))
        finally:
            logger.info("-" * 3)


class MyTest(View):

    def get(self, request):
        try:
            a = float(request.GET.get('a'))
            b = float(request.GET.get('b'))
            result = a / b
            data = {
                'result': result,
            }
            logger.info(f'MyTest --- res={result}')

            return JsonResponse(jsonify(code=ResponseCode.SUCCESS.value, data=data))
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse(jsonify(data=request.GET, code=ResponseCode.UNKNOWN_ERROR.value))
