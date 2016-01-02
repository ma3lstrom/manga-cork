import logging

from flask import render_template, request, redirect, url_for
from flask.ext.login import (login_user, logout_user, current_user,
                             login_required)

from . import app, db, login_manager
from .utils import (increment_page_number, build_img_path, is_last_page)
from .models import LastPage, Comments, User
from .forms import RegistrationForm, LoginForm

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

INDEX_CHAPTER = 'dragonball_ch1'
INDEX_PAGE = 'ndragon_ball_v001-000'
LAST_PAGE_LIST = [i.lastpage for i in LastPage.query.all()]
logger.debug('Last Page List {}'.format(LAST_PAGE_LIST))

# Reloads user ID in session
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return redirect(url_for('display',chapter=INDEX_CHAPTER, page=INDEX_PAGE))


@app.route('/<chapter>/<page>')
def display(chapter, page):
    form = LoginForm()
    image_path = build_img_path(chapter, page)
    next_page_number = increment_page_number(page)
    comments = Comments.query.order_by(Comments.id.desc()).filter_by(
                image_path=image_path).all()

    if (is_last_page(page, LAST_PAGE_LIST)):
        next_page = '/last_page'
    else:
        next_page = build_img_path(chapter, next_page_number)

    return render_template('manga.html',form=form, next_page=next_page,
                           image_path=image_path, comments=comments)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('login'))


@app.route('/login', methods = ['GET','POST'])
@login_manager.user_loader
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check pwd and log user in

        # [...]
        return redirect(url_for('index'))
    # form has not been submitted (GET request)
    # therefore render login page
    return render_template('login.html', form=form)


@app.route('/add', methods= ['POST'])
@login_required
def add_entry():
    image_path = request.form['image_path']
    comment = request.form['post_text']
    _, chapter, page  = image_path.split('/')

    new_comment = Comments(comment, image_path)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for('display', chapter=chapter, page=page ))

@app.route('/last_page')
def display_lastpage():
    return render_template('lastpage.html')
