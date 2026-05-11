from extensions import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    vet_id = db.Column(db.Integer, db.ForeignKey('veterinarians.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='waiting')  # waiting, confirmed, completed, cancelled
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    treatment = db.relationship('Treatment', backref='appointment', uselist=False, lazy=True)
    payment = db.relationship('Payment', backref='appointment', uselist=False, lazy=True)

    @property
    def status_badge(self):
        badges = {
            'waiting': 'warning',
            'confirmed': 'info',
            'completed': 'success',
            'cancelled': 'danger'
        }
        return badges.get(self.status, 'secondary')

    @property
    def status_text(self):
        texts = {
            'waiting': 'รอรับบริการ',
            'confirmed': 'ยืนยันแล้ว',
            'completed': 'เสร็จสิ้น',
            'cancelled': 'ยกเลิก'
        }
        return texts.get(self.status, self.status)

    @property
    def appointment_datetime_str(self):
        if self.appointment_date and self.appointment_time:
            return f"{self.appointment_date.strftime('%d/%m/%Y')} {self.appointment_time.strftime('%H:%M')}"
        return ''

    def __repr__(self):
        return f'<Appointment {self.id} - Pet {self.pet_id}>'
