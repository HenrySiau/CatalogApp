from models import User
from database import db_session
users = User.query.all()
new_user = User(name='Henry', email='henry@gmail.com')
db_session.add(new_user)
try:
    db_session.commit()
except:
    print('can not add new user')