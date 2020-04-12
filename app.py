from flask import Flask, render_template, make_response, request, redirect, url_for
import requests, json

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/success/<name>')
def success(name):
    # return 'welcome %s' % name
    return render_template('login.html', tips=name*1000)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm'].strip()
    else:
        user = request.args.get('nm')

    if user:
        return redirect(url_for('success', name=user))
    else:
        return render_template('login.html')


@app.route('/set_cookie', methods=['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        user = request.form['nm']

    # resp = make_response(('sucess'))
    resp = make_response(render_template('index.html', status='login sucess'))
    resp.set_cookie('userID', user)

    return resp


@app.route('/get_cookie')
def getcookie():
    name = request.cookies.get('userID')
    return '<h1>welcome ' + name + '</h1>'


@app.route("/delete_cookie")
def delete_cookie():
    """
    删除cookie，通过delete_cookie()的方式，里面是cookie的名字
    这里的删除只是让cookie过期，并不是直接删除cookie
    """
    resp = make_response("del success")
    resp.delete_cookie("userID")


def send_post(name):
    # 构造数据
    res = {
        'eid': '20180601',
        'type': None,
        'name': name,
        'tid': name
    }

    if res is not None:
        eid = res.get('eid')
        year = eid[0:4]
        month = eid[4:6]
        dict = {}
        dict['date'] = year + "年" + month + "月"
        dict['name'] = res.get('name')
        dict['code'] = res.get('tid')
        lista = []
        lista.append(dict)
        return render_template('search.html', nums=lista)
    elif res is None:
        return render_template('search.html', tips=name + ",很抱歉，您本期未中签！")
    # return "<h3>"+json.dumps(name)+"</h3>"  # 另起一个网页返回


@app.route('/search', methods=['POST', 'GET'])
def search():
    """
    搜索接口，在搜索框中填入相关内容， 然后返回计算的结果
    :return:
    """
    if request.method == 'POST':
        name = request.form['username'].strip()  # strip去除前后空格
    else:
        name = request.args.get('username')

    if name:
        return send_post(name)
    else:
        return render_template('search.html', tips="请输入正确的姓名或编码")


if __name__ == '__main__':
    app.run(debug=True)
