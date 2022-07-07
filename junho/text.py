
def message(uidb64, token):
     return f"아래 링크를 클릭하면 회원가입 인증이 완료됩니다. \n\n 회원가입 링크 : http://54.180.193.83:8081/accounts/activate/{uidb64}/{token}\n\n 감사합니다"


def passwordmessage(uidb64, token):
     return f"아래 링크를 클릭하면 비밀번호 변경 페이지로 이동합니다. \n\n 비밀번호 변경 링크 : http://54.180.193.83:8081/accounts/passwd/{uidb64}/{token}\n\n 감사합니다"

