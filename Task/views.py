import json
import logging

from django.http import JsonResponse
from django.views import View

from utils.enumerationClass.response_code_enum import jsonify, ResponseCode

logger = logging.getLogger(__name__)


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


class Algorithm1(View):

    def post(self, request):
        data = {}
        try:
            data = json.loads(request.body)
            a = float(data.get('a'))
            b = float(data.get('b'))
            result = a / b
            data = {
                'result': result,
            }
            logger.info(f'Algorithm1 --- res={result}')

            return JsonResponse(jsonify(code=ResponseCode.SUCCESS.value, data=data))
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse(jsonify(data=data, code=ResponseCode.UNKNOWN_ERROR.value))


class Algorithm2(View):

    def post(self, request):
        data = {}
        try:
            data = json.loads(request.body)
            a = float(data.get('a'))
            b = float(data.get('b'))
            result = a / b
            data = {
                'result': result,
            }
            logger.info(f'Algorithm2 --- res={result}')

            return JsonResponse(jsonify(code=ResponseCode.SUCCESS.value, data=data))
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse(jsonify(data=data, code=ResponseCode.UNKNOWN_ERROR.value))


class Algorithm3(View):

    def post(self, request):
        data = {}
        try:
            data = json.loads(request.body)
            a = float(data.get('a'))
            b = float(data.get('b'))
            result = a / b
            data = {
                'result': result,
            }
            logger.info(f'Algorithm3 --- res={result}')

            return JsonResponse(jsonify(code=ResponseCode.SUCCESS.value, data=data))
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse(jsonify(data=data, code=ResponseCode.UNKNOWN_ERROR.value))
