# coding:utf-8
from bottle import route, run, template


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
    return "<h1>Hello {} !</h1>".format(name)


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


@route("/hello2/<name>")
def hello2_name(name):
    """
    テンプレート機能を使うことでデザインとロジックを切り離すことができます。
    bottleはシンプルなテンプレート機構が含まれているためすぐに利用できます。

    標準では./views/配下から指定されたテンプレートを取得します。
    その際拡張子はなんでも問題ありません。

    テンプレート側に渡すデータは名前付きパラメータを使用します。
    eg.
    display_name="TEST NAME"

    :param name:
    :return:
    """

    return template("sample", display_name=name)


# サーバの起動
run(host='localhost', port=8080, debug=True, reloader=True)

