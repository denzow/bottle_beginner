# coding:utf-8
import bottle
from bottle import route, run, template, request, response


@route("/")
def index():
    return template("index")


@route("/enter", method=["POST"])
def enter():
    """
    入室処理を行います。
    フォームの情報をcookieに格納し、チャット時の名前として使用します。

    :return:
    """
    # POSTデータの確認
    username = request.POST.get("username")
    print("POST username is ", username)

    # cookieへの格納
    response.set_cookie("username", username)

    return ""



# サーバの起動
run(host='localhost', port=8080, debug=True, reloader=True)

