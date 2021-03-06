# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-16 07:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('text', models.CharField(blank=True, max_length=200)),
                ('val', models.CharField(blank=True, max_length=50)),
                ('addr', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BSS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('val', models.CharField(blank=True, max_length=50)),
                ('label', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Constant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=50)),
                ('val', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val', models.CharField(blank=True, max_length=50)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('label', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Eflag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cf', models.IntegerField(default=0)),
                ('zf', models.IntegerField(default=0)),
                ('sf', models.IntegerField(default=0)),
                ('of', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('num', models.IntegerField(default=1)),
                ('src', models.CharField(blank=True, max_length=50)),
                ('dest', models.CharField(blank=True, max_length=50)),
                ('label', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'ordering': ['num'],
            },
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('steps', models.IntegerField()),
                ('current_line', models.IntegerField(default=1)),
                ('filename', models.CharField(blank=True, max_length=50)),
                ('stdout', models.TextField(blank=True)),
                ('ccode', models.TextField(blank=True)),
                ('test', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('content', models.CharField(blank=True, max_length=50, null=True)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.Problem')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Rodata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('val', models.CharField(blank=True, max_length=50)),
                ('label', models.CharField(blank=True, max_length=50)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.Problem')),
            ],
        ),
        migrations.CreateModel(
            name='Stack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('val', models.CharField(blank=True, max_length=50)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.Problem')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val', models.CharField(default='*code text here*', max_length=50)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.Problem')),
            ],
        ),
        migrations.AddField(
            model_name='instruction',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.Problem'),
        ),
        migrations.AddField(
            model_name='eflag',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.Problem'),
        ),
        migrations.AddField(
            model_name='data',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.Problem'),
        ),
        migrations.AddField(
            model_name='constant',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.Problem'),
        ),
        migrations.AddField(
            model_name='bss',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.Problem'),
        ),
        migrations.AddField(
            model_name='arg',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.Problem'),
        ),
    ]
