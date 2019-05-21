from flask import Flask, render_template, request, session, redirect, url_for
from http.cookies import SimpleCookie
from bs4 import BeautifulSoup
import requests
import base64

from config import secret_key

app = Flask(__name__)
app.secret_key = secret_key


@app.route('/fuck', methods=['GET', 'POST'])
def fuck():
    if request.method == 'POST':
        # session['username'] = request.form['username']
        # session['password'] = request.form['password']
        # session['validateCode'] = request.form['validateCode']
        cookie_string = session['cookie']
        cookie = SimpleCookie()
        cookie.load(cookie_string)
        cookies = {}
        for key, morsel in cookie.items():
            cookies[key] = morsel.value
        username = request.form['username']
        password = request.form['password']
        validcode = request.form['validateCode']
        r = requests.post('http://elite.nju.edu.cn/jiaowu/login.do',
                          data={'userName': username, 'password': password, 'ValidateCode': validcode},
                          cookies=cookies)
        print(r.content.decode('utf-8'))

        r = requests.get('http://elite.nju.edu.cn/jiaowu/student/evalcourse/courseEval.do?method=currentEvalCourse',
                         cookies=cookies)
        soup = BeautifulSoup(r.content, 'lxml')
        trs = soup.find_all('tr')
        trs.remove(trs[0])

        # 获取没评的课并打分
        for tr in trs:
            if not tr.contents[9].has_attr('id'):
                continue
            code = tr.contents[9].attrs['id'][2:]
            r = requests.post('http://elite.nju.edu.cn/jiaowu/student/evalcourse/courseEval.do',
                              data={'method': 'currentEvalItem', 'id': code}, cookies=cookies)
            tmpSoup = BeautifulSoup(r.content, 'lxml')

            # 获取课程一共需要评价几道题
            question = tmpSoup.find('input', type='hidden')
            questionNum = int(question.attrs['value'])

            # 组装数据
            data = {'question': str(questionNum), 'mulItem1': '1', 'mulItem': ' 1', 'sub': '提   交'}
            for i in range(questionNum):
                data['question' + str(i + 1)] = '5'

            # 发送评价post
            r = requests.post('http://elite.nju.edu.cn/jiaowu/student/evalcourse/courseEval.do?method=submitEval',
                              data=data, cookies=cookies)

        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/')
def index():
    # return 'Hello, World!'
    r = requests.get('http://elite.nju.edu.cn/jiaowu/ValidateCode.jsp')
    cookie_string = "; ".join([str(x) + "=" + str(y) for x, y in r.cookies.items()])
    base64_data = base64.b64encode(r.content).decode("utf-8")
    base64_data = "data:image/png;base64," + base64_data
    print(cookie_string)
    print(base64_data)
    session['cookie'] = cookie_string
    return render_template('index.html', validatepic=base64_data)


if __name__ == '__main__':
    app.run()
