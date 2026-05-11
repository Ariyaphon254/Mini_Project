from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from extensions import db
from models.pet import Pet
from models.owner import Owner
from datetime import datetime

pet_bp = Blueprint('pet', __name__, url_prefix='/pets')

@pet_bp.route('/')
@login_required
def index():
    search = request.args.get('search', '')
    if search:
        pets = Pet.query.join(Owner).filter(
            Pet.name.contains(search) |
            Pet.species.contains(search) |
            Owner.name.contains(search)
        ).all()
    else:
        pets = Pet.query.order_by(Pet.name).all()
    return render_template('pets/index.html', pets=pets, search=search)

@pet_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    owners = Owner.query.order_by(Owner.name).all()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        species = request.form.get('species', '').strip()
        breed = request.form.get('breed', '').strip()
        gender = request.form.get('gender', '')
        dob_str = request.form.get('date_of_birth', '')
        weight = request.form.get('weight', '')
        color = request.form.get('color', '').strip()
        owner_id = request.form.get('owner_id', '')

        if not name or not species or not gender or not owner_id:
            flash('กรุณากรอกข้อมูลที่จำเป็นให้ครบ', 'danger')
            return render_template('pets/form.html', owners=owners, action='add')

        dob = None
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        pet = Pet(
            name=name, species=species, breed=breed or None,
            gender=gender, date_of_birth=dob,
            weight=float(weight) if weight else None,
            color=color or None, owner_id=int(owner_id)
        )
        db.session.add(pet)
        db.session.commit()
        flash(f'เพิ่มข้อมูลสัตว์เลี้ยง "{name}" สำเร็จ', 'success')
        return redirect(url_for('pet.index'))

    return render_template('pets/form.html', owners=owners, action='add')

@pet_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    pet = Pet.query.get_or_404(id)
    owners = Owner.query.order_by(Owner.name).all()

    if request.method == 'POST':
        pet.name = request.form.get('name', '').strip()
        pet.species = request.form.get('species', '').strip()
        pet.breed = request.form.get('breed', '').strip() or None
        pet.gender = request.form.get('gender', '')
        pet.color = request.form.get('color', '').strip() or None
        pet.owner_id = int(request.form.get('owner_id', pet.owner_id))

        dob_str = request.form.get('date_of_birth', '')
        if dob_str:
            try:
                pet.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                pet.date_of_birth = None

        weight = request.form.get('weight', '')
        pet.weight = float(weight) if weight else None

        db.session.commit()
        flash(f'แก้ไขข้อมูล "{pet.name}" สำเร็จ', 'success')
        return redirect(url_for('pet.index'))

    return render_template('pets/form.html', pet=pet, owners=owners, action='edit')

@pet_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    pet = Pet.query.get_or_404(id)
    name = pet.name
    db.session.delete(pet)
    db.session.commit()
    flash(f'ลบข้อมูล "{name}" แล้ว', 'warning')
    return redirect(url_for('pet.index'))

@pet_bp.route('/view/<int:id>')
@login_required
def view(id):
    pet = Pet.query.get_or_404(id)
    return render_template('pets/view.html', pet=pet)
