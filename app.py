from models import app, db, User, Stocks
from flask import render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, StocksForm
from stocks import data
import requests
import random


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users', methods=['GET', 'POST'])
def users():
    mydata = User.query.all()
    return render_template('users.html', mydata=mydata)


@app.route('/stocks', methods=['GET', 'POST'])
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
        stock_data = Stocks.query.filter(Stocks.symbol.contains(q))
    else:
        stock_data = Stocks.query.all()

    return render_template('stocks.html', stock_data=stock_data)


@app.route('/about-me', methods=['GET', 'POST'])
def about_me():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(name=form.name.data, last=form.last.data,
                        email=form.email.datam, budget=form.budget.data)
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
def delete(id):
    user_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_delete)
        db.session.commit()
        return redirect(url_for('users'))
    except:
        return 'There was an error deleting your friend'


@app.route('/coming-soon')
def coming_soon():
	return render_template('soon.html')


if __name__ == '__main__':
    app.run(debug=True)
    app.run(debug=True)
