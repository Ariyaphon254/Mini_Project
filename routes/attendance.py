from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from models.attendance import Attendance
from models.veterinarian import Veterinarian
from datetime import datetime, date

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@attendance_bp.route('/')
@login_required
def index():
    date_filter = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    vet_filter = request.args.get('vet_id', '')

    try:
        filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
    except ValueError:
        filter_date = date.today()

    query = Attendance.query.filter(Attendance.date == filter_date)
    if vet_filter:
        query = query.filter(Attendance.vet_id == int(vet_filter))

    records = query.all()
    vets = Veterinarian.query.filter_by(status='active').order_by(Veterinarian.name).all()

    return render_template('attendance/index.html',
        records=records, vets=vets,
        date_filter=date_filter, vet_filter=vet_filter,
        filter_date=filter_date
    )

@attendance_bp.route('/checkin/<int:vet_id>', methods=['POST'])
@login_required
def checkin(vet_id):
    vet = Veterinarian.query.get_or_404(vet_id)
    today = date.today()

    existing = Attendance.query.filter_by(vet_id=vet_id, date=today).first()
    if existing:
        if existing.check_in:
            flash(f'{vet.name} เช็คอินแล้ววันนี้', 'warning')
        else:
            existing.check_in = datetime.utcnow()
            db.session.commit()
            flash(f'{vet.name} เช็คอินสำเร็จ', 'success')
    else:
        record = Attendance(vet_id=vet_id, date=today, check_in=datetime.utcnow())
        db.session.add(record)
        db.session.commit()
        flash(f'{vet.name} เช็คอินสำเร็จ', 'success')

    return redirect(url_for('attendance.index'))

@attendance_bp.route('/checkout/<int:vet_id>', methods=['POST'])
@login_required
def checkout(vet_id):
    vet = Veterinarian.query.get_or_404(vet_id)
    today = date.today()

    record = Attendance.query.filter_by(vet_id=vet_id, date=today).first()
    if not record or not record.check_in:
        flash(f'{vet.name} ยังไม่ได้เช็คอิน', 'danger')
    elif record.check_out:
        flash(f'{vet.name} เช็คเอาท์แล้วในวันนี้', 'warning')
    else:
        record.check_out = datetime.utcnow()
        db.session.commit()
        flash(f'{vet.name} เช็คเอาท์สำเร็จ ทำงาน {record.work_hours}', 'success')

    return redirect(url_for('attendance.index'))

@attendance_bp.route('/history')
@login_required
def history():
    vet_id = request.args.get('vet_id', '')
    month = request.args.get('month', date.today().strftime('%Y-%m'))

    query = Attendance.query
    if vet_id:
        query = query.filter(Attendance.vet_id == int(vet_id))
    if month:
        try:
            year, mon = month.split('-')
            query = query.filter(
                db.extract('year', Attendance.date) == int(year),
                db.extract('month', Attendance.date) == int(mon)
            )
        except ValueError:
            pass

    records = query.order_by(Attendance.date.desc()).all()
    vets = Veterinarian.query.order_by(Veterinarian.name).all()

    return render_template('attendance/history.html',
        records=records, vets=vets,
        vet_filter=vet_id, month=month
    )
