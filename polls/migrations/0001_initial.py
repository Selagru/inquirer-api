# Generated by Django 2.2.10 on 2020-08-03 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название опроса', max_length=255)),
                ('start_date', models.DateTimeField(auto_now_add=True, help_text='Дата старта')),
                ('end_date', models.DateTimeField(blank=True, help_text='Дата окончания', null=True)),
                ('description', models.TextField(help_text='Описание опроса')),
            ],
            options={
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(help_text='Текст вопроса', max_length=4096)),
                ('question_type', models.CharField(choices=[('text', 'ответ текстом'), ('single', 'ответ с выбором одного варианта'), ('multiple', 'ответ с выбором нескольких вариантов')], default='text', help_text='Тип вопроса', max_length=8)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Poll')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SingleChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Текст выбора', max_length=4096)),
                ('points', models.PositiveSmallIntegerField(help_text='Очков за выбор этого ответа')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question')),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Текст выбора', max_length=4096)),
                ('points', models.PositiveSmallIntegerField(help_text='Очков за выбор этого ответа')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(help_text='уникальный ключ браузерной сессии пользователя', max_length=32)),
                ('text', models.TextField(blank=True, help_text='Текстовый ответ пользователя', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Дата и время ответа')),
                ('multiple_choice', models.ManyToManyField(blank=True, to='polls.MultipleChoice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question')),
                ('single_choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='polls.SingleChoice')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
