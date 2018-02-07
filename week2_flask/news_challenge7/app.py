#!/usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json, os

#file_list = os.listdir('/home/shiyanlou/files/')
#file_list = os.listdir('/jerry/shiyanlou_homework/week2_flask/files/')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self,name):
        self.name = name
    
    def __repr__(self):
        return '<Category(name=%s)>'%self.name

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))
    content = db.Column(db.Text)

    def __init__(self, title, content, category, created_time=None):
        self.title = title
        self.content = self.content
        if created_time is None:
            created_time = datetime.utcnow()
        self.created_time = created_time
        self.category = category

    def __repr__(self):
        return '<File(title=%s)>'%self.title



@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    titles = File.query.all()
    return render_template('index.html', files=titles)   


@app.route('/files/<file_id>')
def file(file_id):
    files = File.query.all()
    file_id_find = 0
    for titles in files:
        if int(file_id) == titles.id:
            file_id_find = 1
            return render_template('file.html', file_info = titles)
    if file_id_find == 0:
        abort(404)









