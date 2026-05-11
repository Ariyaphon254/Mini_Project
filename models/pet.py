from extensions import db
from datetime import datetime

class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)  # dog, cat, bird, etc.
    breed = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(10), nullable=False)  # male, female
    date_of_birth = db.Column(db.Date, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    color = db.Column(db.String(50), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    appointments = db.relationship('Appointment', backref='pet', lazy=True, cascade='all, delete-orphan')
    treatments = db.relationship('Treatment', backref='pet', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Pet {self.name}>'

    @property
    def age(self):
        if self.date_of_birth:
            today = datetime.today().date()
            delta = today - self.date_of_birth
            years = delta.days // 365
            months = (delta.days % 365) // 30
            if years > 0:
                return f'{years} ปี {months} เดือน'
            else:
                return f'{months} เดือน'
        return 'ไม่ระบุ'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species,
            'breed': self.breed,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else '',
            'weight': self.weight,
            'color': self.color,
            'owner_id': self.owner_id,
            'age': self.age,
        }
