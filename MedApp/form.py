from django import forms

from MedApp.models import ConsultationResult


class ConsultationResultForm(forms.ModelForm):
    model = ConsultationResult

    class Meta:
        fields = ['Consultation.patient', 'Consultation.doctor', 'recipe']
