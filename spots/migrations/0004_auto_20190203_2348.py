# Generated by Django 2.1.5 on 2019-02-03 14:48

from django.db import migrations, models
import spots.models


class Migration(migrations.Migration):

    dependencies = [("spots", "0003_auto_20190203_2346")]

    operations = [
        migrations.AlterField(
            model_name="spot",
            name="business_status",
            field=models.CharField(
                blank=True, choices=[(spots.models.BusinessStatus("Closed"), "Closed")], max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="spot", name="business_status_confirm_time", field=models.DateTimeField(blank=True, null=True)
        ),
    ]
