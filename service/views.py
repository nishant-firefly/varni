# from django.shortcuts import render

# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from .models import User, Role, Company, Entity, EntityRolePermission
# from .serializers import UserSerializer, RoleSerializer, CompanySerializer, EntitySerializer, EntityRolePermissionSerializer
# from django.contrib.auth import get_user_model

# User = get_user_model()

# @api_view(['GET', 'POST'])
# def user_list(request):
#     if request.method == 'GET':
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def create_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def get_user(request, user_id):
#     user = User.objects.filter(id=user_id).first()
#     if user:
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#     return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['POST'])
# def create_role(request):
#     serializer = RoleSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "Role created successfully", "role_id": serializer.data['id']}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def create_company(request):
#     serializer = CompanySerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "Company created successfully", "company_id": serializer.data['id']}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def create_entity(request):
#     serializer = EntitySerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "Entity created successfully", "entity_id": serializer.data['id']}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def assign_role_to_user(request, user_id, role_id):
#     user = User.objects.filter(id=user_id).first()
#     role = Role.objects.filter(id=role_id).first()
#     if user and role:
#         user.roles.add(role)
#         return Response({"message": f"Role {role.name} assigned to user {user.username}"})
#     return Response({"detail": "User or Role not found"}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['POST'])
# def grant_entity_permissions(request, role_id, entity_id):
#     role = Role.objects.filter(id=role_id).first()
#     entity = Entity.objects.filter(id=entity_id).first()
#     if role and entity:
#         serializer = EntityRolePermissionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(role=role, entity=entity)
#             return Response({"message": "Permissions granted successfully"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     return Response({"detail": "Role or Entity not found"}, status=status.HTTP_404_NOT_FOUND)


# # Create your views here.


#2.view***************************************************************************

# from django.contrib import admin
# from .models import User, Role, Company, Entity, EntityRolePermission, Project, ClockInConfiguration, ClockInMonthly, ClockInWeekly

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
#     list_display = ('role', 'entity', 'can_create', 'can_read', 'can_update', 'can_delete')
#     list_filter = ('role', 'entity')
#     search_fields = ('role__name', 'entity__entity_label')

# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     search_fields = ('name',)

# @admin.register(ClockInConfiguration)
# class ClockInConfigurationAdmin(admin.ModelAdmin):
#     list_display = ('configuration_name', 'settings')

# @admin.register(ClockInMonthly)
# class ClockInMonthlyAdmin(admin.ModelAdmin):
#     list_display = ('user', 'date', 'hours_worked')

# @admin.register(ClockInWeekly)
# class ClockInWeeklyAdmin(admin.ModelAdmin):
#     list_display = ('user', 'week_start', 'hours_worked')

#****************************************************************************************

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .models import (
    Role, Entity, EntityRolePermission, Company, Project, UserProject,
    PersonalInformation, AddressHistory, Education, EmploymentHistory, PastReference,
    ClockInConfiguration, ClockInMonthly, ClockInWeekly, Home
)
from .serializers import (
    UserSerializer, RoleSerializer, EntitySerializer, EntityRolePermissionSerializer, CompanySerializer,
    ProjectSerializer, UserProjectSerializer, PersonalInformationSerializer, AddressHistorySerializer,
    EducationSerializer, EmploymentHistorySerializer, PastReferenceSerializer,
    ClockInConfigurationSerializer, ClockInMonthlySerializer, ClockInWeeklySerializer, HomeSerializer
)

User = get_user_model()

# ====================
# Auth APIs
# ====================

