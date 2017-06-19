from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from django.utils.html import format_html

from MedApp.models import CustomUser, Appointment, Patient, Specialization, Diagnostic, Consultation, ConsultationResult


class DoctorFilter(admin.SimpleListFilter):
    title = 'Doctors'
    parameter_name = 'doctor'

    def lookups(self, request, model_admin):
        doctors = []
        qs = CustomUser.objects.filter(groups__in=[1]).distinct()
        for c in qs:
            doctors.append([c.id, c.get_full_name()])
        return doctors

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(doctor__id__exact=self.value())
        else:
            return queryset


class AppointmentEdit(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'time', 'created_by')
    exclude = ('created_by', )

    list_filter = ['time', DoctorFilter]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'doctor':
            kwargs["queryset"] = CustomUser.objects.filter(groups__in=[1])
        return super(AppointmentEdit, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(AppointmentEdit, self).get_queryset(request)
        if request.user.groups.filter(name='Doctors').exists():
            return qs.filter(doctor=request.user)
        else:
            return qs


class ConsultationEdit(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'specialization')


class ConsultationResultEdit(admin.ModelAdmin):
    list_display = ('patient','diagnostic','recipe','image_tag')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'diagnostic':
            specialization_id = Specialization.objects.get(doctor_id=request.user.id)
            kwargs["queryset"] = Diagnostic.objects.filter(specilization_id=specialization_id)
        return super(ConsultationResultEdit, self).formfield_for_foreignkey(db_field, request, **kwargs)




class DiagnosticEdit(admin.ModelAdmin):
    list_display = ('name', 'code')

    def get_queryset(self, request):
        qs = super(DiagnosticEdit, self).get_queryset(request)
        if request.user.groups.filter(name='Doctors').exists():
            specialization_id = Specialization.objects.get(doctor_id = request.user.id)
            return qs.filter( specilization_id= specialization_id)
        else:
            return qs



class PatientEdit(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    # list_filter = [DoctorFilter,]
    exclude = ['doctor']
    search_fields = ('first_name', 'last_name', 'cnp',)






admin.site.register(Diagnostic, DiagnosticEdit)
admin.site.register(ConsultationResult, ConsultationResultEdit)
admin.site.register(Appointment, AppointmentEdit)
admin.site.register(Consultation, ConsultationEdit)
admin.site.register(Patient, PatientEdit)


class FilterUser(admin.ModelAdmin):
    def is_member(self, CustomUser):
        if CustomUser.groups.filter(name='Doctors').exists():
            pass

    admin.site.register(Specialization)


admin.site.register(CustomUser, FilterUser)



# admin.site.register(Specialization)

# admin.site.register(Diagnostic)
#
# admin.site.register(Consultation)

# admin.site.register(ConsultationResult, FilterByUser)
