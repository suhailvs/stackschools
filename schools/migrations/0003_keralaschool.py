# Generated by Django 4.0.1 on 2022-01-31 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0002_auditentry_generalsettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeralaSchool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.IntegerField(unique=True)),
                ('district', models.CharField(max_length=30)),
                ('edu_district', models.CharField(max_length=30)),
                ('sub_district', models.CharField(max_length=30)),
                ('url_id', models.IntegerField(blank=True, null=True)),
                ('hs_phone', models.CharField(blank=True, max_length=30)),
                ('hse_phone', models.CharField(blank=True, max_length=30)),
                ('hs_email', models.CharField(blank=True, max_length=200)),
                ('hse_email', models.CharField(blank=True, max_length=200)),
                ('headmaster_name', models.CharField(blank=True, max_length=200)),
                ('lat', models.CharField(blank=True, max_length=30)),
                ('lon', models.CharField(blank=True, max_length=30)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('img_src', models.TextField(blank=True)),
                ('mal_address', models.TextField(blank=True)),
                ('website', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]