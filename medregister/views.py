from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, SignInForm, HealthRecordForm, PatientForm
from .models import Patient, HealthRecord
from django.db.models import Q 

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signin(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "You have logged in succesfully.")
            return redirect("patients")
    else:
        form = SignInForm()
    return render(request, "signin.html", {"form": form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered and logged in.')
            return redirect('patients')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def signout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')

@login_required
def patients(request):
    qs = Patient.objects.filter(user=request.user)   # base queryset

    # ─── BLOQUE NUEVO ───
    query = request.GET.get("q")                     # valor de ?q=
    if query:                                        # si hay texto
        qs = qs.filter(name__icontains=query)        # aplica filtro
    # ────────────────────

    patients = qs.order_by("name")
    return render(
        request,
        "patients.html",
        {"patients": patients, "query": query or ""}  # ← pasa “query”
    )
    return render(request, 'patients.html', {'patients': my_patients})

@login_required
def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()
            messages.success(request, 'Patient created successfully.')
            return redirect('patients')
    else:
        form = PatientForm()
    return render(request, 'create_patient.html', {'form': form})

@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient details updated successfully.')
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patient_detail.html', {'form': form, 'patient': patient})


@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully.')
        return redirect('patients')
    else:
        messages.error(request, 'Error deleting patient.')
        return redirect('patients')
    
@login_required
def diagnosis(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)

    # ─── BLOQUE DE BÚSQUEDA ───
    query = request.GET.get("q")
    if query:
        health_records = patient.health_records.filter(
            Q(diagnostic__icontains=query) |
            Q(description__icontains=query)
        ).order_by("-created_at")
    else:
        health_records = patient.health_records.order_by("-created_at")
    # ──────────────────────────

    form = HealthRecordForm()   # para el botón Create (si lo usas)

    return render(
        request,
        "diagnosis.html",
        {
            "patient": patient,
            "health_records": health_records,
            "query": query or "",
            "form": form,
        },
    )
@login_required
def create_diagnosis(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            health_record = form.save(commit=False)
            health_record.patient = patient
            health_record.save()
            messages.success(request, 'Diagnosis created successfully.')
            return redirect('diagnosis', patient_id=patient.id)
    else:
        form = HealthRecordForm()
    return render(request, 'create_diagnosis.html', {'form': form, 'patient': patient})

@login_required
def diagnosis_detail(request, patient_id, diagnosis_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    health_record = get_object_or_404(HealthRecord, id=diagnosis_id, patient=patient)
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=health_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Diagnosis updated successfully.')
            return redirect('diagnosis', patient_id=patient.id)
        else:
            messages.error(request, 'Error updating diagnosis.')
            return redirect('diagnosis_detail', patient_id=patient.id, diagnosis_id=diagnosis_id)
    else:
        form = HealthRecordForm(instance=health_record)
    return render(request, 'diagnosis_detail.html', {'form': form, 'patient': patient, 'health_record': health_record})

@login_required
def delete_diagnosis(request, patient_id, diagnosis_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    health_record = get_object_or_404(HealthRecord, id=diagnosis_id, patient=patient)
    if request.method == 'POST':
        health_record.delete()
        messages.success(request, 'Diagnosis deleted successfully.')
        return redirect('diagnosis', patient_id=patient.id)
    else:
        messages.error(request, 'Error deleting diagnosis.')
        return redirect('diagnosis', patient_id=patient.id)