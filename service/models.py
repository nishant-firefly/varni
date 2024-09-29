# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# class UserManager(BaseUserManager):
#     def create_user(self, email, username, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, username, password, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100, blank=True, null=True)
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(unique=True)
#     is_email_verified = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     roles = models.ManyToManyField('Role', related_name='users')

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     # Add the following lines to avoid conflicts
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='custom_user_set',  # Custom related name to avoid conflicts
#         blank=True,
#     )

#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='custom_user_set',  # Custom related name to avoid conflicts
#         blank=True,
#     )

#     def __str__(self):
#         return self.username

# class Role(models.Model):
#     name = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name

# class Company(models.Model):
#     name = models.CharField(max_length=100)
#     code = models.CharField(max_length=50, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     contact_number = models.CharField(max_length=20, blank=True, null=True)
#     contact_email = models.EmailField(blank=True, null=True)

#     def __str__(self):
#         return self.name

# class Entity(models.Model):
#     entity_label = models.CharField(max_length=100)
#     url = models.URLField(max_length=200)
#     dashboard_url = models.URLField(max_length=200, blank=True, null=True)

#     def __str__(self):
#         return self.entity_label

# class EntityRolePermission(models.Model):
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='entity_permissions')
#     entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='role_permissions')

#     can_create = models.BooleanField(default=False)
#     can_read = models.BooleanField(default=False)
#     can_update = models.BooleanField(default=False)
#     can_delete = models.BooleanField(default=False)

#     class Meta:
#         unique_together = ('role', 'entity')

#     def __str__(self):
#         return f"{self.role.name} - {self.entity.entity_label}"


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# ====================
# User Management
# ====================

class UserManager(BaseUserManager):
    """Custom user manager for handling user creation."""
    
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, username, password, **extra_fields)




class User(AbstractBaseUser, PermissionsMixin):
    # Your existing fields here
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Add custom related_name to avoid conflicts with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Custom related name
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Custom related name
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username





# ====================
# Roles and Permissions
# ====================

class Role(models.Model):
    """Role model to define different roles."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Entity(models.Model):
    """Model to represent different system entities."""
    entity_label = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    dashboard_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.entity_label


class EntityRolePermission(models.Model):
    """Model to define the permissions a role has on a particular entity."""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='entity_permissions')
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='role_permissions')
    
    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'entity')

    def __str__(self):
        return f"{self.role.name} - {self.entity.entity_label}"


# ====================
# Company and Projects
# ====================

class Company(models.Model):
    """Model to represent a company."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    """Model to represent a project within the company."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name


class UserProject(models.Model):
    """Model to represent the projects assigned to users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"


# ====================
# Personal Information and History
# ====================

class PersonalInformation(models.Model):
    """Model to store user's personal information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Personal Information"


class AddressHistory(models.Model):
    """Model to store user's address history."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Address History"


class Education(models.Model):
    """Model to store user's educational background."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    year_of_graduation = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.degree}"


class EmploymentHistory(models.Model):
    """Model to store user's employment history."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employment_history')
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.company}"


class PastReference(models.Model):
    """Model to store references provided by past employers."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='references')
    reference_name = models.CharField(max_length=100)
    reference_contact = models.CharField(max_length=100)
    relation = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - Reference"


# ====================
# Clock-in System
# ====================

class ClockInConfiguration(models.Model):
    """Model to configure the clock-in system."""
    configuration_name = models.CharField(max_length=100)
    settings = models.JSONField()

    def __str__(self):
        return self.configuration_name


class ClockInMonthly(models.Model):
    """Model to store clock-in data on a monthly basis."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    hours_worked = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class ClockInWeekly(models.Model):
    """Model to store clock-in data on a weekly basis."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start = models.DateField()
    hours_worked = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - Week {self.week_start}"


# ====================
# Home API Configuration
# ====================

class Home(models.Model):
    """Dummy model for home API response (if needed for storing info)."""
    content = models.TextField()

    def __str__(self):
        return "Home Page Content"
