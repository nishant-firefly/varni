# from rest_framework import serializers
# from .models import User, Role, Company, Entity, EntityRolePermission

# class RoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = ['id', 'name']

# class UserSerializer(serializers.ModelSerializer):
#     # Use RoleSerializer to properly handle the ManyToManyField
#     roles = RoleSerializer(many=True, read_only=True)

#     class Meta:
#         model = User
#         fields = ['id', 'first_name', 'last_name', 'username', 'email', 'roles']

# class CompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = ['id', 'name', 'code', 'address', 'contact_number', 'contact_email']

# class EntitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Entity
#         fields = ['id', 'entity_label', 'url', 'dashboard_url']

# class EntityRolePermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EntityRolePermission
#         fields = ['role', 'entity', 'can_create', 'can_read', 'can_update', 'can_delete']


from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Role, Entity, EntityRolePermission, Company, Project, UserProject,
    PersonalInformation, AddressHistory, Education, EmploymentHistory, PastReference,
    ClockInConfiguration, ClockInMonthly, ClockInWeekly, Home
)

User = get_user_model()

# ====================
# User and Auth Serializers
# ====================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'is_email_verified', 'is_active', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'is_email_verified']


# ====================
# Role and Permission Serializers
# ====================

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']
        read_only_fields = ['id']


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ['id', 'entity_label', 'url', 'dashboard_url']
        read_only_fields = ['id']


class EntityRolePermissionSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    entity = EntitySerializer(read_only=True)
    
    class Meta:
        model = EntityRolePermission
        fields = ['id', 'role', 'entity', 'can_create', 'can_read', 'can_update', 'can_delete']
        read_only_fields = ['id']


# ====================
# Company and Project Serializers
# ====================

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'code', 'address', 'contact_number', 'contact_email']
        read_only_fields = ['id']


class ProjectSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'company']
        read_only_fields = ['id']


class UserProjectSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = UserProject
        fields = ['id', 'user', 'project']
        read_only_fields = ['id']


# ====================
# Personal Information and History Serializers
# ====================

class PersonalInformationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PersonalInformation
        fields = ['id', 'user', 'bio', 'date_of_birth', 'contact_number']
        read_only_fields = ['id']


class AddressHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AddressHistory
        fields = ['id', 'user', 'address', 'start_date', 'end_date']
        read_only_fields = ['id']


class EducationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Education
        fields = ['id', 'user', 'degree', 'institution', 'year_of_graduation']
        read_only_fields = ['id']


class EmploymentHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EmploymentHistory
        fields = ['id', 'user', 'company', 'position', 'start_date', 'end_date']
        read_only_fields = ['id']


class PastReferenceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PastReference
        fields = ['id', 'user', 'reference_name', 'reference_contact', 'relation']
        read_only_fields = ['id']


# ====================
# Clock-in System Serializers
# ====================

class ClockInConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClockInConfiguration
        fields = ['id', 'configuration_name', 'settings']
        read_only_fields = ['id']


class ClockInMonthlySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ClockInMonthly
        fields = ['id', 'user', 'date', 'hours_worked']
        read_only_fields = ['id']


class ClockInWeeklySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ClockInWeekly
        fields = ['id', 'user', 'week_start', 'hours_worked']
        read_only_fields = ['id']


# ====================
# Home API Serializer
# ====================

class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ['id', 'content']
        read_only_fields = ['id']
