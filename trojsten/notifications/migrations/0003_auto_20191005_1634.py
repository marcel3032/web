# Generated by Django 2.1.9 on 2019-10-05 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("notifications", "0002_notification_created_at")]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="content_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.ContentType",
            ),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="object_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
