# Generated by Django 4.2.8 on 2023-12-09 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일자')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일자')),
                ('is_complete', models.BooleanField(default=False, verbose_name='완료 여부')),
                ('completed_date', models.DateTimeField(blank=True, null=True, verbose_name='완료 일자')),
            ],
            options={
                'verbose_name': '하위 업무',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일자')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일자')),
                ('title', models.CharField(max_length=256, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('is_complete', models.BooleanField(default=False, verbose_name='완료 여부')),
                ('completed_date', models.DateTimeField(blank=True, null=True, verbose_name='완료 일자')),
            ],
            options={
                'verbose_name': '업무',
            },
        ),
    ]