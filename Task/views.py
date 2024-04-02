import json
import logging

from django.http import JsonResponse
from django.views import View

from algorithms.person_position_match import recommend_person
from utils.enumerationClass.common_enum import Option, OptMethod, PersonChoice
from utils.enumerationClass.response_code_enum import jsonify, ResponseCode

logger = logging.getLogger(__name__)


class Algorithm1(View):

    def post(self, request):
        try:
            params = json.loads(request.body)
            option = int(params['option'])  # 算法一的那种请求
            task = str(params['task'])  # 部署任务名称
            positions = params['positions']  # 战位数据
            persons = params['persons']  # 舰员数据

            if not task:
                msg = f'部署任务，不能为空'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

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
                res = recommend_person(model_path='./algorithms/bert-base-chinese')
            elif option == Option.position_rec.value:
                res = recommend_person(model_path='./algorithms/bert-base-chinese')
            else:
                res = recommend_person(model_path='./algorithms/bert-base-chinese')

            if res['code'] == ResponseCode.SUCCESS.value:
                logger.info(f'algorithm1 执行返回成功')
                return JsonResponse(jsonify(code=ResponseCode.SUCCESS.value, data=res['data']))
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
            # res = algorithm2(task, opt_method, base_data, schedule_days,
            #                  max_days, max_shifts, shift_nums)
            # 测试数据
            with open('./test_data/algo2/输出结果排班表&辅助决策输入人工排班表.json', 'r', encoding='utf-8') as f:
                res = json.loads(f.read())
            # ---

            if res['code'] == ResponseCode.SUCCESS.value:
                logger.info(f'algorithm2 执行返回成功')
                return JsonResponse(jsonify(code=ResponseCode.SUCCESS.value, data=res['data']))
            else:
                logger.info(f'algorithm2 执行返回失败，code 为 {res["code"]}')
                return JsonResponse(jsonify(code=res['code'], msg=res['message']))
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
            task = params['task']  # 部署任务：中船提供的数据，json数据
            scheduling = params['scheduling']  # 当前值更表：算法二的输出结果，json数据
            task_time = params['task_time']  # 任务时间  "13:00-14:00"
            person_choice = params['person_choice']  # 人员是否需要逐个确认
            manual_choice = params['manual_choice']  # 人工选择过的数据

            if not task:
                msg = f'部署任务，不能为空'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if not scheduling:
                msg = f'当前值更表，不能为空'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if not task_time:
                msg = f'任务时间，不能为空'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            if not PersonChoice.value_exists(person_choice):
                msg = f'person_choice 参数不支持 {person_choice}'
                return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))

            logger.info(f"person_choice：{PersonChoice.value_name(person_choice)}")
            if person_choice == PersonChoice.need.value:
                if not manual_choice:
                    msg = f"{PersonChoice.value_name(person_choice)}, 必须传递 manual_choice（人工选择过的数据）"
                    return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))
                else:
                    manual_choice = None
        except KeyError as e:
            logger.error(e, exc_info=True)
            msg = f"请求参数缺失: {e}"
            return JsonResponse(jsonify(code=ResponseCode.PARAMETER_ERROR.value, msg=msg))
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse(jsonify(code=ResponseCode.UNKNOWN_ERROR.value))

        try:
            # res = algorithm3(task, scheduling, task_time, person_choice, manual_choice)
            # 测试数据
            with open('./test_data/algo3/algo3_result.json', 'r', encoding='utf-8') as f:
                res = json.loads(f.read())
            # ---

            if res['code'] == ResponseCode.SUCCESS.value:
                logger.info(f'algorithm3 执行返回成功')
                return JsonResponse(jsonify(code=ResponseCode.SUCCESS.value, data=res['data']))
            else:
                logger.info(f'algorithm3 执行返回失败，code 为 {res["code"]}')
                return JsonResponse(jsonify(code=res['code'], msg=res['message']))
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
