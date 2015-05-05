# coding: utf-8
import re
import math
from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, URL, Optional
from ._helper import check_url, trim, remove_book_tilte_mark
from ..models import Piece


class PieceForm(Form):
    content = TextAreaField('文献', validators=[DataRequired('文献标题不能为空'), trim])
    # original = BooleanField('原创', default=False)
    author = StringField('第一作者', validators=[DataRequired('第一作者不能为空'), trim], description='')
    source = StringField('期刊名称',
                         validators=[DataRequired('期刊名称不能为空'), trim, remove_book_tilte_mark])
    source_link = StringField('文献链接',
                              validators=[Optional(), trim, check_url, URL(message='文献链接格式不正确')],
                              description='选填')
    comment = TextAreaField('附言',
                            validators=[Optional(), trim],
                            description='选填，个人感想或推荐理由')

    def validate_content(self, field):
        content = self.content.data
        content = content.strip()  # 去除首尾的空格
        content = re.sub('\r\n', '', content)  # 去掉换行符
        content = re.sub('\s+', ' ', content)  # 将多个空格替换为单个空格
        self.content.data = content

        content_length = Piece.calculate_content_length(self.content.data)
        if content_length > 200:
            raise ValueError('不超过200字')


class PieceCommentForm(Form):
    content = TextAreaField('评论',
                            validators=[DataRequired('评论内容不能为空')],
                            description='评论内容')
