from app import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
