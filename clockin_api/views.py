from django.http import HttpResponse
from django.shortcuts import render

def homePage(request):
    return render(request,"index.html")

def home(request):
    return HttpResponse("Hello World")

def ClockinDetails(request):
    return HttpResponse("ClockinDetails")

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from service.models import Role, Entity, EntityRolePermission

User = get_user_model()

def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def role_list(request):
    roles = Role.objects.all()
    return render(request, 'roles/role_list.html', {'roles': roles})

def entity_list(request):
    entities = Entity.objects.all()
    return render(request, 'entities/entity_list.html', {'entities': entities})

def entity_role_permission_list(request):
    permissions = EntityRolePermission.objects.all()
    return render(request, 'permissions/permission_list.html', {'permissions': permissions})
