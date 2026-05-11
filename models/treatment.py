from extensions import db
from datetime import datetime

class Treatment(db.Model):
    __tablename__ = 'treatments'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    vet_id = db.Column(db.Integer, db.ForeignKey('veterinarians.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=True)
    diagnosis = db.Column(db.Text, nullable=True)
    treatment_details = db.Column(db.Text, nullable=True)
    doctor_notes = db.Column(db.Text, nullable=True)
    treatment_fee = db.Column(db.Float, default=0.0)
    treatment_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    prescriptions = db.relationship('Prescription', backref='treatment', lazy=True, cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='treatment', uselist=False, lazy=True)

    def __repr__(self):
        return f'<Treatment {self.id} - Pet {self.pet_id}>'

    @property
    def total_medicine_cost(self):
        return sum(p.subtotal for p in self.prescriptions)

    @property
    def grand_total(self):
        return self.treatment_fee + self.total_medicine_cost
