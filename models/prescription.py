from extensions import db
from datetime import datetime

class Prescription(db.Model):
    __tablename__ = 'prescriptions'

    id = db.Column(db.Integer, primary_key=True)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    dosage = db.Column(db.String(200), nullable=True)  # e.g. "1 เม็ด วันละ 2 ครั้ง"
    duration_days = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    unit_price = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def __repr__(self):
        return f'<Prescription {self.id} - Treatment {self.treatment_id}>'
