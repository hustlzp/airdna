# coding: utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ._base import db
from ..utils.uploadsets import avatars
from ..utils import cache
from ..models import Follow


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    avatar = db.Column(db.String(200), default='default.png')
    motto = db.Column(db.String(100))
    password = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    votes_count = db.Column(db.Integer, default=0)
    pieces_count = db.Column(db.Integer, default=0)
    ncbipieces_count = db.Column(db.Integer, default=0)
    published_count = db.Column(db.Integer, default=0)
    liked_collections_count = db.Column(db.Integer, default=0)

    # 个人信息
    introduction = db.Column(db.String(200))
    research_areas = db.Column(db.String(200))
    education = db.Column(db.String(200))
    school = db.Column(db.String(200))
    city = db.Column(db.String(200))
    laboratory_site = db.Column(db.String(200))
    public_mailbox = db.Column(db.String(200))

    # 社交媒体
    weibo = db.Column(db.String(100))
    zhihu = db.Column(db.String(100))
    douban = db.Column(db.String(100))
    blog = db.Column(db.String(100))

    def __setattr__(self, name, value):
        # Hash password when set it.
        if name == 'password':
            value = generate_password_hash(value)
        super(User, self).__setattr__(name, value)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def followed_by(self, user_id):
        return self.followers.filter(Follow.follower_id == user_id).count() > 0

    def is_followed(self, user_id):
        return self.follows.filter(Follow.followed_id == user_id).count() > 0

    def is_block(self, user_id):
        return self.blocked.filter(BlackList.blocked_id == user_id).count() > 0

    def is_ncbi_collections(self, dbname, uid):
        
        from ..models import NCBIPiece, NCBICollectionPiece
        piece = NCBIPiece.query.filter(NCBIPiece.db_name == dbname, NCBIPiece.uid == uid).first() 
        return piece and self.ncbi_collections.filter(NCBICollectionPiece.piece_id == piece.id).first()

    @property
    def avatar_url(self):
        return avatars.url(self.avatar)

    @property
    def online(self):
        return cache.cache.get("user_online_{}".format(self.id))

    @online.setter
    def online(self, value):
        
        return cache.cache.set("user_online_{}".format(self.id), value, ex = 60)


    def __repr__(self):
        return '<User %s>' % self.name


class InvitationCode(db.Model):
    """"""
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(200))
    email = db.Column(db.String(100))
    used = db.Column(db.Boolean, default=False)
    sended_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 当用户使用此邀请码注册后，填充user_id字段
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=None)
    user = db.relationship('User',
                           backref=db.backref('invitation_code',
                                              cascade="all, delete, delete-orphan",
                                              uselist=False),
                           foreign_keys=[user_id])

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=None)
    sender = db.relationship('User',
                             backref=db.backref('sended_invitation_codes',
                                                cascade="all, delete, delete-orphan",
                                                uselist=False),
                             foreign_keys=[sender_id])

class BlackList(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                             backref=db.backref('blocked', lazy='dynamic',
                                                order_by="desc(BlackList.created_at)",
                                                cascade="all, delete, delete-orphan"),
                             foreign_keys=[user_id])
    blocked_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blocked_user = db.relationship('User',
                             backref=db.backref('block', lazy='dynamic',
                                                order_by="desc(BlackList.created_at)",
                                                cascade="all, delete, delete-orphan"),
                             foreign_keys=[blocked_id])

    created_at = db.Column(db.DateTime, default=datetime.now)
