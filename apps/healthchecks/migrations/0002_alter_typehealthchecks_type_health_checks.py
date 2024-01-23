# Generated by Django 5.0.1 on 2024-01-23 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthchecks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typehealthchecks',
            name='type_health_checks',
            field=models.CharField(choices=[('I', 'Exame de imagem'), ('S', 'Exame de sangue'), ('U', 'Exame de urina'), ('D', 'Exame de DNA')], max_length=1),
        ),
    ]