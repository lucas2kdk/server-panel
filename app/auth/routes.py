"""
Authentication routes for login, registration, and logout.
"""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth
from app.models import db, User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('servers.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)

        # Validation
        if not email or not password:
            flash('Please provide email and password.', 'error')
            return render_template('auth/login.html')

        # Find user
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'Welcome back, {email}!', 'success')

            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('servers.dashboard'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('auth/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('servers.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')

        # Validation
        if not email or not password:
            flash('Please provide email and password.', 'error')
            return render_template('auth/register.html')

        if password != password_confirm:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('auth/register.html')

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('auth.register'))

        # Create new user
        try:
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('auth/register.html')

    return render_template('auth/register.html')


@auth.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
