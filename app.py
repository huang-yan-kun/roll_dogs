from core import create_app

# 创建实例
app = create_app()

if __name__ == '__main__':
    print("Rolldogs 卷狗管理程序正在啟動...")
    print("---------------------------------------")
    print(f"数据库路径（SQLite）：[您的根目录]/instance/rolldogs.db")
    print("请访问：http://127.0.0.1:5000/")
    print("---------------------------------------")
    app.run(debug=True)