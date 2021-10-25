import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from stocks import data
import random
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
db = SQLAlchemy(app)


# Create DB model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    last = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return 'Name %r' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users', methods=['GET', 'POST'])
def users():
    mydata = User.query.all()
    return render_template('users.html', mydata=mydata)


@app.route('/stocks', methods=['GET', 'POST'])
def stocks():
    r1 = random.randint(0, 495)
    token = 'Tsk_1c42cee11b834d83b84aec96ae542f1a'
    stock_data = []
    for ticker in data[r1: r1+10]:
        api_url = f'https://sandbox.iexapis.com/stable/stock/{ticker}/quote/?token={token}'
        ## Transform the data as a json object
        stock = requests.get(api_url).json()
        stock_data.append(stock)

    return render_template('stocks.html', stock_data=stock_data)


@app.route('/about-me', methods=['GET', 'POST'])
def about_me():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['name']
        user_last = request.form['last']
        user_email = request.form['email']
        new_user = User(name=user_name, last=user_last, email=user_email)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('users'))
        except:
            return 'There was an error adding your friend.'
    else:
        return render_template('register.html')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user_to_update = User.query.get_or_404(id)
    print(user_to_update.name, user_to_update.last)
    if request.method == 'POST':
        print('POST IS WORKING')
        user_to_update.name = request.form['name']
        user_to_update.last = request.form['last']
        user_to_update.email = request.form['email']
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
