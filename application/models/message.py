# coding: utf-8
from datetime import datetime
from ._base import db

class Messsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, default="")
    checked = db.Column(db.Boolean, nullable=False, default=False)
    checked_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender = db.relationship('User',
                             backref=db.backref('sender_messages', lazy='dynamic',
                                                order_by="desc(Messsage.created_at)",
                                                cascade="all, delete, delete-orphan"),
                             foreign_keys=[sender_id])

    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver = db.relationship('User', backref=db.backref('messages', lazy='dynamic',
                                                          order_by="desc(Messsage.created_at)",
                                                          cascade="all, delete, delete-orphan"),
                               foreign_keys=[receiver_id])
