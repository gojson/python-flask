#encoding: utf-8

from flask_script import Manager                                  #终端命令
from flask_migrate import Migrate,MigrateCommand                  #迁移表
from company import app
from exts import db
from models import User,Question
#1.0 添加应用到终端命令
manager = Manager(app)

#2.0 使用migrate 绑定app 和 db
migrate = Migrate(app,db)

#3.0 添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()
