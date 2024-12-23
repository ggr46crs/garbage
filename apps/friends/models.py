from apps.app import db

class Friends(db.Model):
    __tablename__ = "friends"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    friend_id = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    recipient = db.Column(db.Integer)
    room_ID = db.Column(db.String)