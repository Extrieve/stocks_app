from models import db, User
import json

with open('user_datajson.json') as file:
    data = json.load(file)
    for entry in data:
        new_user = User(name=entry['first_name'], last=entry['last_name'],
                        email=entry['email'], budget=entry['budget'])
        db.session.add(new_user)
    db.session.commit()
