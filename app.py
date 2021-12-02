from models import app, db, User, Stocks, Portfolios
from flask import render_template, request, redirect, url_for, flash
from forms import RegisterForm, StocksForm, LoginForm,  PurchaseItemForm, FriendRequestForm
from flask_login import login_user, logout_user, login_required, current_user
import requests
import random


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users', methods=['GET', 'POST'])
def users():
    user_form = FriendRequestForm()
    q = request.args.get('q')

    if q:
        user_data = User.query.filter(
            User.name.contains(q) | User.last.contains(q) | User.email.contains(q) | User.id.contains(q))
    else:
        user_data = User.query.all()

    if request.method == 'POST':
        add_user = request.form.get('add_user')
        flash(
            f"Congratulations you've added {add_user}!", category='success')

    return render_template('users.html', mydata=user_data, user_form=user_form)


@app.route('/stocks', methods=['GET', 'POST'])
def stocks():
    purchase_form = PurchaseItemForm()
    q = request.args.get('q')

    if q:
        stock_data = Stocks.query.filter(
            Stocks.name.contains(q) | Stocks.symbol.contains(q))
    else:
        stock_data = Stocks.query.all()

    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_stock_object = Stocks.query.filter_by(name=purchased_item).first()
        if p_stock_object:
            if current_user.budget > p_stock_object.latest_price:
                new_entry = Portfolios(
                    name=p_stock_object.name, symbol=p_stock_object.symbol, user_id=current_user.id, price=p_stock_object.latest_price)
                current_user.budget -= p_stock_object.latest_price
                db.session.add(new_entry)
                db.session.commit()
                flash(
                    f"Congratulations! You purchased {p_stock_object.name} for {p_stock_object.latest_price}$", category='success')
                return redirect(url_for('portfolios', id=current_user.id))
            else:
                flash(
                    f"Unfortunately, you don't have enough money to purchase {p_stock_object.name}!", category='danger')

    return render_template('stocks.html', stock_data=stock_data, purchase_form=purchase_form)


@app.route('/portfolio/<int:id>', methods=['GET', 'POST'])
@login_required
def portfolios(id):
    my_stocks = Portfolios.query.filter_by(user_id=id)
    return render_template('portfolios.html', stocks=my_stocks)


@app.route('/about-me', methods=['GET', 'POST'])
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
        login_user(new_user)
        flash(
            f'Account Created successfully! You are now logged in as: {new_user.username}', category='success')
        return redirect(url_for('users'))

    if form.errors != {}:  # if no errors found
        for err_msg in form.errors.values():
            flash(f'There was an error: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    user_to_update = User.query.get_or_404(id)
    if request.method == 'POST':
        user_to_update.username = request.form['username']
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


@app.route('/info/<string:symbol>', methods=['GET', 'POST'])
def more_info(symbol):
    token = 'Tsk_1c42cee11b834d83b84aec96ae542f1a'
    api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/chart/20200415?token={token}'
    historical_data = requests.get(api_url).json()
    labels = [item['date'] for item in historical_data]
    data = [item['close'] for item in historical_data]
    stock = Stocks.query.get(symbol)
    color = "#872027" if data[0] > data[-1] else '#11992c'
    # color = "green" if data[0] < data[-1] else 'red'
    return render_template('info.html', labels=labels, data=data, symbol=symbol, name=stock.name, color=color)


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


@app.route('/dummy')
def dummy():
    return render_template('dummy.html')


if __name__ == '__main__':
    app.run(debug=True)
