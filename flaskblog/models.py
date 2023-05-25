from flask import current_app
from flaskblog import db,login_manager
from flask_login import UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    usernames=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(60),unique=False,nullable=False)
    def __repr__(self):
        return f"User('{self.usernames}','{self.email}')"
    
class Mail(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120),unique=False,nullable=False)
    def __repr__(self):
        return f"mail('{self.email}')"

