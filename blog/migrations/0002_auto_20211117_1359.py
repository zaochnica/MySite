# Generated by Django 3.2.9 on 2021-11-17 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True, verbose_name='Номер телефона')),
                ('username', models.CharField(max_length=255, verbose_name='Имя клиента')),
                ('mail_adr', models.EmailField(max_length=254, verbose_name='Эл.почта')),
            ],
            options={
                'verbose_name': 'Неавторизованный пользователь',
                'verbose_name_plural': 'Неавторизованные пользователи',
            },
        ),
        migrations.AlterModelOptions(
            name='training',
            options={'ordering': ['-id'], 'verbose_name': 'Тренировку', 'verbose_name_plural': 'Тренировки'},
        ),
        migrations.AddField(
            model_name='training',
            name='format',
            field=models.CharField(blank=True, choices=[('group', 'group'), ('individual', 'individual'), ('personal', 'personal'), ('mini-group', 'mini-group')], max_length=20, null=True, verbose_name='Формат тренировок'),
        ),
        migrations.AlterField(
            model_name='training',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]