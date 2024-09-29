# import json
# from django.core.management.base import BaseCommand
# from service.models import Company, Role, User, Entity, EntityRolePermission

# class Command(BaseCommand):
#     help = 'Import external JSON file data into Django PGadmin database'

#     def handle(self,*args, **kwargs):
#         with open(r'D:\clockin_api\clockin_api\data\CLOCKIN.postman_collection.json', 'r', encoding='utf8') as file:
#             data=json.load(file)
#             # print(data)

#             for item in data:
#                 Company, Role, User, Entity, EntityRolePermission.objects.create(

#                 ) 



import json
from django.core.management.base import BaseCommand
from service.models import Company, Role, User, Entity, EntityRolePermission

class Command(BaseCommand):
    help = 'Import data from external JSON file into Django PostgreSQL database'

    def handle(self, *args, **kwargs):
        # Load the JSON file
        with open(r'D:\clockin_api\clockin_api\data\CLOCKIN.postman_collection.json', 'r', encoding='utf8') as file:
            data = json.load(file)
            # Assuming 'item' contains the data in the JSON structure
            for item in data['item']:
                # Company Data (replace with relevant fields)
                company_name = item.get('name', 'Default Company')
                company, created = Company.objects.get_or_create(
                    name=company_name,
                    defaults={
                        'code': 'CMP001',
                        'address': '123 Street, City',
                        'contact_number': '1234567890',
                        'contact_email': 'company@mail.com'
                    }
                )

                # Role Data
                role_name = item.get('role', {}).get('name', 'User')
                role, created = Role.objects.get_or_create(name=role_name)

                # User Data
                user_data = item.get('user', {})
                user, created = User.objects.get_or_create(
                    username=user_data.get('username', 'defaultuser'),
                    defaults={
                        'first_name': user_data.get('first_name', 'John'),
                        'last_name': user_data.get('last_name', 'Doe'),
                        'email': user_data.get('email', 'defaultuser@mail.com'),
                        'password': user_data.get('password', 'password'),
                        'is_email_verified': user_data.get('is_email_verified', False),
                        'is_active': user_data.get('is_active', True),
                    }
                )
                # Add Role to User
                user.roles.add(role)

                # Entity Data
                entity_label = item.get('entity', {}).get('entity_label', 'Default Entity')
                entity, created = Entity.objects.get_or_create(
                    entity_label=entity_label,
                    defaults={
                        'url': 'http://default.url',
                        'dashboard_url': 'http://dashboard.url'
                    }
                )

                # Entity Role Permission Data
                EntityRolePermission.objects.get_or_create(
                    role=role,
                    entity=entity,
                    defaults={
                        'create': item.get('permissions', {}).get('create', False),
                        'read': item.get('permissions', {}).get('read', False),
                        'update': item.get('permissions', {}).get('update', False),
                        'delete': item.get('permissions', {}).get('delete', False)
                    }
                )
            self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
