# coding:utf-8
from bottle import route, run


@route('/')
@route('/hello')
def hello():
    """
    route でどのようなURLでアクセスした際に関数が実行されるかを
    登録します。

    文字列をreturnすると、そのままブラウザで表示されます

    routeでのルーティングは重ねる事で、複数のURLにマップさせる事もできます。
    :return:
    """
    return "Hello World!"


@route("/hello/<name>")
def hello_name(name):
    """
    ダイナミックルーティングではurlに埋め込まれたパラメータを
    取得することができます

    :param name:
    :return:
    """
    return "Hello {} !".format(name)


@route("/no/<your_no:int>")
def no(your_no):
    """
    ルーティングでは数字のみ・正規表現等で細かく設定できます

    eg.
    /no/100 -> OK
    /no/one -> NG

    :param your_no:
    :return:
    """

    return "Your No is {} !".format(your_no)


# サーバの起動
run(host='localhost', port=8080, debug=True, reloader=True)

