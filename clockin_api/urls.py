"""
URL configuration for clockin_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""





# from django.contrib import admin
# from django.urls import path
# from service.views import (  # Make sure to import from service.views
#     user_list,
#     get_user,
#     create_role,
#     create_company,
#     create_entity,
#     assign_role_to_user,
#     grant_entity_permissions,
# )
# from clockin_api import views  # If you have other views in clockin_api

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.homePage),  # Ensure these functions are defined in clockin_api.views
#     path('Home/', views.home),
#     path('ClockinDetails/', views.ClockinDetails),
#     path('users/', user_list, name='user_list'),  # Updated to user_list
#     path('users/<int:user_id>/', get_user, name='get_user'),  # To get a user by ID
#     path('roles/', create_role, name='create_role'),  # To create a role
#     path('companies/', create_company, name='create_company'),  # To create a company
#     path('entities/', create_entity, name='create_entity'),  # To create an entity
#     path('users/<int:user_id>/roles/<int:role_id>/', assign_role_to_user, name='assign_role_to_user'),  # Assign role to user
#     path('roles/<int:role_id>/entities/<int:entity_id>/permissions/', grant_entity_permissions, name='grant_entity_permissions'),  # Grant permissions
# ]

from django.urls import path
from django.contrib import admin
from django.urls import path
from service.views import (
    login_with_otp,
    login_with_password,
    reset_password,
    change_password,
    verify_otp,
    token_refresh,
    user_registration,
    auth_configuration,
    roles,
    role_to_user_mapping,
    entity,
    entity_role_permissions,
    company,
    projects,
    user_projects,
    personal_information,
    address_history,
    education,
    employment_history,
    past_references,
    clock_in_configuration,
    clock_in_monthly,
    clock_in_weekly,
    home
)
from clockin_api import views  # If you have other views in clockin_api

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.homePage),  # Ensure these functions are defined in clockin_api.views
    path('Home/', views.home),
    path('ClockinDetails/', views.ClockinDetails),
    # Auth APIs
    path('noauth/api/login-via-email/', login_with_otp, name='login_with_otp'),
    path('noauth/api/login-via-email/password/', login_with_password, name='login_with_password'),
    path('noauth/api/reset/password/email/', reset_password, name='reset_password'),
    path('noauth/api/reset/password/email/otp/', change_password, name='change_password'),
    path('noauth/api/verify-otp/', verify_otp, name='verify_otp'),
    path('api/refresh-token/', token_refresh, name='token_refresh'),
    path('auth/user/registration/', user_registration, name='user_registration'),
    path('auth/configuration/', auth_configuration, name='auth_configuration'),

    # Admin Menu APIs
    path('api/roles/', roles, name='roles'),
    path('api/role-to-user-mapping/', role_to_user_mapping, name='role_to_user_mapping'),
    path('api/entity/', entity, name='entity'),
    path('api/entity-role-permissions/', entity_role_permissions, name='entity_role_permissions'),
    path('api/company/', company, name='company'),
    path('api/projects/', projects, name='projects'),
    path('api/user-projects/', user_projects, name='user_projects'),

    # Personal Information and History APIs
    path('api/personal-information/', personal_information, name='personal_information'),
    path('api/address-history/', address_history, name='address_history'),
    path('api/education/', education, name='education'),
    path('api/employment-history/', employment_history, name='employment_history'),
    path('api/past-references/', past_references, name='past_references'),

    # Clock-in APIs
    path('api/clockin-configuration/', clock_in_configuration, name='clock_in_configuration'),
    path('api/clockin-monthly/', clock_in_monthly, name='clock_in_monthly'),
    path('api/clockin-weekly/', clock_in_weekly, name='clock_in_weekly'),

    # Home API
    path('dashboard/clock-in/', home, name='home'),
]
