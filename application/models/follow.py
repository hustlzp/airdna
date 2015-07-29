# coding: utf-8
from datetime import datetime
from ._base import db


class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed = db.relationship('User',
                             backref=db.backref('followers', lazy='dynamic',
                                                order_by="desc(Follow.created_at)",
                                                cascade="all, delete, delete-orphan"),
                             foreign_keys=[followed_id])
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    follower = db.relationship('User',
                             backref=db.backref('follows', lazy='dynamic',
                                                order_by="desc(Follow.created_at)",
                                                cascade="all, delete, delete-orphan"),
                             foreign_keys=[follower_id])

    created_at = db.Column(db.DateTime, default=datetime.now)
