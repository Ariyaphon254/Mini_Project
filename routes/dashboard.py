from flask import Blueprint, render_template
from flask_login import login_required
from models.owner import Owner
from models.pet import Pet
from models.veterinarian import Veterinarian
from models.appointment import Appointment
from models.treatment import Treatment
from models.medicine import Medicine
from models.payment import Payment
from models.attendance import Attendance
from datetime import datetime, date

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    today = date.today()

    # Summary counts
    total_owners = Owner.query.count()
    total_pets = Pet.query.count()
    total_vets = Veterinarian.query.filter_by(status='active').count()
    total_medicines = Medicine.query.count()

    # Today's appointments
    today_appointments = Appointment.query.filter(
        Appointment.appointment_date == today
    ).order_by(Appointment.appointment_time).all()

    # Recent appointments
    recent_appointments = Appointment.query.order_by(
        Appointment.created_at.desc()
    ).limit(5).all()

    # Appointment stats
    waiting_count = Appointment.query.filter_by(status='waiting').count()
    confirmed_count = Appointment.query.filter_by(status='confirmed').count()
    completed_count = Appointment.query.filter_by(status='completed').count()
    cancelled_count = Appointment.query.filter_by(status='cancelled').count()

    # Low stock medicines
    low_stock = Medicine.query.filter(
        Medicine.stock_quantity <= Medicine.minimum_stock
    ).all()

    # Recent payments
    recent_payments = Payment.query.filter_by(
        payment_status='paid'
    ).order_by(Payment.payment_date.desc()).limit(5).all()

    # Today's revenue
    from sqlalchemy import func
    today_revenue = Payment.query.filter(
        func.date(Payment.payment_date) == today,
        Payment.payment_status == 'paid'
    ).with_entities(func.sum(Payment.total_amount)).scalar() or 0

    # Monthly revenue
    month_start = date.today().replace(day=1)
    monthly_revenue = Payment.query.filter(
        func.date(Payment.payment_date) >= month_start,
        Payment.payment_status == 'paid'
    ).with_entities(func.sum(Payment.total_amount)).scalar() or 0

    # Vets checked in today
    vets_checked_in = Attendance.query.filter(
        Attendance.date == today,
        Attendance.check_in.isnot(None),
        Attendance.check_out.is_(None)
    ).count()

    return render_template('dashboard/index.html',
        total_owners=total_owners,
        total_pets=total_pets,
        total_vets=total_vets,
        total_medicines=total_medicines,
        today_appointments=today_appointments,
        recent_appointments=recent_appointments,
        waiting_count=waiting_count,
        confirmed_count=confirmed_count,
        completed_count=completed_count,
        cancelled_count=cancelled_count,
        low_stock=low_stock,
        recent_payments=recent_payments,
        today_revenue=today_revenue,
        monthly_revenue=monthly_revenue,
        vets_checked_in=vets_checked_in,
        today=today
    )
