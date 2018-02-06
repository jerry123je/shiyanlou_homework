#!/usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, abort
import json, os

#file_list = os.listdir('/home/shiyanlou/files/')
file_list = os.listdir('/jerry/shiyanlou_homework/week2_flask/files/')

app = Flask(__name__)

artical = {}
for file_name in file_list:
    with open(os.path.join('/jerry/shiyanlou_homework/week2_flask/files',file_name)) as f:
        artical[file_name.split('.')[0]] = json.loads(f.read())

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    #print(artical)
    return render_template('index.html', artical=artical)   


@app.route('/file/<filename>')
def file(filename):
    #print(artical)
    print(filename)
    if filename not in artical.keys():
#        print('redirect to 404')
        abort(404)
    return render_template('file.html', filename=filename, artical=artical)









