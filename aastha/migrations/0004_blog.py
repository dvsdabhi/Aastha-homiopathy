# Generated by Django 5.2.3 on 2025-07-02 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aastha', '0003_treatmentcategory_treatment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
