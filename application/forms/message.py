# coding: utf-8
from flask import g
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import Optional, URL, DataRequired, EqualTo, Email

class SendMessageForm(Form):
    content = StringField('内存')
    uid = StringField('发给')
    username = StringField('发给')
