# Generated by Django 5.1.4 on 2025-03-22 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacantes', '0021_alter_registrocandidato_aspiracion_salarial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrocandidato',
            name='registrado_en_sise',
            field=models.CharField(blank=True, choices=[('SI', 'Sí'), ('NO', 'No')], max_length=2, null=True),
        ),
    ]
