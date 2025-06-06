from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('patients/', views.patients, name='patients'),
    path('patients/create/', views.create_patient, name='create_patient'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),
    path('patients/diagnosis/<int:patient_id>/', views.diagnosis, name='diagnosis'),
    path('patients/diagnosis/<int:patient_id>/create/', views.create_diagnosis, name='create_diagnosis'),
    path('patients/diagnosis/<int:patient_id>/<int:diagnosis_id>/', views.diagnosis_detail, name='diagnosis_detail'),
    path('patients/diagnosis/<int:patient_id>/<int:diagnosis_id>/delete/', views.delete_diagnosis, name='delete_diagnosis'),


]