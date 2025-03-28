from app import create_app, db
from app.models.user import User, UserRole
from app.models.classe import Classe
from app.models.semestre import Semestre, SemestreType
from app.models.module import Module, classe_module
from app.models.notes import Note
from app.models.reclamation import Reclamation, StatutReclamation
from werkzeug.security import generate_password_hash
import datetime

app = create_app()

with app.app_context():
    # Créer toutes les tables
    db.drop_all()  # Attention: cela supprime toutes les données existantes
    db.create_all()
    
    # Créer un utilisateur admin par défaut
    admin = User(
        name="Admin",
        lastname="System",
        email="admin@example.com",
        im="ADMIN001",
        password=generate_password_hash("admin123", method='pbkdf2:sha256'),
        role=UserRole.ADMIN
    )
    
    # Créer un enseignant par défaut
    enseignant = User(
        name="Prof",
        lastname="Test",
        email="prof@example.com",
        im="PROF001",
        password=generate_password_hash("prof123", method='pbkdf2:sha256'),
        role=UserRole.ENSEIGNANT
    )
    
    # Créer un étudiant par défaut
    etudiant = User(
        name="Etudiant",
        lastname="Test",
        email="etudiant@example.com",
        im="ETU001",
        password=generate_password_hash("etudiant123", method='pbkdf2:sha256'),
        role=UserRole.ETUDIANT
    )
    
    # Ajouter les utilisateurs à la base de données
    db.session.add(admin)
    db.session.add(enseignant)
    db.session.add(etudiant)
    
    # Créer une classe par défaut
    classe = Classe(
        nom="Informatique",
        niveau="Licence 3"
    )
    
    # Ajouter la classe à la base de données
    db.session.add(classe)
    
    # Associer l'étudiant à la classe
    etudiant.classe_id = 1
    
    # Créer un semestre par défaut
    semestre = Semestre(
        type=SemestreType.S5,
        annee_academique="2023-2024"
    )
    
    # Ajouter le semestre à la base de données
    db.session.add(semestre)
    
    # Valider les changements
    db.session.commit()
    
    print("Base de données initialisée avec succès!")
