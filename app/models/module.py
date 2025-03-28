from app import db

classe_module = db.Table('classe_module',
    db.Column('classe_id', db.Integer, db.ForeignKey('classe.id'), primary_key=True),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'), primary_key=True)
)

class Module(db.Model):
    __tablename__ = 'module'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    semestre_id = db.Column(db.Integer, db.ForeignKey('semestre.id'), nullable=False)
    enseignant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    enseignant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f'<Module {self.nom}>'
