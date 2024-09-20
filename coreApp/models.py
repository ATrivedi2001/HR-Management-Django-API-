from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager,Permission,Group
from django.core.exceptions import ValidationError

# Create your models here.

class Leave(models.Model):
    LEAVE_TYPES = [
        ('Sick', 'Sick Leave'),
        ('Casual', 'Casual Leave'),
        ('Paid', 'Paid Leave'),
        ('Unpaid', 'Unpaid Leave'),
    ]

    LEAVE_STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    leave_id = models.IntegerField()
    leave_type = models.CharField(max_length=100, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=LEAVE_STATUS, default='Pending')

# *******************************************************************************************************************************************

class CustomUserManager(BaseUserManager):
    def _create_user(self, username, password, first_name, last_name, email, contact, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            contact=contact,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, first_name, last_name, email, contact, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, first_name, last_name, email, contact, **extra_fields)

    def create_superuser(self, username, password, first_name, last_name, email, contact, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, password, first_name, last_name, email, contact, **extra_fields)

# *******************************************************************************************************************************************

class User(AbstractBaseUser, PermissionsMixin):
    USER_GENDER = [
        ('Male','Male'),
        ('Female','Female')
        ]
    
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    email = models.EmailField()
    gender = models.CharField(max_length=50 , choices=USER_GENDER)
    contact = models.CharField(max_length=50)
    date_of_join = models.DateField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'email', 'gender', 'contact',]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    # Add custom related names to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='coreapp_user_groups',  # Avoids clash with auth.User.groups
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='coreapp_user_permissions',  # Avoids clash with auth.User.user_permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

# *******************************************************************************************************************************************

class Attendance(models.Model):
    ATTENDANCE = [
        ('Present','Present'),
        ('Absent','Absent')
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField()
    log_in = models.TimeField(blank=True)
    log_out = models.TimeField(blank=True)
    status = models.CharField(max_length=50,choices=ATTENDANCE)

# *******************************************************************************************************************************************


class Department(models.Model):
    department_name= models.CharField(max_length=50)
    description=models.CharField(max_length=50)
    hod=models.CharField(max_length=50)

# *******************************************************************************************************************************************

class Applicant(models.Model):
    APPLICANT_STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    # Custom validator to ensure only PDFs are uploaded
    def validate_pdf(file):
        if not file.name.endswith('.pdf'):
            raise ValidationError('Invalid file type. Only PDF files are allowed.')
    
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    phone_number=models.CharField(max_length=50)
    dob=models.DateField(blank=True,null=True)
    address=models.CharField(max_length=50)
    applicant_date=models.DateField(null=True)
    status=models.CharField(max_length=20,choices=APPLICANT_STATUS)
    resume = models.FileField(upload_to='Resume/', validators=[validate_pdf])


# *******************************************************************************************************************************************

# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
# from django.db import models

# class User(AbstractBaseUser, PermissionsMixin):
#     USER_GENDER = [
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#     ]
    
#     username = models.CharField(max_length=50)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     gender = models.CharField(max_length=50, choices=USER_GENDER)
#     contact = models.CharField(max_length=50)
#     date_of_join = models.DateField(null=True)

#     # Set USERNAME_FIELD and REQUIRED_FIELDS
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'gender', 'contact']

# 

  
