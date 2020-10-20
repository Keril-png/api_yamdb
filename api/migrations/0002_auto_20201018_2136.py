# Generated by Django 3.0.5 on 2020-10-18 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles_of_category', to='api.Category'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles_of_genre', to='api.Genre'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveIntegerField(),
        ),
    ]