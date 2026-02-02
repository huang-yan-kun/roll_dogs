from .db import db

# 1. 学生主表
class Student(db.Model):
    __tablename__ = 'roll_dog'

    # 这里的变量名是 student_id
    student_id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    # 添加缺失的 class_name 字段，否则 routes.py 传入会报错
    class_name = db.Column(db.String(50))
    title = db.Column(db.String(100))
    praice_sentence = db.Column(db.String(100))

    # 关联关系
    birth_info = db.relationship('Birth', backref='student', uselist=False, cascade="all, delete-orphan")
    skills = db.relationship('StudentPower', backref='student', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Student {self.name} ({self.student_id})>'

# 2. 生日表
class Birth(db.Model):
    __tablename__ = 'birth'

    bir_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_id = db.Column(db.String(10), db.ForeignKey('roll_dog.student_id'), nullable=False)
    date = db.Column(db.Date)


# 3. 技能主表
class Power(db.Model):
    __tablename__ = 'power'

    power_id = db.Column(db.String(4), primary_key=True)
    power_name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Power {self.power_name}>'


# 4. 学生技能关联表
class StudentPower(db.Model):
    __tablename__ = 's_power'

    student_id = db.Column(db.String(10), db.ForeignKey('roll_dog.student_id'), primary_key=True)
    power_id = db.Column(db.String(4), db.ForeignKey('power.power_id'), primary_key=True)
    level = db.Column(db.String(10))

    # 关联到技能详情
    power_info = db.relationship('Power')