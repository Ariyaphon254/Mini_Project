from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from extensions import db
from models.payment import Payment
from models.treatment import Treatment
from models.appointment import Appointment
from datetime import datetime

payment_bp = Blueprint('payment', __name__, url_prefix='/payments')

@payment_bp.route('/')
@login_required
def index():
    status_filter = request.args.get('status', '')
    query = Payment.query
    if status_filter:
        query = query.filter_by(payment_status=status_filter)
    payments = query.order_by(Payment.created_at.desc()).all()
    return render_template('payments/index.html', payments=payments, status_filter=status_filter)

@payment_bp.route('/create/<int:treatment_id>', methods=['GET', 'POST'])
@login_required
def create(treatment_id):
    treatment = Treatment.query.get_or_404(treatment_id)
    medicine_fee = treatment.total_medicine_cost

    if request.method == 'POST':
        treatment_fee = float(request.form.get('treatment_fee', treatment.treatment_fee) or 0)
        discount = float(request.form.get('discount', 0) or 0)
        payment_method = request.form.get('payment_method', 'cash')
        notes = request.form.get('notes', '').strip()
        total = treatment_fee + medicine_fee - discount

        # Check if payment already exists
        existing = Payment.query.filter_by(treatment_id=treatment_id, payment_status='paid').first()
        if existing:
            flash('มีการบันทึกการชำระเงินสำหรับการรักษานี้แล้ว', 'warning')
            return redirect(url_for('payment.index'))

        payment = Payment(
            treatment_id=treatment_id,
            appointment_id=treatment.appointment_id,
            treatment_fee=treatment_fee,
            medicine_fee=medicine_fee,
            discount=discount,
            total_amount=total,
            payment_method=payment_method,
            payment_status='paid',
            payment_date=datetime.utcnow(),
            notes=notes or None
        )
        db.session.add(payment)
        db.session.flush()
        payment.generate_receipt_number()

        # Update appointment status
        if treatment.appointment_id:
            appt = Appointment.query.get(treatment.appointment_id)
            if appt:
                appt.status = 'completed'

        db.session.commit()
        flash(f'บันทึกการชำระเงินสำเร็จ ใบเสร็จ: {payment.receipt_number}', 'success')
        return redirect(url_for('payment.receipt', id=payment.id))

    return render_template('payments/create.html',
        treatment=treatment,
        medicine_fee=medicine_fee
    )

@payment_bp.route('/receipt/<int:id>')
@login_required
def receipt(id):
    payment = Payment.query.get_or_404(id)
    return render_template('payments/receipt.html', payment=payment)

@payment_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    payment = Payment.query.get_or_404(id)
    db.session.delete(payment)
    db.session.commit()
    flash('ลบข้อมูลการชำระเงินแล้ว', 'warning')
    return redirect(url_for('payment.index'))
