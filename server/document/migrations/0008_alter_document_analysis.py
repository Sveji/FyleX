# Generated by Django 5.1.7 on 2025-03-21 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0007_alter_document_analysis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='analysis',
            field=models.JSONField(default=[]),
        ),
    ]
