# Generated by Django 5.2.3 on 2025-06-18 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_design', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imageinlist',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='imageinlist',
            unique_together=set(),
        ),
        migrations.AlterOrderWithRespectTo(
            name='imageinlist',
            order_with_respect_to='image_list',
        ),
        migrations.AddField(
            model_name='imageinlist',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False, verbose_name='order'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='imageinlist',
            name='position',
        ),
    ]
