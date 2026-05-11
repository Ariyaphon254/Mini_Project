from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from extensions import db
from models.medicine import Medicine

medicine_bp = Blueprint('medicine', __name__, url_prefix='/medicines')

@medicine_bp.route('/')
@login_required
def index():
    search = request.args.get('search', '')
    if search:
        medicines = Medicine.query.filter(
            Medicine.name.contains(search) |
            Medicine.category.contains(search)
        ).all()
    else:
        medicines = Medicine.query.order_by(Medicine.name).all()
    return render_template('medicines/index.html', medicines=medicines, search=search)

@medicine_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        unit = request.form.get('unit', 'เม็ด')
        price = float(request.form.get('price_per_unit', 0) or 0)
        stock = int(request.form.get('stock_quantity', 0) or 0)
        min_stock = int(request.form.get('minimum_stock', 10) or 10)
        category = request.form.get('category', '').strip()

        if not name:
            flash('กรุณากรอกชื่อยา', 'danger')
            return render_template('medicines/form.html', action='add')

        med = Medicine(
            name=name, description=description or None,
            unit=unit, price_per_unit=price,
            stock_quantity=stock, minimum_stock=min_stock,
            category=category or None
        )
        db.session.add(med)
        db.session.commit()
        flash(f'เพิ่มยา "{name}" สำเร็จ', 'success')
        return redirect(url_for('medicine.index'))

    return render_template('medicines/form.html', action='add')

@medicine_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    med = Medicine.query.get_or_404(id)

    if request.method == 'POST':
        med.name = request.form.get('name', '').strip()
        med.description = request.form.get('description', '').strip() or None
        med.unit = request.form.get('unit', 'เม็ด')
        med.price_per_unit = float(request.form.get('price_per_unit', 0) or 0)
        med.stock_quantity = int(request.form.get('stock_quantity', 0) or 0)
        med.minimum_stock = int(request.form.get('minimum_stock', 10) or 10)
        med.category = request.form.get('category', '').strip() or None
        db.session.commit()
        flash(f'แก้ไขยา "{med.name}" สำเร็จ', 'success')
        return redirect(url_for('medicine.index'))

    return render_template('medicines/form.html', med=med, action='edit')

@medicine_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    med = Medicine.query.get_or_404(id)
    name = med.name
    db.session.delete(med)
    db.session.commit()
    flash(f'ลบยา "{name}" แล้ว', 'warning')
    return redirect(url_for('medicine.index'))

@medicine_bp.route('/restock/<int:id>', methods=['POST'])
@login_required
def restock(id):
    med = Medicine.query.get_or_404(id)
    amount = int(request.form.get('amount', 0) or 0)
    if amount > 0:
        med.stock_quantity += amount
        db.session.commit()
        flash(f'เติมสต็อก "{med.name}" +{amount} {med.unit} สำเร็จ', 'success')
    return redirect(url_for('medicine.index'))
