from models import db, User
import json

with open('user_data.json') as file:
    data = json.load(file)
    for entry in data[:100]:
        new_user = User(username=entry['username'], password=entry['password'], name=entry['first_name'], last=entry['last_name'],
                        email=entry['email'], budget=entry['budget'])
        db.session.add(new_user)
    db.session.commit()

# User.query.delete()
# db.session.commit()
