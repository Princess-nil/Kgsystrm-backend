from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import Form, ValidationError
from wtforms.fields import StringField, IntegerField, FileField
from flask_wtf.file import FileAllowed, FileSize
from wtforms.validators import Email, Length, EqualTo, DataRequired, InputRequired
from models.auth import User
from flask import request

class BaseForm(Form):
    @property
    def messages(self):
        message_list = []
        if self.errors:
            for error in self.errors.values():
                message_list.extend(error)
        return message_list

class LoginForm(BaseForm):
    username = StringField(validators=[Length(3, 20, message="请输入正确长度的用户名！")])
    userpwd = StringField(validators=[Length(6, 20, message="请输入正确长度的密码！")])

class DataSetAddForm(BaseForm):
    dataname = StringField(validators=[Length(1, 20, message="请输入正确长度的数据集名称！")])
    datadescription = StringField(validators=[Length(1, 200, message="请输入正确长度的描述！")])
    userid = IntegerField(validators=[InputRequired(message="请传入用户ID")])

class DataSetEditForm(BaseForm):
    dataname = StringField(validators=[Length(1, 20, message="请输入正确长度的数据集名称！")])
    datadescription = StringField(validators=[Length(1, 200, message="请输入正确长度的描述！")])
    dataid = IntegerField(validators=[InputRequired(message="请传入数据集ID")])

class UploadFileForm(BaseForm):
    file = FileField(validators=[FileAllowed(['txt'],
        message="文件格式不符合要求！"), FileSize(max_size=1024*1024*5, message="文件最大不能超过2M！")])
