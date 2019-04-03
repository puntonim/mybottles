# Generated by Django 2.2 on 2019-04-03 21:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bottle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('creation_ts', models.DateTimeField(auto_now_add=True)),
                ('update_ts', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('alcohol', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('price_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('price_original', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('bottle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Bottle')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Store')),
            ],
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('winery_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Location')),
            ],
            options={
                'unique_together': {('name', 'winery_location')},
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='photos/')),
                ('bottle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Bottle')),
            ],
        ),
        migrations.AddField(
            model_name='bottle',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Producer'),
        ),
        migrations.AddField(
            model_name='bottle',
            name='vineyard_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Location'),
        ),
    ]
