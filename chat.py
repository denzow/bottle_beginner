# coding:utf-8
import json
import csv
import os
from datetime import datetime
from bottle import route, run, template, request, response, redirect, static_file

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
    # cookieにユーザ情報がない場合は入室画面へ戻す
    if not username:
        return redirect("/")


    # 永続化してあるこれまでのチャット履歴を取得
    talk_list = get_talk()

    return template("chat_room", username=username, talk_list=talk_list)


@route("/talk", method=["POST"])
def talk():
    """
    発言を登録し、チャットルームへリダイレクトします
    :return:
    """

    # マルチバイトデータのためgetではなくgetunicodeにする
    chat_data = request.POST.getunicode("chat")
    # 発言者をcookieから取得
    username = request.get_cookie("username")
    # 発言時間取得
    talk_time = datetime.now()
    # 発言保存
    save_talk(talk_time, username, chat_data)

    return redirect("/chat_room")


@route("/api/talk", method=["GET", "POST"])
def talk_api():
    """
    発言一覧を管理するAPI

    GET -> 発言一覧を戻す
    POST -> 発言を保存する

    json eg.

    [
        {
            talk_time:2016-09-17 15:00:49.937402
            username:sayamada
            chat_data:おはよう
        }
    :
        },
        {
            talk_time:2016-09-17 15:58:03.200027
            username:sayamada
            chat_data:こんにちは
        },
        {
            talk_time:2016-09-17 15:58:12.289631
            username:sayamada
            chat_data:元気ですか？
        }

    ]

    :return:
    """

    if request.method == "GET":
        talk_list = get_talk()
        return json.dumps(talk_list)

    elif request.method == "POST":
        # マルチバイトデータのためgetではなくgetunicodeにする
        chat_data = request.POST.getunicode("chat")
        # 発言者をcookieから取得
        username = request.get_cookie("username")
        # 発言時間取得
        talk_time = datetime.now()
        # 発言保存
        save_talk(talk_time, username, chat_data)

        return json.dumps({
            "status": "success"
        })


@route("/api/last_talk")
def get_last_talk():
    """
    最終発言だけを戻すAPI

    :return:
    """
    talk_list = get_talk()
    return json.dumps(talk_list[-1])


@route('/static/<file_path:path>')
def static(file_path):
    """
    静的ファイル専用のルーティング
    /static/* は静的ファイルが存在するものとして動く
    :param file_path:
    :return:
    """
    return static_file(file_path, root="./static")

def save_talk(talk_time, username, chat_data):
    """
    チャットデータを永続化する関数
    CSVとしてチャットの内容を書き込んでいる

    :param username:
    :param chat_data:
    :param talk_time:
    :return:
    """
    with open('./chat_data.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([talk_time, username, chat_data])


def get_talk():
    """
    永続化されたチャットデータを取得する関数
    CSVからリスト形式でデータを取得している
    :return:
    """
    talk_list = []
    # 履歴ファイルがない場合は空ファイルを作成する
    if not os.path.exists("./chat_data.csv"):
        open("./chat_data.csv", "w").close()

    with open('./chat_data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            talk_list.append({
                "talk_time": row[0],
                "username": row[1],
                "chat_data": row[2],
            })

    return talk_list

# サーバの起動
run(host='localhost', port=8080, debug=True, reloader=True)

