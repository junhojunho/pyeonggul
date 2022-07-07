from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response



# class PasswdQustionFindError(APIException):
#     status_code = 400
#     default_detail = '질문과 답이 일치하지 않습니다.'
#     default_code = 'PYEON003'
    
# class PasswdEmailFindError(APIException):
#     status_code = 400
#     default_detail = '등록된 이메일이 아닙니다.'
#     default_code = 'PYEON003'
