from extensions import db
from datetime import datetime

class Veterinarian(db.Model):
    __tablename__ = 'veterinarians'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    specialization = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    status = db.Column(db.String(20), default='active')  # active, inactive, on_leave
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    appointments = db.relationship('Appointment', backref='veterinarian', lazy=True)
    treatments = db.relationship('Treatment', backref='veterinarian', lazy=True)
    attendances = db.relationship('Attendance', backref='veterinarian', lazy=True, cascade='all, delete-orphan')
    user = db.relationship('User', backref='veterinarian', uselist=False, lazy=True)

    def __repr__(self):
        return f'<Veterinarian {self.name}>'

    @property
    def status_badge(self):
        badges = {
            'active': 'success',
            'inactive': 'secondary',
            'on_leave': 'warning'
        }
        return badges.get(self.status, 'secondary')

    @property
    def status_text(self):
        texts = {
            'active': 'ทำงานอยู่',
            'inactive': 'ไม่ได้ทำงาน',
            'on_leave': 'ลาพัก'
        }
        return texts.get(self.status, self.status)
