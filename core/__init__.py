import os
from flask import Flask
from .db import db
from flask_sqlalchemy import SQLAlchemy

def create_app(test_config=None):
    # 初始化 Flask
    app = Flask(__name__)

    #载入config配置
    app.config.from_object('config.DevelopmentConfig')

    #初始化并绑定
    db.init_app(app)

    from . import models
    from . import routes

    app.register_blueprint(routes.bp)

    #确保instance存在
    try:
        instance_path = os.path.join(os.path.dirname(app.root_path), 'instance')
        os.makedirs(instance_path, exist_ok=True)
    except OSError:
        pass

    # 注册模型和路由
    with app.app_context():
        # 创建所有资料表
        db.create_all()

    return app