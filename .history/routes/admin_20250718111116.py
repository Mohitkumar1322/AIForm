from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import User, Form
from app import db
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    forms = Form.query.all()
    return render_template('dashboard.html', forms=forms)

@admin_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_form():
    if request.method == 'POST':
        title = request.form['title']
        fields = json.dumps(request.form.getlist('fields'))
        new_form = Form(title=title, fields=fields)
        db.session.add(new_form)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    return render_template('create_form.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))
