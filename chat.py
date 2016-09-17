# coding:utf-8
import bottle
from bottle import route, run, template


@route("/")
def index():

    return template("index")

# サーバの起動
run(host='localhost', port=8080, debug=True, reloader=True)

