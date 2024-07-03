from django.urls import path
from .views import healthRecord, recordDetails, hospitaVisitDetails, addHospitalVisit, deleteHospitalVisit, searchRecords, otpVerify
# from .forms import LoginForm

urlpatterns = [
    path('health-records/',  healthRecord, name='h-records'),
    path('record-details/<int:pk>',  recordDetails, name='records-details'),
    path('visit-details/<int:pk>',  hospitaVisitDetails, name='visit-details'),
    path('<int:pk>/add-visit/', addHospitalVisit, name='visit_submit'),
    path('<int:pk>/delete-visit/', deleteHospitalVisit, name='visit_delete'),
    path('search-results/',  searchRecords, name='search-records'),
    path('otp/<str:uid>/', otpVerify, name='otp')
]