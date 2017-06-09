# _*_ encoding:utf-8 _*_

from django import  forms
from operation.models import UserAsk
import re
class UserAskForm (forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']
## 自定义验证方式
    def clean_mobile(self):
        ##验证是否合法
        mobile = self.cleaned_data['mobile']
        RE_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(RE_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise  forms.ValidationError(u'手机号码非法',code='mobile_inval')