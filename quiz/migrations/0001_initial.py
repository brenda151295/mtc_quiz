# Generated by Django 2.0.1 on 2018-01-19 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enunciado', models.CharField(max_length=256)),
                ('imagen_enunciado', models.ImageField(blank=True, null=True, upload_to='preguntas')),
                ('alternativa_1', models.CharField(max_length=256)),
                ('alternativa_2', models.CharField(max_length=256)),
                ('alternativa_3', models.CharField(max_length=256)),
                ('alternativa_4', models.CharField(max_length=256)),
                ('imagen_alternativa_1', models.ImageField(blank=True, null=True, upload_to='alternativas')),
                ('imagen_alternativa_2', models.ImageField(blank=True, null=True, upload_to='alternativas')),
                ('imagen_alternativa_3', models.ImageField(blank=True, null=True, upload_to='alternativas')),
                ('imagen_alternativa_4', models.ImageField(blank=True, null=True, upload_to='alternativas')),
                ('tema', models.CharField(choices=[('T1', 'Reglamento de Tránsito y Manual de Dispositivos de Control de Tránsito'), ('T2', 'Mercancías peligrosas'), ('T3', 'Reglamento Nacional de Vehículos'), ('T4', 'Funcionamiento del Sistema Nacional de Emisión de Licencias de Conducir'), ('T5', 'Mecánica para la conducción'), ('T6', 'Regulación de actividad de transporte'), ('T7', 'Mecánica avanzada para la conducción')], max_length=4)),
                ('alternativa_correcta', models.CharField(choices=[('a', '1'), ('b', '2'), ('c', '3'), ('d', '4')], max_length=1)),
            ],
        ),
    ]
