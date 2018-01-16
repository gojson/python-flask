# python-flask
flask web project

```
p install virtualenv
2.0 指定virtualenv 使用的python 版本号
Virtualenv -p /usr/local/bin/python ven3.6.6


1.0 创建项目目录
Mkdir project
Cd project
git clone http://github.com/mitsuhiko/flask.git

2.0 创建虚拟环境
Virtualenv -p /usr/local/bin/python ven3.6.6

3.0 激活环境
source /Virtualenv/ven3.6.6/bin/activate

4.0 安装 Flask sqlalchemy
 (1) pip install Flask
 (2) pip install flask-sqlalchemy

5.0 pycharm 配置
 (1) pycharm -> preferences -> project ->project-interpreter ->右键齿轮 add-local ->ok
 (2) run server




1.0 Mysql 数据库安装：
https://dev.mysql.com/downloads/mysql/

2.0 mysql-python 中间件安装
 (1) 切换虚拟环境
    Source virtualenv/bin/activate
 (2) pip install python-mysql  (支持python2.7)
     或者
    Pip install pymysql  (支持python3)
 (3) 配置数据库
    config.py

Config.py
#encoding: utf-8

DEBUG = True
#SECRET_KEY

#SQLALCHEMY_DB
#dialet+driver://username:password@host:post/database
DIALET = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'cyl17600109104'
HOST = '127.0.0.1'
PORT = '3306'
DB_NAME = 'py_mysql'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALET,DRIVER,USERNAME,PASSWORD,HOST,PORT,DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = True

创建数据库Model.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
# db.create_all()

db = SQLAlchemy(app)

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)

class Role(db.Model):
 # 定义表名
 __tablename__ = 'roles'
 # 定义列对象
 id = db.Column(db.Integer, primary_key=True)
 name = db.Column(db.String(64), unique=True)
 user = db.relationship('User', backref='role')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

db.create_all()

if __name__ == '__main__':
    app.run()export PATH="$PATH":/usr/local/mysql/bin
```

## 开发步骤
```
Cdn 引入 jquery
http://www.bootcdn.cn/

Bootstrapt
Css
js


1.0 创建虚拟环境
Pycharm ->preference ->project -> addlocal -> ‘Virtualenv/venv3.6.6’ ->OK
Source  Virtualenv/venv3.6.6/bin/activate

2.0 pip install flask
3.0 pip install flask_script
4.0 pip install flask_migrate
5.0 pip install pymysql
6.0 pip install jinja2
7.0 pip install flask_sqlalchemy 



1. 切换虚拟环境,创建项目company
2. Config.py 添加配置
3. 初始化配置
4. 创建exts.py
5. Manage.py
6. Models.py

Exts.py
#encoding: utf-8

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


Manage.py
#encoding: utf-8

from flask_script import Manager                                  #终端命令
from flask_migrate import Migrate,MigrateCommand                  #迁移表
from company import app
from exts import db
from models import User
#1.0 添加应用到终端命令
manager = Manager(app)

#2.0 使用migrate 绑定app 和 db
migrate = Migrate(app,db)

#3.0 添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()




Model.py
#encoding: utf-8

#供模型使用 db.Model
from exts import db

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tel = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(32),nullable=False)
    pwd = db.Column(db.String(100),nullable=False)
    created_at = db.Column(db.DateTime,nullable=False)


#生成迁移文件和数据表
python manage.py db init          #初始化迁移环境
python manage.py db migrate       #生成迁移文件
python manage.py db upgrade       #迁移文件映射到数据表


Models.py
#初始化项目
from flask import Flask
app = Flask(__name__)

#from flask_sqlalchemy import SQLAlchemy
from exts import db

from db_model import Article,User,Role

#引入配置文件
import config

#导入数据库配置
app.config.from_object(config)
#应用数据库
# db = SQLAlchemy(app)
db.init_app(app)


#添加文章
@app.route('/addArticle')
def addArticle():
    ar1 = Article(title='测试4',content='内容4')
    db.session.add(ar1)
    db.session.commit()
    return "hello"

#查找文章
@app.route('/findArticle')
def findArticle():
    #1.0 找到文章
    result = Article.query.filter(Article.title == '测试2').first()
    print (result.title,result.content)
    return "find"

#更新文章
@app.route('/updateArticle')
def updateArticle():
    #1.0 找到文章
    up = Article.query.filter(Article.title =='测试1').first()
    #2.0 修改文章
    up.title='测试1'
    up.content = '内容1'
    #3.0 提交
    db.session.commit()
    return "update"

#删除文章
@app.route('/delArticle')
def delArticle():
    #1.0 查到文章
    ar1 = Article.query.filter(Article.title == '测试1').first()
    db.session.delete(ar1)
    db.session.commit()
    return 'del'


#新增用户user
@app.route('/addUser/<name>')
def addUser(name):
    user1 = User(username = name)
    db.session.add(user1)
    db.session.commit()
    return name

if __name__ == '__main__':
    app.run()



#分开models :让代码方便管理
#解决代码循环引用问题：把db放在一个单独文件exts,model引入exts, controller 引入exts并初始化db.init_app(app)

Script.py
#encoding: utf-8

from flask_script import Manager

DBmanager = Manager()

@DBmanager.command
def init():
    print ('数据库初始化')

@DBmanager.command
def migrate():
    print ('数据库迁移成功')

```

## 登录限制
```

#-*- encoding:utf-8 -*-

from functools import wraps
from flask import session
from flask import redirect,url_for

#登录限制
def login_required(func):
    @wraps(func)
    def wapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wapper



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
```
