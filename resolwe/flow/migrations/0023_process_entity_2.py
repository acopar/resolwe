# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-10-01 03:15
from __future__ import unicode_literals

from django.db import migrations


def migrate_flow_collection(apps, schema_editor):
    """Migrate 'flow_collection' field to 'entity_type'."""
    Process = apps.get_model('flow', 'Process')
    DescriptorSchema = apps.get_model('flow', 'DescriptorSchema')

    for process in Process.objects.all():
        process.entity_type = process.flow_collection
        process.entity_descriptor_schema = process.flow_collection

        if not DescriptorSchema.objects.filter(slug=process.entity_descriptor_schema).exists():
            raise LookupError(
                "Descriptow schema '{}' referenced in 'entity_descriptor_schema' not "
                "found.".format(process.entity_descriptor_schema)
            )

        process.save()


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0022_process_entity_1'),
    ]

    operations = [
        migrations.RunPython(migrate_flow_collection)
    ]
