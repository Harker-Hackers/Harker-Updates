#!/usr/bin/python3

import schoolopy
from os import environ
import pytz
import flask
from datetime import datetime

app = flask.Flask(__name__)
sc = schoolopy.Schoology(schoolopy.Auth(environ.get('SCHOOLOGY_KEY'), environ.get('SCHOOLOGY_SECRET')))
sc.limit = 20

def updates():
    updates = sc.get_group_updates(402741151)
    ls = []
    for update in updates:
        sender = sc.get_user(update['uid'])['name_display'].replace(' (Admin)', '')
        ls.append({
            'from': sender,
            'body': update['body'].replace('\n', '<br>'),
            'time': str(datetime.fromtimestamp(update['created'], pytz.timezone('America/Los_Angeles')))[:-9].replace(' ', ', ')
        })

    body = open('app/head.html', 'r').read() + '<style>' + open('app/static/style.css', 'r').read() + '</style>'
    for update in ls:
        body = body + '<hr><strong>' + update['from'] + '</strong><p>' + update['body'] + '<br><b>' + update['time'] + '</b></p>'
    return(body)

@app.route('/', methods=['GET'])
def main():
    return(updates())

@app.errorhandler(404)
def page_not_found(err):
    return(flask.render_template('404.html'))

@app.errorhandler(500)
def server_error(err):
    return(flask.render_template('500.html'))

if environ.get('ENVIROMENT') == 'test':
    app.run()