from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from .models import Student
from .db import db
import random

bp = Blueprint('main', __name__, template_folder='templates')


@bp.route('/')
def index():
    """首页：学生列表"""
    try:
        students = db.session.execute(select(Student)).scalars().all()
        return render_template('index.html', title="Rolldogs 卷王观测站", students=students)
    except Exception as e:
        return f"数据库查询失败: {str(e)}", 500


@bp.route('/add', methods=['GET', 'POST'])
def add_student():
    """录入新同学"""
    if request.method == 'POST':
        name = request.form.get('name')
        s_id = request.form.get('student_id')
        class_name = request.form.get('class_name')
        title = request.form.get('title')

        if not name or not s_id:
            flash('姓名和学号是必填项！', 'error')
            return redirect(url_for('main.add_student'))

        try:
            new_student = Student(
                student_id=s_id,
                name=name,
                class_name=class_name,
                title=title
            )
            db.session.add(new_student)
            db.session.commit()
            flash(f'成功录入: {name}', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'录入失败: 学号可能已存在', 'error')

    return render_template('add.html')


@bp.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_student(id):
    """编辑同学信息"""
    student = db.session.get(Student, id)
    if not student:
        flash('未找到该同学', 'error')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        student.name = request.form.get('name')
        student.class_name = request.form.get('class_name')
        student.title = request.form.get('title')

        try:
            db.session.commit()
            flash('修改成功', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('修改失败', 'error')

    return render_template('edit.html', student=student)


@bp.route('/delete/<string:id>', methods=['POST'])
def delete_student(id):
    """删除记录（视奸终结）"""
    student = db.session.get(Student, id)
    if student:
        try:
            db.session.delete(student)
            db.session.commit()
            flash('记录已销毁', 'success')
        except Exception as e:
            db.session.rollback()
            flash('销毁失败', 'error')
    return redirect(url_for('main.index'))


@bp.route('/add_test_student')
def add_test_student():
    """随机生成卷狗"""
    try:
        test_id = f'ID-{random.randint(1000, 9999)}'
        titles = ['半夜修仙者', 'LeetCode 刷题机器', '图书馆钉子户', '由于太卷被开除班籍']
        new_student = Student(
            student_id=test_id,
            name=f'卷王{random.randint(1, 100)}号',
            class_name='秘密研究班',
            title=random.choice(titles)
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('main.index'))
    except Exception as e:
        db.session.rollback()
        return f"投喂失败: {str(e)}", 500