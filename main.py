import requests
from skimage import io
from io import BytesIO
from bs4 import BeautifulSoup

# 模拟进入主页
s = requests.Session()
s.get('http://elite.nju.edu.cn/jiaowu')

# 读取验证码
r = s.get('http://elite.nju.edu.cn/jiaowu/ValidateCode.jsp')
image = io.imread(BytesIO(r.content))
io.imshow(image)
io.show()

# 获取用户名，密码
username = input('用户名：')
password = input('密码： ')
# username = 
# password = 
validcode = input('验证码: ')

# 模拟登陆
r = s.post('http://elite.nju.edu.cn/jiaowu/login.do', data = {'userName':username, 'password': password, 'ValidateCode': validcode})
r = s.get('http://elite.nju.edu.cn/jiaowu/student/evalcourse/courseEval.do?method=currentEvalCourse')
soup = BeautifulSoup(r.content, 'lxml')
trs = soup.find_all('tr')
trs.remove(trs[0])

# 获取没评的课并打分
for tr in trs:
    if not tr.contents[9].has_attr('id'):
        continue
    code=tr.contents[9].attrs['id'][2:]
    r = s.post('http://elite.nju.edu.cn/jiaowu/student/evalcourse/courseEval.do', data = {'method': 'currentEvalItem', 'id': code})
    tmpSoup = BeautifulSoup(r.content, 'lxml')
    
    # 获取课程一共需要评价几道题
    question = tmpSoup.find('input', type='hidden')
    questionNum = int(question.attrs['value'])
    
    # 组装数据
    data = {'question': str(questionNum), 'mulItem1': '1', 'mulItem': ' 1', 'sub': '提   交'}
    for i in range(questionNum):
        data['question'+str(i+1)] = '5'
        
    # 发送评价post
    r = s.post('http://elite.nju.edu.cn/jiaowu/student/evalcourse/courseEval.do?method=submitEval', data = data)