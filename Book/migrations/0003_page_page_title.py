# Generated by Django 5.0.7 on 2024-08-06 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0002_rename_choice_text_comment_comment_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='page_title',
            field=models.CharField(default='Test Page', max_length=50),
            preserve_default=False,
        ),
    ]
