from flask import Blueprint, render_template
from simpledu.models import db, Course, User

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/<username>')
def user_index(username):
    u = User.query.filter(User.username==username).first()
    return render_template('user.html', u=u)
