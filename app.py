from flask import Flask
from application.database import db
app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'edine-secret-key'
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///e-dine.sqlite3'
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()

from application.controllers import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        manager = User.query.filter_by(role = 'manager').first()
        if manager is None:
            manager = User(username = 'Rounak', email = 'rounak16112006@gmail.com', password = '12345', role = 'manager')
            db.session.add(manager)
            db.session.commit()
    app.run()