from extensions import db
from datetime import datetime

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    vet_id = db.Column(db.Integer, db.ForeignKey('veterinarians.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def work_hours(self):
        if self.check_in and self.check_out:
            delta = self.check_out - self.check_in
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            return f'{hours} ชั่วโมง {minutes} นาที'
        return '-'

    @property
    def status(self):
        if self.check_in and self.check_out:
            return ('success', 'เสร็จสิ้น')
        elif self.check_in:
            return ('warning', 'กำลังทำงาน')
        return ('secondary', 'ยังไม่เข้างาน')

    def __repr__(self):
        return f'<Attendance Vet:{self.vet_id} Date:{self.date}>'
