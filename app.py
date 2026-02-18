from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from extensions import db, login_manager
from models import User, Post, Comment
from forms import LoginForm, RegistrationForm, PostForm, CommentForm
from flask_login import login_user, logout_user, login_required, current_user

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Routes
    @app.route('/')
    def home():
        posts = Post.query.order_by(Post.date_posted.desc()).all()
        return render_template('home.html', posts=posts)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email already registered. Try logging in.', 'danger')
                return redirect(url_for('login'))
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created! You can now log in.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                flash('Logged in successfully!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login failed. Check email and password.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).all()
        return render_template('dashboard.html', posts=posts)

    @app.route('/create_post', methods=['GET', 'POST'])
    @login_required
    def create_post():
        form = PostForm()
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', 'success')
            return redirect(url_for('home'))
        return render_template('create_post.html', form=form)

    @app.route('/post/<int:post_id>')
    def post_detail(post_id):
        post = Post.query.get_or_404(post_id)
        form = CommentForm()
        return render_template('post_detail.html', post=post, form=form)

    @app.route('/post/<int:post_id>/comment', methods=['POST'])
    @login_required
    def add_comment(post_id):
        post = Post.query.get_or_404(post_id)
        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(content=form.content.data, author=current_user, post=post)
            db.session.add(comment)
            db.session.commit()
            flash('Comment added!', 'success')
        return redirect(url_for('post_detail', post_id=post_id))

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
