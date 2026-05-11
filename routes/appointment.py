from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from models.appointment import Appointment
from models.pet import Pet
from models.veterinarian import Veterinarian
from datetime import datetime

appointment_bp = Blueprint('appointment', __name__, url_prefix='/appointments')

@appointment_bp.route('/')
@login_required
def index():
    status_filter = request.args.get('status', '')
    date_filter = request.args.get('date', '')

    query = Appointment.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(Appointment.appointment_date == filter_date)
        except ValueError:
            pass

    appointments = query.order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()

    return render_template('appointments/index.html',
        appointments=appointments,
        status_filter=status_filter,
        date_filter=date_filter
    )

@appointment_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    pets = Pet.query.order_by(Pet.name).all()
    vets = Veterinarian.query.filter_by(status='active').order_by(Veterinarian.name).all()

    if request.method == 'POST':
        pet_id = request.form.get('pet_id')
        vet_id = request.form.get('vet_id')
        appt_date = request.form.get('appointment_date')
        appt_time = request.form.get('appointment_time')
        reason = request.form.get('reason', '').strip()
        notes = request.form.get('notes', '').strip()

        if not pet_id or not vet_id or not appt_date or not appt_time:
            flash('กรุณากรอกข้อมูลให้ครบ', 'danger')
            return render_template('appointments/form.html', pets=pets, vets=vets, action='add')

        try:
            date_obj = datetime.strptime(appt_date, '%Y-%m-%d').date()
            time_obj = datetime.strptime(appt_time, '%H:%M').time()
        except ValueError:
            flash('รูปแบบวันที่หรือเวลาไม่ถูกต้อง', 'danger')
            return render_template('appointments/form.html', pets=pets, vets=vets, action='add')

        appt = Appointment(
            pet_id=int(pet_id), vet_id=int(vet_id),
            appointment_date=date_obj, appointment_time=time_obj,
            reason=reason or None, notes=notes or None, status='waiting'
        )
        db.session.add(appt)
        db.session.commit()
        flash('บันทึกการนัดหมายสำเร็จ', 'success')
        return redirect(url_for('appointment.index'))

    return render_template('appointments/form.html', pets=pets, vets=vets, action='add')

@appointment_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    appt = Appointment.query.get_or_404(id)
    pets = Pet.query.order_by(Pet.name).all()
    vets = Veterinarian.query.filter_by(status='active').order_by(Veterinarian.name).all()

    if request.method == 'POST':
        appt.pet_id = int(request.form.get('pet_id', appt.pet_id))
        appt.vet_id = int(request.form.get('vet_id', appt.vet_id))
        appt.reason = request.form.get('reason', '').strip() or None
        appt.notes = request.form.get('notes', '').strip() or None
        appt.status = request.form.get('status', appt.status)

        date_str = request.form.get('appointment_date', '')
        time_str = request.form.get('appointment_time', '')
        if date_str:
            appt.appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if time_str:
            appt.appointment_time = datetime.strptime(time_str, '%H:%M').time()

        db.session.commit()
        flash('แก้ไขการนัดหมายสำเร็จ', 'success')
        return redirect(url_for('appointment.index'))

    return render_template('appointments/form.html', appt=appt, pets=pets, vets=vets, action='edit')

@appointment_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    appt = Appointment.query.get_or_404(id)
    db.session.delete(appt)
    db.session.commit()
    flash('ลบการนัดหมายแล้ว', 'warning')
    return redirect(url_for('appointment.index'))

@appointment_bp.route('/update-status/<int:id>', methods=['POST'])
@login_required
def update_status(id):
    appt = Appointment.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status in ['waiting', 'confirmed', 'completed', 'cancelled']:
        appt.status = new_status
        db.session.commit()
        flash('อัปเดตสถานะสำเร็จ', 'success')
    return redirect(url_for('appointment.index'))
