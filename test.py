from app import db, User

user = User.query.get_or_404(3)
print(user.name, user.last)

user.last = 'Cena'
db.session.commit()
print(user.name, user.last)
