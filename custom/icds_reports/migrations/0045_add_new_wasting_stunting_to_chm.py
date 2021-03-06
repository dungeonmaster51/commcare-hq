# Generated by Django 1.11.12 on 2018-04-23 19:03
from corehq.sql_db.operations import RawSQLMigration
from django.db import migrations

from custom.icds_reports.const import SQL_TEMPLATES_ROOT

migrator = RawSQLMigration((SQL_TEMPLATES_ROOT,))


class Migration(migrations.Migration):

    dependencies = [
        ('icds_reports', '0044_add_muac_grading'),
    ]

    operations = [
        migrator.get_migration('update_tables21.sql'),
    ]
