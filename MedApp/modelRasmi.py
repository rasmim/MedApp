from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.models import (
    BaseUserManager
)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff,is_doctor, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,is_doctor=is_doctor, is_active=True,
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
    is_doctor = models.BooleanField(_('doctor'), default=True, help_text=_('Determine if the user is a doctor or not'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return u"%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):              # __unicode__ on Python 2
        return u"%s" % self.first_name

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

class Patient(models.Model):
    cnp = models.CharField(max_length=35, primary_key=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=20)
    address = models.TextField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.cnp)


class Specialization(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Diagnostic(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=200)


class Consultation(models.Model):

    # date = models.DateField()
    doctor = models.ForeignKey(CustomUser, related_name="consultation",
                               on_delete=models.SET_NULL, null=True, limit_choices_to={'groups__in': [1]})
    time = models.DateTimeField()
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, related_name="consultation", null = True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, related_name="consultation", null= True)

class Appointment(models.Model):
    time = models.DateTimeField()
    doctor = models.ForeignKey(CustomUser, related_name="appointments",
                               on_delete=models.SET_NULL, null= True, limit_choices_to={'groups__in': [1]})
    created_by = models.ForeignKey(CustomUser, related_name="appointments_created_by_me", on_delete=models.SET_NULL, null = True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, related_name="appointments", null= True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, related_name="appointments", null = True)

    def __str__(self):
        return "{} {} {}".format(self.specialization, self.patient, self.created_by)

class ConsultationResult(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.SET_NULL, related_name="ConsultationResult", null = True )
    consultation = models.ForeignKey(Consultation, on_delete=models.SET_NULL, related_name="ConsultationResult", null = True)
    image = models.ImageField()
    recipe = models.TextField()





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
