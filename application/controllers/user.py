# coding: utf-8
from datetime import datetime
from flask import render_template, Blueprint, redirect, request, url_for, flash, g, json, abort
from ..utils.permissions import UserPermission
from ..utils.uploadsets import avatars, crop_image, process_image_for_cropping
from ..models import db, User, Notification, Follow, Message, BlackList
from ..forms import SettingsForm, ChangePasswordForm

bp = Blueprint('user', __name__)


@bp.route('/people/<int:uid>', defaults={'page': 1})
@bp.route('/people/<int:uid>/page/<int:page>')
def profile(uid, page):
    user = User.query.get_or_404(uid)
    votes = user.voted_pieces.paginate(page, 20)
    return render_template('user/profile.html', user=user, votes=votes)


@bp.route('/people/<int:uid>/share', defaults={'page': 1})
@bp.route('/people/<int:uid>/share/page/<int:page>')
def share(uid, page):
    user = User.query.get_or_404(uid)
    pieces = user.pieces.paginate(page, 20)
    return render_template('user/share.html', user=user, pieces=pieces)

@bp.route('/people/<int:uid>/published', defaults={'page': 1})
@bp.route('/people/<int:uid>/published/page/<int:page>')
def published(uid, page):
    user = User.query.get_or_404(uid)
    pieces = user.pieces.filter_by(published = True).paginate(page, 20)
    return render_template('user/published.html', user=user, pieces=pieces)

@bp.route('/people/<int:uid>/likes', defaults={'page': 1})
@bp.route('/people/<int:uid>/likes/page/<int:page>')
def likes(uid, page):
    user = User.query.get_or_404(uid)
    collections = user.liked_collections.paginate(page, 20)
    return render_template('user/collections.html', user=user, collections=collections)


@bp.route('/my/online', methods=['POST'])
@UserPermission()
def online():
    """在线设置"""
    g.user.online = True
    
    return "You Are Online"

@bp.route('/my/follow/<int:uid>', methods=['POST'])
@UserPermission()
def follow(uid):
    """在线设置"""
    if uid == g.user.id:
        return '不能关注本人'
    user = User.query.get_or_404(uid)
    if g.user.follows.filter(Follow.followed_id == uid).count() > 0:
        return '已关注'
    follow = Follow()
    follow.follower_id = g.user.id
    follow.followed_id = user.id;
    db.session.add(follow)
    db.session.commit()
    return "关注成功"

@bp.route('/my/unfollow/<int:uid>', methods=['POST'])
@UserPermission()
def unfollow(uid):
    """在线设置"""
    followeds = g.user.follows.filter(Follow.followed_id == uid)
    if followeds.count() == 0:
        return '未关注'
    for followed in followeds:
        db.session.delete(followed)
    db.session.commit()
    return "取消关注成功"

@bp.route('/my/block/<int:uid>', methods=['POST'])
@UserPermission()
def block(uid):
    """在线设置"""
    if uid == g.user.id:
        return '不能拉黑本人'
    user = User.query.get_or_404(uid)
    if g.user.blocked.filter(BlackList.blocked_id == uid).count() > 0:
        return '已加黑名单'
    block = BlackList()
    block.user_id = g.user.id
    block.blocked_id = user.id;
    db.session.add(block)
    db.session.commit()
    return "拉黑成功"

@bp.route('/my/unblock/<int:uid>', methods=['POST'])
@UserPermission()
def unblock(uid):
    """在线设置"""
    blockeds = g.user.blocked.filter(BlackList.blocked_id == uid)
    if blockeds.count() == 0:
        return '未拉黑'
    for blocked in blockeds:
        db.session.delete(blocked)
    db.session.commit()
    return "取消拉黑成功"

@bp.route('/my/settings', methods=['GET', 'POST'])
@UserPermission()
def settings():
    """个人设置"""
    form = SettingsForm(obj=g.user)
    if form.validate_on_submit():
        form.populate_obj(g.user)
        db.session.add(g.user)
        db.session.commit()
        flash('设置已保存')
        return redirect(url_for('.settings'))
    return render_template('user/settings.html', form=form)


@bp.route('/my/change_password', methods=['GET', 'POST'])
@UserPermission()
def change_password():
    """修改密码"""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        g.user.password = form.new_password.data
        db.session.add(g.user)
        db.session.commit()
        flash('密码修改成功')
        return redirect(url_for('.settings'))
    return render_template('user/change_password.html', form=form)


@bp.route('/my/upload_avatar', methods=['POST'])
@UserPermission()
def upload_avatar():
    try:
        filename, (w, h) = process_image_for_cropping(request.files['file'], avatars)
    except Exception, e:
        return json.dumps({'result': False, 'error': e.__repr__()})
    else:
        return json.dumps({
            'result': True,
            'image_url': avatars.url(filename),
            'width': w,
            'height': h
        })


