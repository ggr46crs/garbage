from apps.app import db

class Chat(db.Model):
    __tablename__ = "chat"
    id = db.Column(db.Integer, primary_key=True)
    send = db.Column(db.String)
    receive = db.Column(db.String)
    comment = db.Column(db.String)
    data = db.Column(db.TIMESTAMP)
