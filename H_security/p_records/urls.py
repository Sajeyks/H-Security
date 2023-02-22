from django.urls import path
from django.contrib.auth import views as auth_views
from .views import healthRecord, recordDetails, hospitaVisit, hospitaVisitDetails, addHospitalVisit, deleteHospitalVisit
# from .forms import LoginForm

urlpatterns = [
    path('health-records/',  healthRecord, name='h-records'),
    path('record-details/<int:pk>',  recordDetails, name='records-details'),
    path('visit-details/<int:pk>',  hospitaVisitDetails, name='visit-details'),
    path('<int:pk>/add-visit/', addHospitalVisit, name='visit_submit'),
    path('<int:pk>/delete-visit/', deleteHospitalVisit, name='visit_delete'),
    
]