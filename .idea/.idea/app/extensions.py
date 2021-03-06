from flask import jsonify,request,session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from functools import wraps
from flask_mail import Mail,Message
import redis

db = SQLAlchemy()
mail = Mail()
whooshee = Whooshee()
r = redis.Redis()

from app.models import Photo,Drama

#登录验证装饰器
def login_required(func):
    @wraps(func)
    def yes_or_no():
        token = request.form.get('token')
        if r.get(token) is None:
            return jsonify(Event1001())
        return func(token)
    return yes_or_no


#发送邮件函数
def send_email(subject,to,body):
    message = Message(subject=subject,recipients=[to],body=body)
    mail.send(message)


def Event0(**kwargs):
    return {
                "status": 0,
                "data": kwargs
            }

def Event1001():
    return {
            "status": 1001,
            "message": "token失效"
        }

def Event1002():
    return {
            "status": 1002,
            "message": "对象不存在"
        }

def Event1003():
    return {
            "status": 1003,
            "message": "已存在对象"
        }

def Event1004():
    return {
            "status": 1004,
            "message": "请求错误"
        }

def Event1005(message):
    return {
                "status": 1005,
                "message": message
            }

def Giveuser(user):
    Rdramas = Drama.query.filter(Drama.user_id==user.id,Drama.solution==None).all()
    Adramas = Drama.query.filter(Drama.user_id==user.id,Drama.solution!=None).all()

    return {
        "userid": user.id,
        "name": user.name,
        "avatar": user.avatar,
        "email": user.email,
        "Rdramas": [{"dramaid":drama.id} for drama in Rdramas],
        "Adramas": [{"dramaid":drama.id} for drama in Adramas],
        "collects": [{"dramaid":drama.id} for drama in user.collects],
        "follows": [{"followid":follow.id,"followname":follow.name} for follow in user.follows]
    }


def Givedrama(drama):
    photos = Photo.query.filter_by(drama_id=drama.id,content=True).all()
    animepictures = Photo.query.filter_by(drama_id=drama.id,cover=True).all()
    if drama.animefrom == 1:
        animelink = drama.animeseasonid
    else:
        animelink = drama.animelink

    return {
            "dramaid": drama.id,
            "authorid": drama.user.id,
            "authorname": drama.user.name,
            "title": drama.title,
            "content": drama.content,
            "time": drama.time,
            "photos": [photo.image for photo in photos],
            "animetitle": drama.animetitle,
            "animedescribe": drama.animedescribe,
            "animepicture": [photo.image for photo in animepictures],
            "animefrom": drama.animefrom,
            "animelink": animelink,
            "comment": [Givecomment(comment) for comment in drama.comments]
        }

def Givecomment(comment):
    return {
                "commentid": comment.id,
                "authorname": comment.author,
                "authorid": comment.author_id,
                "content": comment.text,
                "time": comment.time
            }

def Giveask(drama):
    photos = Photo.query.filter_by(drama_id=drama.id, content=True).all()
    return {
        "dramaid": drama.id,
        "authorid": drama.user.id,
        "authorname": drama.user.name,
        "title": drama.title,
        "content": drama.content,
        "time": drama.time,
        "photos": [photo.image for photo in photos],
        "comment": [Givecomment(comment) for comment in drama.comments]
    }
