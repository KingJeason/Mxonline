# _*_ encoding:utf-8 _*_

from django import  forms
from captcha.fields import CaptchaField
### 必须和html表单里的name一致
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误 '})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误 '})

class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)






