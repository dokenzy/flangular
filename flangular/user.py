# -*- coding: utf-8 -*-

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, \
    SignatureExpired, BadSignature
from passlib.apps import custom_app_context as pwd_context
from flangular import app, db
from werkzeug.security import generate_password_hash
#from model import Model

class User(db.Document):
    email         = db.StringField()
    password_hash = db.StringField()

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': str(self.id)})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token

        return User.objects(id=data['id']).first()

    @classmethod
    def login(cls, email, password):
        user = cls.objects(email=email).first()
        if user and user.verify_password(password):
            return user

        return None

    @staticmethod
    def new_user(email, password):
        if User.objects(email=email).first() is not None:
            return
        user = User(email=email)
        user.password_hash = pwd_context.encrypt(password)
        user.save()
