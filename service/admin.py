

# # Register your models here.




# from django.contrib import admin
# from .models import User, Role, Company, Entity, EntityRolePermission

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'is_active', 'is_email_verified', 'is_staff')
#     list_filter = ('is_active', 'is_staff')
#     search_fields = ('username', 'email')

# @admin.register(Role)
# class RoleAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)

# @admin.register(Company)
# class CompanyAdmin(admin.ModelAdmin):
#     list_display = ('name', 'code', 'contact_number', 'contact_email')
#     search_fields = ('name', 'code')

# @admin.register(Entity)
# class EntityAdmin(admin.ModelAdmin):
#     list_display = ('entity_label', 'url', 'dashboard_url')
#     search_fields = ('entity_label',)

# @admin.register(EntityRolePermission)
# class EntityRolePermissionAdmin(admin.ModelAdmin):
#     list_display = ('role', 'entity', 'can_create', 'can_read', 'can_update', 'can_delete')  # Updated field names
#     list_filter = ('role', 'entity')
#     search_fields = ('role__name', 'entity__entity_label')



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Role, Entity, EntityRolePermission, Company, Project, UserProject,
    PersonalInformation, AddressHistory, Education, EmploymentHistory, PastReference,
    ClockInConfiguration, ClockInMonthly, ClockInWeekly, Home
)


# ====================
# Custom User Admin
# ====================

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_email_verified', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username')}),
        ('Permissions', {'fields': ('is_active', 'is_email_verified', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_email_verified', 'is_staff', 'is_superuser'),
        }),
    )


# ====================
# Role Admin
# ====================

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# ====================
# Entity Admin
# ====================

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('entity_label', 'url', 'dashboard_url')
    search_fields = ('entity_label', 'url')


# ====================
# Entity Role Permission Admin
# ====================

@admin.register(EntityRolePermission)
class EntityRolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'entity', 'can_create', 'can_read', 'can_update', 'can_delete')
    list_filter = ('role', 'entity')
    search_fields = ('role__name', 'entity__entity_label')


# ====================
# Company Admin
# ====================

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'contact_number', 'contact_email')
    search_fields = ('name', 'code', 'contact_email')


# ====================
# Project Admin
# ====================

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'company')
    search_fields = ('name', 'company__name')


# ====================
# User Project Admin
# ====================

@admin.register(UserProject)
class UserProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')
    search_fields = ('user__username', 'project__name')


# ====================
# Personal Information Admin
# ====================

@admin.register(PersonalInformation)
class PersonalInformationAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'contact_number')
    search_fields = ('user__username', 'contact_number')


# ====================
# Address History Admin
# ====================

@admin.register(AddressHistory)
class AddressHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'start_date', 'end_date')
    search_fields = ('user__username', 'address')


# ====================
# Education Admin
# ====================

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree', 'institution', 'year_of_graduation')
    search_fields = ('user__username', 'degree', 'institution')


# ====================
# Employment History Admin
# ====================

@admin.register(EmploymentHistory)
class EmploymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'position', 'start_date', 'end_date')
    search_fields = ('user__username', 'company', 'position')


# ====================
# Past Reference Admin
# ====================

@admin.register(PastReference)
class PastReferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'reference_name', 'relation', 'reference_contact')
    search_fields = ('user__username', 'reference_name')


# ====================
# Clock-in Configuration Admin
# ====================

@admin.register(ClockInConfiguration)
class ClockInConfigurationAdmin(admin.ModelAdmin):
    list_display = ('configuration_name', 'settings')
    search_fields = ('configuration_name',)


# ====================
# Clock-in Monthly Admin
# ====================

@admin.register(ClockInMonthly)
class ClockInMonthlyAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'hours_worked')
    search_fields = ('user__username', 'date')


# ====================
# Clock-in Weekly Admin
# ====================

@admin.register(ClockInWeekly)
class ClockInWeeklyAdmin(admin.ModelAdmin):
    list_display = ('user', 'week_start', 'hours_worked')
    search_fields = ('user__username', 'week_start')


# ====================
# Home Admin
# ====================

@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('content',)
    search_fields = ('content',)
