from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from extensions import db
from models.veterinarian import Veterinarian
from models.user import User

vet_bp = Blueprint('vet', __name__, url_prefix='/vets')

@vet_bp.route('/')
@login_required
def index():
    vets = Veterinarian.query.order_by(Veterinarian.name).all()
    return render_template('vets/index.html', vets=vets)

@vet_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        license_number = request.form.get('license_number', '').strip()
        specialization = request.form.get('specialization', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip() or None
        status = request.form.get('status', 'active')
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not name or not license_number:
            flash('กรุณากรอกชื่อและหมายเลขใบอนุญาต', 'danger')
            return render_template('vets/form.html', action='add')

        if Veterinarian.query.filter_by(license_number=license_number).first():
            flash('หมายเลขใบอนุญาตนี้มีอยู่แล้ว', 'danger')
            return render_template('vets/form.html', action='add')

        vet = Veterinarian(
            name=name, license_number=license_number,
            specialization=specialization or None,
            phone=phone or None, email=email, status=status
        )
        db.session.add(vet)
        db.session.flush()

        # Create user account for vet
        if username and password:
            if User.query.filter_by(username=username).first():
                flash('ชื่อผู้ใช้นี้มีอยู่แล้ว', 'danger')
                db.session.rollback()
                return render_template('vets/form.html', action='add')
            user = User(username=username, name=name, email=email, role='vet', vet_id=vet.id)
            user.set_password(password)
            db.session.add(user)

        db.session.commit()
        flash(f'เพิ่มข้อมูลสัตวแพทย์ "{name}" สำเร็จ', 'success')
        return redirect(url_for('vet.index'))

    return render_template('vets/form.html', action='add')

@vet_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    vet = Veterinarian.query.get_or_404(id)

    if request.method == 'POST':
        vet.name = request.form.get('name', '').strip()
        vet.specialization = request.form.get('specialization', '').strip() or None
        vet.phone = request.form.get('phone', '').strip() or None
        vet.email = request.form.get('email', '').strip() or None
        vet.status = request.form.get('status', 'active')
        db.session.commit()
        flash(f'แก้ไขข้อมูล "{vet.name}" สำเร็จ', 'success')
        return redirect(url_for('vet.index'))

    return render_template('vets/form.html', vet=vet, action='edit')

@vet_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    vet = Veterinarian.query.get_or_404(id)
    name = vet.name
    # Delete associated user
    if vet.user:
        db.session.delete(vet.user)
    db.session.delete(vet)
    db.session.commit()
    flash(f'ลบข้อมูล "{name}" แล้ว', 'warning')
    return redirect(url_for('vet.index'))

@vet_bp.route('/view/<int:id>')
@login_required
def view(id):
    vet = Veterinarian.query.get_or_404(id)
    return render_template('vets/view.html', vet=vet)
