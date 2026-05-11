from .auth import auth_bp
from .dashboard import dashboard_bp
from .owner import owner_bp
from .pet import pet_bp
from .vet import vet_bp
from .appointment import appointment_bp
from .treatment import treatment_bp
from .medicine import medicine_bp
from .attendance import attendance_bp
from .payment import payment_bp

__all__ = [
    'auth_bp', 'dashboard_bp', 'owner_bp', 'pet_bp',
    'vet_bp', 'appointment_bp', 'treatment_bp',
    'medicine_bp', 'attendance_bp', 'payment_bp'
]
