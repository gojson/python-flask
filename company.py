#encoding: utf-8

from flask import Flask,render_template,request,redirect,url_for,session
import config
app = Flask(__name__)
app.config.from_object(config)  #链接数据库

#引入数据库
from exts import db
db.init_app(app)

#引入model
from models import User,Question

#日期处理
from datetime import datetime

#登录限制
from decorators import login_required


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/index')
def index():
    context = {
        "questions":Question.query.order_by('-created_at').all()
    }
    return render_template('index.html',**context)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    else:
        tel = request.form.get('tel')
        pwd = request.form.get('pwd')
        user = User.query.filter(User.tel==tel,User.pwd==pwd).first()
        if user:
            session['user_id'] = user.id
            #31天内免登陆
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u"手机号或密码错误"

@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')
    else:
        tel = request.form.get('tel')
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        repwd = request.form.get('repwd')
        #1.0 手机号码验证：
        user = User.query.filter(User.tel==tel).first()
        if user:
            return u"该手机号码已经被注册"
        elif len(tel) != 11:
            return u"请输入正确的手机号码"
        else:
            #密码和确认密码校验
            if pwd != repwd:
                return u"密码和确认密码不一致"
            else:
                user = User(tel=tel,username=username,pwd=pwd,created_at=datetime.now())
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
        return 'post register'


@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question/question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get("user_id")
        user = User.query.filter(User.id==user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<int:question_id>')
def detail(question_id):
    info = Question.query.filter(Question.id == question_id).first()
    return render_template('question/detail.html',info=info)



#退出登录
@app.route('/logout/')
def logout():
    session.clear()
    return render_template('user/login.html')



if __name__ == '__main__':
    app.run(debug=True)
