from apps.app import db
from sqlalchemy import func
from datetime import datetime
class Chat(db.Model):
    __tablename__ = "chat"
    id = db.Column(db.Integer, primary_key=True)
    send = db.Column(db.Integer)
    receive = db.Column(db.Integer)
    comment = db.Column(db.String)
    data = db.Column(db.TIMESTAMP,default=lambda: datetime.now().replace(microsecond=0))