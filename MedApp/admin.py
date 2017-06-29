from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from MedApp.models import CustomUser, Appointment, Patient, Specialization, Diagnostic, Consultation, ConsultationResult


# Register your models here.


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
    actions = ['print_consultation']
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'diagnostic':
            specialization_id = Specialization.objects.get(doctor_id=request.user.id)
            kwargs["queryset"] = Diagnostic.objects.filter(specilization_id=specialization_id)
        return super(ConsultationResultEdit, self).formfield_for_foreignkey(db_field, request, **kwargs)

        # def print_consultation(request, canvas=None):
        #     response = HttpResponse(content_type='application/pdf')
        #     response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
        #
        #     buffer = BytesIO()
        #
        #     # Create the PDF object, using the BytesIO object as its "file."
        #     p = canvas.Canvas(buffer)
        #
        #     # Draw things on the PDF. Here's where the PDF generation happens.
        #     # See the ReportLab documentation for the full list of functionality.
        #     p.drawString(100, 100, "Hello world.")
        #
        #     # Close the PDF object cleanly.
        #     p.showPage()
        #     p.save()
        #
        #     # Get the value of the BytesIO buffer and write it to the response.
        #     pdf = buffer.getvalue()
        #     buffer.close()
        #     response.write(pdf)
        #     return response

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


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    list_display = ("email",)
    ordering = ("email",)
    # refine the fields

    fieldsets = (
        (
        None, {'fields': ('email', 'password', 'first_name', 'last_name', 'groups', 'last_login', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active', 'groups',
            'last_login', 'user_permissions')}
         ),
    )

    search_fields = ('first_name', 'last_name', 'email',)


admin.site.register(CustomUser, CustomUserAdmin)



# admin.site.register(Specialization)

# admin.site.register(Diagnostic)
#
# admin.site.register(Consultation)

# admin.site.register(ConsultationResult, FilterByUser)
