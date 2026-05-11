from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from extensions import db
from models.owner import Owner

owner_bp = Blueprint('owner', __name__, url_prefix='/owners')

@owner_bp.route('/')
@login_required
def index():
    search = request.args.get('search', '')
    if search:
        owners = Owner.query.filter(
            Owner.name.contains(search) |
            Owner.phone.contains(search) |
            Owner.email.contains(search)
        ).all()
    else:
        owners = Owner.query.order_by(Owner.name).all()
    return render_template('owners/index.html', owners=owners, search=search)

@owner_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip() or None
        address = request.form.get('address', '').strip()

        if not name or not phone:
            flash('กรุณากรอกชื่อและเบอร์โทรศัพท์', 'danger')
            return render_template('owners/form.html', action='add')

        # Check duplicate email
        if email and Owner.query.filter_by(email=email).first():
            flash('อีเมลนี้ถูกใช้งานแล้ว', 'danger')
            return render_template('owners/form.html', action='add')

        owner = Owner(name=name, phone=phone, email=email, address=address)
        db.session.add(owner)
        db.session.commit()
        flash(f'เพิ่มข้อมูลเจ้าของ "{name}" สำเร็จ', 'success')
        return redirect(url_for('owner.index'))

    return render_template('owners/form.html', action='add')

@owner_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    owner = Owner.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip() or None
        address = request.form.get('address', '').strip()

        if not name or not phone:
            flash('กรุณากรอกชื่อและเบอร์โทรศัพท์', 'danger')
            return render_template('owners/form.html', owner=owner, action='edit')

        # Check duplicate email (exclude current owner)
        if email:
            existing = Owner.query.filter_by(email=email).first()
            if existing and existing.id != id:
                flash('อีเมลนี้ถูกใช้งานแล้ว', 'danger')
                return render_template('owners/form.html', owner=owner, action='edit')

        owner.name = name
        owner.phone = phone
        owner.email = email
        owner.address = address
        db.session.commit()
        flash(f'แก้ไขข้อมูล "{name}" สำเร็จ', 'success')
        return redirect(url_for('owner.index'))

    return render_template('owners/form.html', owner=owner, action='edit')

@owner_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    owner = Owner.query.get_or_404(id)
    name = owner.name
    db.session.delete(owner)
    db.session.commit()
    flash(f'ลบข้อมูล "{name}" แล้ว', 'warning')
    return redirect(url_for('owner.index'))

@owner_bp.route('/view/<int:id>')
@login_required
def view(id):
    owner = Owner.query.get_or_404(id)
    return render_template('owners/view.html', owner=owner)
