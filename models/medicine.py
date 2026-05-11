from extensions import db
from datetime import datetime

class Medicine(db.Model):
    __tablename__ = 'medicines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    unit = db.Column(db.String(50), nullable=False, default='เม็ด')  # tablet, ml, capsule
    price_per_unit = db.Column(db.Float, nullable=False, default=0.0)
    stock_quantity = db.Column(db.Integer, default=0)
    minimum_stock = db.Column(db.Integer, default=10)
    category = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    prescriptions = db.relationship('Prescription', backref='medicine', lazy=True)

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.minimum_stock

    @property
    def stock_status(self):
        if self.stock_quantity == 0:
            return ('danger', 'หมด')
        elif self.is_low_stock:
            return ('warning', 'ใกล้หมด')
        return ('success', 'พอเพียง')

    def __repr__(self):
        return f'<Medicine {self.name}>'
