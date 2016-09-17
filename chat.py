# coding:utf-8
from bottle import route, run, template, request, response, redirect


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

    return redirect("/chat_room")


@route("/chat_room")
def chat_room():
    """
    チャットを行う画面

    :return:
    """
    # cookieからの取得はrequestから行う
    username = request.get_cookie("username")

    return template("chat_room", username=username)



# サーバの起動
run(host='localhost', port=8080, debug=True, reloader=True)

