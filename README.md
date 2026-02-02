# 🐕 Rolldogs 学生管理系统 v1.0

这是 Rolldogs 项目的第一个正式版本！我们已经完成了从后端逻辑到前端 UI 的完整打通。

# 🚀 v1.0 已实现功能

核心架构：基于 Flask 蓝图 (Blueprint) 的模块化设计，代码结构清晰。

数据库集成：使用 SQLAlchemy 实现对学生信息（姓名、学号、班级）的持久化存储。

动态 UI：基于 Tailwind CSS 构建的响应式看板，支持不同设备访问。

CRUD 基础：支持手动录入学生数据及“一键随机抓捕”生成测试数据。

🛠️ 技术清单

后端：Python 3.x / Flask

数据库：Flask-SQLAlchemy (SQLite)

前端：Tailwind CSS

📸 运行预览

安装依赖：

# 根据 environment.yml 创建环境
conda env create -f environment.yml

# 激活环境
conda activate my_flask


启动应用：

python app.py


访问页面：

打开浏览器访问 http://127.0.0.1:5000 即可查看学生列表。

记录每一只努力奋斗的卷狗。