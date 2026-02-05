from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from .models import Student, Power, StudentPower
from .db import db
import random

bp = Blueprint('main', __name__, template_folder='templates')


@bp.route('/')
def index():
    """首页：展示所有卷王卡片"""
    try:
        students = db.session.execute(select(Student)).scalars().all()
        return render_template('index.html', title="卷王观测站", students=students)
    except Exception as e:
        return f"数据库查询失败: {str(e)}", 500


@bp.route('/add', methods=['GET', 'POST'])
def add_student():
    """录入新同学（仅基本信息）"""
    if request.method == 'POST':
        s_id = request.form.get('student_id')
        name = request.form.get('name')
        class_name = request.form.get('class_name')

        if s_id and name:
            # 检查是否已存在
            existing = db.session.get(Student, s_id)
            if existing:
                flash("学号已存在，请勿重复录入", "error")
                return redirect(url_for('main.add_student'))

            new_student = Student(student_id=s_id, name=name, class_name=class_name)
            db.session.add(new_student)
            db.session.commit()
            flash(f"欢迎新卷王 {name} 加入！", "success")
            return redirect(url_for('main.index'))
        flash("请填写完整信息", "error")
    return render_template('add_student.html')


@bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit_student(id):
    """
    核心整合路由：
    1. GET: 渲染编辑页（包含基本信息、高级画像、技能管理三个 Tab）
    2. POST: 根据 action 处理不同的板块更新
    """
    student = db.session.get(Student, id)
    if not student:
        flash("找不到该同学", "error")
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        action = request.form.get('action')

        # 板块 1: 更新基本信息
        if action == 'update_basic':
            student.name = request.form.get('name')
            student.class_name = request.form.get('class_name')
            db.session.commit()
            flash("基本资料已同步", "success")

        # 板块 2: 更新高级画像 (头衔与金句)
        elif action == 'update_advanced':
            student.title = request.form.get('title')
            student.praice_sentence = request.form.get('praice_sentence')
            db.session.commit()
            flash("卷王画像已更新", "success")

        # 板块 3: 录入新技能
        elif action == 'add_skill':
            power_id = request.form.get('power_id')
            custom_name = request.form.get('custom_power_name')
            level = request.form.get('level', '50')

            # 处理自定义技能名
            if custom_name:
                existing_p = db.session.execute(select(Power).where(Power.power_name == custom_name)).scalar()
                if not existing_p:
                    p_id = f"P{random.randint(100, 999)}"
                    existing_p = Power(power_id=p_id, power_name=custom_name)
                    db.session.add(existing_p)
                    db.session.commit()
                power_id = existing_p.power_id

            if power_id:
                new_sp = StudentPower(student_id=id, power_id=power_id, level=level)
                db.session.merge(new_sp)  # 使用 merge 防止重复添加相同技能报错
                db.session.commit()
                flash("技能点 +1", "success")

        # 提交后通过 URL 参数告诉前端停留在哪个 Tab
        active_tab = request.form.get('active_tab', 'basic')
        return redirect(url_for('main.edit_student', id=id, tab=active_tab))

    all_powers = db.session.execute(select(Power)).scalars().all()
    return render_template('edit.html', student=student, all_powers=all_powers)


@bp.route('/delete/<id>', methods=['POST'])
def delete_student(id):
    """彻底抹除卷王记录"""
    student = db.session.get(Student, id)
    if student:
        db.session.delete(student)
        db.session.commit()
        flash("该同学已从监控名单中移除", "success")
    return redirect(url_for('main.index'))


@bp.route('/delete_skill/<s_id>/<p_id>')
def delete_skill(s_id, p_id):
    """删除某项特定技能"""
    sp = db.session.get(StudentPower, (s_id, p_id))
    if sp:
        db.session.delete(sp)
        db.session.commit()
        flash("技能已重置", "success")
    return redirect(url_for('main.edit_student', id=s_id, tab='skills'))