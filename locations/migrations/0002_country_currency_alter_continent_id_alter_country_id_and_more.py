# Generated by Django 5.0.2 on 2024-06-30 13:30

import utils.snowflake
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="country",
            name="currency",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="continent",
            name="id",
            field=models.BigIntegerField(
                default=utils.snowflake.Snowflake.generate_id,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="country",
            name="id",
            field=models.BigIntegerField(
                default=utils.snowflake.Snowflake.generate_id,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="localgovernment",
            name="id",
            field=models.BigIntegerField(
                default=utils.snowflake.Snowflake.generate_id,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="state",
            name="id",
            field=models.BigIntegerField(
                default=utils.snowflake.Snowflake.generate_id,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
