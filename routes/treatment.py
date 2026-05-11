from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from extensions import db
from models.treatment import Treatment
from models.prescription import Prescription
from models.appointment import Appointment
from models.pet import Pet
from models.veterinarian import Veterinarian
from models.medicine import Medicine
from datetime import datetime

treatment_bp = Blueprint('treatment', __name__, url_prefix='/treatments')

@treatment_bp.route('/')
@login_required
def index():
    treatments = Treatment.query.order_by(Treatment.treatment_date.desc()).all()
    return render_template('treatments/index.html', treatments=treatments)

@treatment_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    pets = Pet.query.order_by(Pet.name).all()
    vets = Veterinarian.query.filter_by(status='active').order_by(Veterinarian.name).all()
    appointments = Appointment.query.filter_by(status='confirmed').order_by(Appointment.appointment_date.desc()).all()
    medicines = Medicine.query.filter(Medicine.stock_quantity > 0).order_by(Medicine.name).all()

    if request.method == 'POST':
        pet_id = request.form.get('pet_id')
        vet_id = request.form.get('vet_id')
        appointment_id = request.form.get('appointment_id') or None
        symptoms = request.form.get('symptoms', '').strip()
        diagnosis = request.form.get('diagnosis', '').strip()
        treatment_details = request.form.get('treatment_details', '').strip()
        doctor_notes = request.form.get('doctor_notes', '').strip()
        treatment_fee = float(request.form.get('treatment_fee', 0) or 0)

        if not pet_id or not vet_id:
            flash('กรุณาเลือกสัตว์เลี้ยงและสัตวแพทย์', 'danger')
            return render_template('treatments/form.html', pets=pets, vets=vets,
                                   appointments=appointments, medicines=medicines, action='add')

        treatment = Treatment(
            pet_id=int(pet_id), vet_id=int(vet_id),
            appointment_id=int(appointment_id) if appointment_id else None,
            symptoms=symptoms or None, diagnosis=diagnosis or None,
            treatment_details=treatment_details or None,
            doctor_notes=doctor_notes or None,
            treatment_fee=treatment_fee,
            treatment_date=datetime.utcnow()
        )
        db.session.add(treatment)
        db.session.flush()

        # Update appointment status
        if appointment_id:
            appt = Appointment.query.get(int(appointment_id))
            if appt:
                appt.status = 'completed'

        # Handle prescriptions
        med_ids = request.form.getlist('medicine_id[]')
        quantities = request.form.getlist('quantity[]')
        dosages = request.form.getlist('dosage[]')
        durations = request.form.getlist('duration_days[]')

        for i, med_id in enumerate(med_ids):
            if med_id:
                med = Medicine.query.get(int(med_id))
                if med:
                    qty = int(quantities[i]) if quantities[i] else 1
                    prescription = Prescription(
                        treatment_id=treatment.id,
                        medicine_id=int(med_id),
                        quantity=qty,
                        dosage=dosages[i] if dosages[i] else None,
                        duration_days=int(durations[i]) if durations[i] else None,
                        unit_price=med.price_per_unit
                    )
                    med.stock_quantity = max(0, med.stock_quantity - qty)
                    db.session.add(prescription)

        db.session.commit()
        flash('บันทึกข้อมูลการรักษาสำเร็จ', 'success')
        return redirect(url_for('treatment.index'))

    return render_template('treatments/form.html', pets=pets, vets=vets,
                           appointments=appointments, medicines=medicines, action='add')

@treatment_bp.route('/view/<int:id>')
@login_required
def view(id):
    treatment = Treatment.query.get_or_404(id)
    return render_template('treatments/view.html', treatment=treatment)

@treatment_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    treatment = Treatment.query.get_or_404(id)
    # Restore medicine stock
    for prescription in treatment.prescriptions:
        med = Medicine.query.get(prescription.medicine_id)
        if med:
            med.stock_quantity += prescription.quantity
    db.session.delete(treatment)
    db.session.commit()
    flash('ลบข้อมูลการรักษาแล้ว', 'warning')
    return redirect(url_for('treatment.index'))
