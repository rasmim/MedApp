from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.models import (
    BaseUserManager
)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _



from django.db.models.signals import pre_save
from django.dispatch import receiver
from send_sms import send_sms, client
from phonenumber_field.modelfields import PhoneNumberField





# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_doctor, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, verbose_name=_("First name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last name"))
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    # is_doctor = models.BooleanField(_('doctor'), default=True, help_text=_('Determine if the user is a doctor or not'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return u"%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):  # __unicode__ on Python 2

        return u"%s" % self.first_name

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class Patient(models.Model):
    cnp = models.CharField(max_length=35, primary_key=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=20)
    address = models.TextField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    sex_choices = (('M', 'Male'),
                   ('F', 'Female'),
                   )
    sex = models.CharField(max_length=20, choices=sex_choices, null=True)
    email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField(blank=True, help_text="Stick to this phone number format : +40phonenumber")
    doctor = models.ForeignKey(CustomUser, related_name="patient",
                               on_delete=models.SET_NULL, null=True)




    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.cnp)


class Specialization(models.Model):
    name = models.CharField(max_length=50)
    doctor = models.ForeignKey(CustomUser, related_name="specialization",
                               on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.name




class Diagnostic(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=200)
    specilization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, related_name='diagnostic', null=True)


    def __str__(self):
        return self.name


class Consultation(models.Model):
    # date = models.DateField()
    doctor = models.ForeignKey(CustomUser, related_name="consultation",
                               on_delete=models.SET_NULL, null=True, limit_choices_to={'groups__in': [1]})
    time = models.DateTimeField(auto_now_add=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, related_name="consultation",
                                       null=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, related_name="consultation", null=True)

    def get_patient_full_name(self):
        return "{} {}".format(self.patient.first_name, self.patient.last_name)

    def __str__(self):
        return "Doctor: {}\nPatient: {}".format(self.doctor, self.patient)


class Appointment(models.Model):
    time = models.DateTimeField(default=datetime.datetime.today())
    doctor = models.ForeignKey(CustomUser, related_name="appointments",
                               on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(CustomUser, related_name="appointments_created_by_me", on_delete=models.SET_NULL,
                                   null=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, related_name="appointments", null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, related_name="appointments",
                                       null=True)

    def get_(self):
        return "{}".format(self.time)


@receiver(pre_save, sender=Appointment)
def appointment_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        message = client.messages.create(to="+40784348384", from_="+447403938273",
                                         body="Dr. {} you have a new appointment at {}"
                                         .format(instance.doctor.get_full_name(),
                                                 instance.time.strftime("%d %b %Y %H:%M")))


class ConsultationResult(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.SET_NULL, related_name="ConsultationResult", null=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.SET_NULL, related_name="ConsultationResult",
                                     null=True)
    image = models.ImageField(upload_to='consultation')
    recipe = models.TextField()

    def patient(self):
        return "%s " % self.consultation.patient.last_name

    def image_tag(self):
        return u'<a href="%s%s" target="_blank"><img src="%s%s" style="width:100px" /></a>' % (settings.MEDIA_URL, self.image, settings.MEDIA_URL, self.image)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return "{} {}".format(self.diagnostic, self.recipe)


@receiver(pre_save, sender=ConsultationResult)
def cons_res_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        if instance.consultation.patient.email:

            send_mail('Consultation results',
                      'Hello, {} your diagnostic is {}.\n MedApp team advice you to take the following recipe:{}'.format(
                          instance.consultation.get_patient_full_name(), instance.diagnostic, instance.recipe),
                      'MedApp Team', ['{}'.format(instance.consultation.patient.email)], fail_silently=False)
        else:
            message = client.messages.create(to="{}".format(instance.consultation.patient.phone), from_="+447403938273",
                                             body="Mr/Mrs. {} you consultation result are ready. You can come to take them from MedApp Clinic."
                                             .format(instance.patient()))





            # class Recipe(models.Model):
        #     diag_consultation =  models.ForeignKey("DiagConsultation")
        #     drug = models.ForeignKey(Drugs)
        #     quantity = models.IntegerField()
        #     days = models.IntegerField()
        #     dosage = models.IntegerField()

        # class Drugs(models.Model):
        #     name = models.CharField(max_lenght = 40)
        #     administration = models.CharField(default="Oral, inhalable, nasal, ophthalmic")
        #     concentration = models.IntegerField()
        #     list_belog = models.CharField(default='A, B, C')



        # class SpecializationMedicine(models.Model):
        #     drug = models.ForeignKey(Drugs)
        #     specialization = models.ForeignKey(Specialization)
