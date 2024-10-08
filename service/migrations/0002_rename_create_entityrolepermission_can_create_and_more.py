# Generated by Django 5.1.1 on 2024-09-28 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entityrolepermission',
            old_name='create',
            new_name='can_create',
        ),
        migrations.RenameField(
            model_name='entityrolepermission',
            old_name='delete',
            new_name='can_delete',
        ),
        migrations.RenameField(
            model_name='entityrolepermission',
            old_name='read',
            new_name='can_read',
        ),
        migrations.RenameField(
            model_name='entityrolepermission',
            old_name='update',
            new_name='can_update',
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='custom_user_set', to='auth.group'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='custom_user_set', to='auth.permission'),
        ),
        migrations.AlterField(
            model_name='company',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(related_name='users', to='service.role'),
        ),
        migrations.AlterUniqueTogether(
            name='entityrolepermission',
            unique_together={('role', 'entity')},
        ),
    ]
