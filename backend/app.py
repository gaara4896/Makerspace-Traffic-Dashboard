import os

from flask import Flask, request, jsonify
from flask_script import Manager, Server
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import random

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(project_dir, "traffic.db"))
db = SQLAlchemy(app)
app.app_context().push()
manager = Manager(app)
manager.add_command("runserver", Server(host='0.0.0.0'))


class Traffic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.now())
    traffic_count = db.Column(db.Integer, nullable=False)

    def __init__(self, traffic_count):
        self.traffic_count = traffic_count

    def __repr__(self):
        return '<User %r>' % self.username


@manager.command
def initdb():
    db.drop_all()
    db.create_all()


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        traffics = db.session.query(Traffic).order_by(desc(Traffic.date_created)).limit(30).all()
        json = []
        for traffic in traffics:
            json.append({"date": traffic.date_created.strftime("%s"), "traffic": traffic.traffic_count})
        return jsonify(json)
    elif request.method == 'POST':
        json = request.json
        db.session.add(Traffic(json["traffic"]))
        db.session.commit()
        return "ok"


if __name__ == '__main__':
    manager.run()