@bp.route('/my/crop_avatar', methods=['POST'])
@UserPermission()
def crop_avatar():
    filename = request.form.get('filename')
    top_left_x_ratio = request.form.get('top_left_x_ratio', type=float)
    top_left_y_ratio = request.form.get('top_left_y_ratio', type=float)
    bottom_right_x_ratio = request.form.get('bottom_right_x_ratio', type=float)
    bottom_right_y_ratio = request.form.get('bottom_right_y_ratio', type=float)

    try:
        new_avatar_filename = crop_image(filename, avatars, top_left_x_ratio, top_left_y_ratio,
                                         bottom_right_x_ratio, bottom_right_y_ratio)
    except Exception, e:
        return json.dumps({'result': False, 'message': e.__repr__()})
    else:
        g.user.avatar = new_avatar_filename
        db.session.add(g.user)
        db.session.commit()
        return json.dumps({'result': True, 'image_url': avatars.url(new_avatar_filename)})


@bp.route('/my/notifications', defaults={'page': 1})
@bp.route('/my/notifications/page/<int:page>')
@UserPermission()
def notifications(page):
    notifications = g.user.notifications.paginate(page, 15)
    check_all_notifications()
    return render_template('user/notifications.html', notifications=notifications)


@bp.route('/my/notification/<int:uid>/check')
@UserPermission()
def check_notification(uid):
    notification = Notification.query.get_or_404(uid)
    notification.checked = True
    notification.checked_at = datetime.now()
    db.session.add(notification)
    db.session.commit()
    return redirect(notification.link)


@bp.route('/my/notifications/check', methods=['POST'])
@UserPermission()
def check_all_notifications():
    notifications = g.user.notifications.filter(~Notification.checked)
    for notification in notifications:
        notification.checked = True
        notification.checked_at = datetime.now()
        db.session.add(notification)
    db.session.commit()
    return json.dumps({'result': True})

@bp.route('/my/messages/', defaults={'page': 1})
@bp.route('/my/messages/<int:uid>/page/<int:page>', defaults={'page': 1})
@bp.route('/my/messages/page/<int:page>')
@UserPermission()
def messages(page, uid):
    print page, uid
    if uid == 0:
        messages = Message.query.filter(((Message.sender_id == g.user.id)\
                & (Message.sender_deleted == False))\
                |((Message.receiver_id == g.user.id)\
                &(Message.receiver_deleted == False)
                )).order_by("-created_at").paginate(page, 15)
    else:
        messages = Message.query.filter(((Message.sender_id == g.user.id)\
                & (Message.sender_deleted == False) & (Message.receiver_id == uid))\
                |((Message.receiver_id == g.user.id)\
                &(Message.receiver_deleted == False) & (Message.sender_id == uid)
                )).order_by("-created_at").paginate(page, 15)
    check_all_messages()
    return render_template('user/messages.html', messages=messages)

@bp.route('/my/messages/check', methods=['POST'])
@UserPermission()
def check_all_messages():
    notifications = g.user.messages.filter(~Message.checked)
    for notification in notifications:
        notification.checked = True
        notification.checked_at = datetime.now()
        db.session.add(notification)
    db.session.commit()
    return json.dumps({'result': True})

@bp.route('/people/<int:uid>/message/', methods = ['GET', 'POST'])
@UserPermission()
def send_message(uid):
    """个人设置"""
    user = User.query.get_or_404(uid)
    if request.method == "POST":
        if g.user.id == uid:
            return redirect(url_for('.messages'))
        elif user.blocked.filter(BlackList.blocked_id == g.user.id).count() > 0:
            flash('发送失败')
            return render_template('user/send_message.html', receiver = user)
        content = request.form.get('content')
        if not content:
            flash('内容不可为空')
            return render_template('user/send_message.html', receiver = user)
        else:
            m = Message(sender_id = g.user.id, receiver_id = uid, content = content)
            db.session.add(m)
            db.session.commit()
            flash('发送成功')
            return redirect(url_for('.messages', uid=0, page=1))
    else:
        return render_template('user/send_message.html', receiver = user)

@bp.route('/my/message/<int:mid>', methods = ['DELETE'])
@UserPermission()
def delete_message(mid):
    message = Message.query.get_or_404(mid)
    if message.sender_id == g.user.id:
        message.sender_deleted = True
    elif message.receiver_id == g.user.id:
        message.receiver_deleted = True
    db.session.add(message)
    db.session.commit()
    return '删除成功'
