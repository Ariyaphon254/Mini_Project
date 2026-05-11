from extensions import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), nullable=True)
    treatment_fee = db.Column(db.Float, default=0.0)
    medicine_fee = db.Column(db.Float, default=0.0)
    discount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    payment_method = db.Column(db.String(50), default='cash')  # cash, card, transfer
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    payment_date = db.Column(db.DateTime, nullable=True)
    receipt_number = db.Column(db.String(50), unique=True, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def status_badge(self):
        badges = {'pending': 'warning', 'paid': 'success', 'refunded': 'danger'}
        return badges.get(self.payment_status, 'secondary')

    @property
    def status_text(self):
        texts = {'pending': 'รอชำระ', 'paid': 'ชำระแล้ว', 'refunded': 'คืนเงิน'}
        return texts.get(self.payment_status, self.payment_status)

    @property
    def method_text(self):
        texts = {'cash': 'เงินสด', 'card': 'บัตรเครดิต', 'transfer': 'โอนเงิน'}
        return texts.get(self.payment_method, self.payment_method)

    def generate_receipt_number(self):
        now = datetime.utcnow()
        self.receipt_number = f'RC{now.strftime("%Y%m%d%H%M%S")}{self.id}'

    def __repr__(self):
        return f'<Payment {self.receipt_number} - {self.total_amount} THB>'
