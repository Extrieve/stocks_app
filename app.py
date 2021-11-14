from models import app, db, User, Stocks
from flask import render_template, request, redirect, url_for, flash
from forms import RegisterForm, StocksForm, LoginForm
from flask_login import login_user, logout_user, login_required
import requests
import random


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    q = request.args.get('q')

    if q:
        user_data = User.query.filter(
            User.name.contains(q) | User.last.contains(q) | User.email.contains(q) | User.id.contains(q))
    else:
        user_data = User.query.all()

    return render_template('users.html', mydata=user_data)


@app.route('/stocks', methods=['GET', 'POST'])
@login_required
def stocks():
    # r1 = random.randint(0, 495)
    # token = 'Tsk_1c42cee11b834d83b84aec96ae542f1a'
    # stock_data = []
    # for ticker in data[r1: r1+10]:
    #     api_url = f'https://sandbox.iexapis.com/stable/stock/{ticker}/quote/?token={token}'
    #     ## Transform the data as a json object
    #     stock = requests.get(api_url).json()
    #     stock_data.append(stock)
    q = request.args.get('q')

    if q:
        stock_data = Stocks.query.filter(
            Stocks.name.contains(q) | Stocks.symbol.contains(q))
    else:
        stock_data = Stocks.query.all()

    return render_template('stocks.html', stock_data=stock_data)


@app.route('/about-me', methods=['GET', 'POST'])
@login_required
def about_me():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password1.data, name=form.name.data, last=form.last.data,
                        email=form.email.data, budget=form.budget.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users'))

    if form.errors != {}:  # if no errors found
        for err_msg in form.errors.values():
            flash(f'There was an error: {err_msg}', category='danger')
    # if request.method == 'POST':
    #     user_name = request.form['name']
    #     user_last = request.form['last']
    #     user_email = request.form['email']
    #     budget = request.form['budget']
    #     new_user = User(name=user_name, last=user_last,
    #                     email=user_email, budget=budget)
    #     try:
    #         db.session.add(new_user)
    #         db.session.commit()
    #         return redirect(url_for('users'))
    #     except:
    #         return 'There was an error adding your friend.'

    return render_template('register.html', form=form)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    user_to_update = User.query.get_or_404(id)
    if request.method == 'POST':
        user_to_update.name = request.form['name']
        user_to_update.last = request.form['last']
        user_to_update.email = request.form['email']
        user_to_update.budget = request.form['budget']
        try:
            db.session.commit()
            return redirect(url_for('users'))
        except:
            return 'There was an error updating your record'
    else:
        return render_template('update.html', user_to_update=user_to_update)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    user_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_delete)
        db.session.commit()
        return redirect(url_for('users'))
    except:
        return 'There was an error deleting your friend'


@app.route('/coming-soon')
@login_required
def coming_soon():
	return render_template('soon.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(
                f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('users'))
        else:
            flash('Username/password mismatch!', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('Successfully logged out!', category='info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
