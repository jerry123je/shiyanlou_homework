#!/usr/bin/env python3

from flask import Flask, render_template
import json, os

file_list = os.listdir('/home/shiyanlou/files/')

app = Flask(__name__)

@app.route('/')
def index():
    artical = {}
    for file_name in file_list:
        with open(os.path.join('/home/shiyanlou/files',file_name)) as f:
            artical[file_name] = json.loads(f.read())
        return render_template('index.html', artical=artical)   


@app.route('/file/<filename>')
def file(filename):
    return render_template('file.html', filename=filename)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=3000)
        #host = '0.0.0.0',
        #port = 3000,
        #debug = True
    #)