@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_otp(request):
    # Logic for logging in with OTP
    return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_password(request):
    # Logic for logging in with email and password
    return Response({"message": "Login successful"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    # Logic for requesting password reset via email
    return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def change_password(request):
    # Logic for resetting password via OTP
    return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    # Logic for verifying the OTP
    return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def token_refresh(request):
    # Logic for refreshing the token
    return Response({"message": "Token refreshed successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def auth_configuration(request):
    # Logic for fetching authentication configuration
    return Response({"config": "Auth Configuration"}, status=status.HTTP_200_OK)


# ====================
# Admin Menu APIs
# ====================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def roles(request):
    if request.method == 'GET':
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def role_to_user_mapping(request):
    user_id = request.data.get('user_id')
    role_id = request.data.get('role_id')
    
    try:
        user = User.objects.get(id=user_id)
        role = Role.objects.get(id=role_id)
        user.roles.add(role)
        return Response({"message": "Role mapped to user successfully"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Role.DoesNotExist:
        return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def entity(request):
    if request.method == 'GET':
        entities = Entity.objects.all()
        serializer = EntitySerializer(entities, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EntitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        entity_id = request.data.get('id')
        try:
            entity = Entity.objects.get(id=entity_id)
            serializer = EntitySerializer(entity, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Entity.DoesNotExist:
            return Response({"error": "Entity not found"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        entity_id = request.data.get('id')
        try:
            entity = Entity.objects.get(id=entity_id)
            entity.delete()
            return Response({"message": "Entity deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Entity.DoesNotExist:
            return Response({"error": "Entity not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def entity_role_permissions(request):
    if request.method == 'GET':
        permissions = EntityRolePermission.objects.all()
        serializer = EntityRolePermissionSerializer(permissions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EntityRolePermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def company(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        company_id = request.data.get('id')
        try:
            company = Company.objects.get(id=company_id)
            serializer = CompanySerializer(company, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        company_id = request.data.get('id')
        try:
            company = Company.objects.get(id=company_id)
            company.delete()
            return Response({"message": "Company deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def projects(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        project_id = request.data.get('id')
        try:
            project = Project.objects.get(id=project_id)
            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        project_id = request.data.get('id')
        try:
            project = Project.objects.get(id=project_id)
            project.delete()
            return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_projects(request):
    if request.method == 'GET':
        user_projects = UserProject.objects.all()
        serializer = UserProjectSerializer(user_projects, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ====================
# Personal Information and History
# ====================

@api_view(['GET', 'POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def personal_information(request):
    if request.method == 'GET':
        user = request.user
        try:
            personal_info = PersonalInformation.objects.get(user=user)
            serializer = PersonalInformationSerializer(personal_info)
            return Response(serializer.data)
        except PersonalInformation.DoesNotExist:
            return Response({"error": "Personal information not found"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        serializer = PersonalInformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        try:
            personal_info = PersonalInformation.objects.get(user=request.user)
            serializer = PersonalInformationSerializer(personal_info, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PersonalInformation.DoesNotExist:
            return Response({"error": "Personal information not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def address_history(request):
    if request.method == 'GET':
        addresses = AddressHistory.objects.filter(user=request.user)
        serializer = AddressHistorySerializer(addresses, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AddressHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        address_id = request.data.get('id')
        try:
            address = AddressHistory.objects.get(id=address_id, user=request.user)
            serializer = AddressHistorySerializer(address, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AddressHistory.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        address_id = request.data.get('id')
        try:
            address = AddressHistory.objects.get(id=address_id, user=request.user)
            address.delete()
            return Response({"message": "Address deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except AddressHistory.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def education(request):
    if request.method == 'GET':
        education = Education.objects.filter(user=request.user)
        serializer = EducationSerializer(education, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        education_id = request.data.get('id')
        try:
            education = Education.objects.get(id=education_id, user=request.user)
            serializer = EducationSerializer(education, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Education.DoesNotExist:
            return Response({"error": "Education record not found"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        education_id = request.data.get('id')
        try:
            education = Education.objects.get(id=education_id, user=request.user)
            education.delete()
            return Response({"message": "Education record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Education.DoesNotExist:
            return Response({"error": "Education record not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def employment_history(request):
    if request.method == 'GET':
        employment = EmploymentHistory.objects.filter(user=request.user)
        serializer = EmploymentHistorySerializer(employment, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EmploymentHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        employment_id = request.data.get('id')
        try:
            employment = EmploymentHistory.objects.get(id=employment_id, user=request.user)
            serializer = EmploymentHistorySerializer(employment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmploymentHistory.DoesNotExist:
            return Response({"error": "Employment record not found"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        employment_id = request.data.get('id')
        try:
            employment = EmploymentHistory.objects.get(id=employment_id, user=request.user)
            employment.delete()
            return Response({"message": "Employment record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except EmploymentHistory.DoesNotExist:
            return Response({"error": "Employment record not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def past_references(request):
    if request.method == 'GET':
        references = PastReference.objects.filter(user=request.user)
        serializer = PastReferenceSerializer(references, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PastReferenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        reference_id = request.data.get('id')
        try:
            reference = PastReference.objects.get(id=reference_id, user=request.user)
            serializer = PastReferenceSerializer(reference, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PastReference.DoesNotExist:
            return Response({"error": "Reference not found"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        reference_id = request.data.get('id')
        try:
            reference = PastReference.objects.get(id=reference_id, user=request.user)
            reference.delete()
            return Response({"message": "Reference deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except PastReference.DoesNotExist:
            return Response({"error": "Reference not found"}, status=status.HTTP_404_NOT_FOUND)


# ====================
# Clock In APIs
# ====================

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def clock_in_configuration(request):
    if request.method == 'GET':
        configurations = ClockInConfiguration.objects.all()
        serializer = ClockInConfigurationSerializer(configurations, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ClockInConfigurationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        config_id = request.data.get('id')
        try:
            config = ClockInConfiguration.objects.get(id=config_id)
            serializer = ClockInConfigurationSerializer(config, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ClockInConfiguration.DoesNotExist:
            return Response({"error": "Configuration not found"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        config_id = request.data.get('id')
        try:
            config = ClockInConfiguration.objects.get(id=config_id)
            config.delete()
            return Response({"message": "Configuration deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ClockInConfiguration.DoesNotExist:
            return Response({"error": "Configuration not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def clock_in_monthly(request):
    if request.method == 'GET':
        clock_in_data = ClockInMonthly.objects.filter(user=request.user)
        serializer = ClockInMonthlySerializer(clock_in_data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ClockInMonthlySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        clock_in_id = request.data.get('id')
        try:
            clock_in = ClockInMonthly.objects.get(id=clock_in_id, user=request.user)
            serializer = ClockInMonthlySerializer(clock_in, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ClockInMonthly.DoesNotExist:
            return Response({"error": "Clock-in data not found"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        clock_in_id = request.data.get('id')
        try:
            clock_in = ClockInMonthly.objects.get(id=clock_in_id, user=request.user)
            clock_in.delete()
            return Response({"message": "Clock-in data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ClockInMonthly.DoesNotExist:
            return Response({"error": "Clock-in data not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def clock_in_weekly(request):
    if request.method == 'GET':
        clock_in_data = ClockInWeekly.objects.filter(user=request.user)
        serializer = ClockInWeeklySerializer(clock_in_data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ClockInWeeklySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        clock_in_id = request.data.get('id')
        try:
            clock_in = ClockInWeekly.objects.get(id=clock_in_id, user=request.user)
            serializer = ClockInWeeklySerializer(clock_in, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ClockInWeekly.DoesNotExist:
            return Response({"error": "Clock-in data not found"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        clock_in_id = request.data.get('id')
        try:
            clock_in = ClockInWeekly.objects.get(id=clock_in_id, user=request.user)
            clock_in.delete()
            return Response({"message": "Clock-in data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ClockInWeekly.DoesNotExist:
            return Response({"error": "Clock-in data not found"}, status=status.HTTP_404_NOT_FOUND)


# ====================
# Home API
# ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    # Logic for home API content
    home_content = Home.objects.first()  # Fetch the first or default content
    if home_content:
        serializer = HomeSerializer(home_content)
        return Response(serializer.data)
    else:
        return Response({"message": "Welcome to the home page!"}, status=status.HTTP_200_OK)

