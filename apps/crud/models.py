from apps.app import db
 
class GarbageRecord(db.Model):
    __tablename__ = "garbage_record"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    garbage_code = db.Column(db.String)
    amount = db.Column(db.String)
    date = db.Column(db.Date)
    
class Garbage(db.Model):
    __tablename__ = "garbage"
    garbage_code = db.Column(db.Integer,primary_key=True,autoincrement=True)
    type = db.Column(db.String)