# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, DEFAULT_DB_ALIAS

from django.core.management.commands import loaddata


def load_data(apps, schema_editor):

    c = loaddata.Command()
    c.handle('widgets/fixtures/users.json', **{'database':DEFAULT_DB_ALIAS, 'verbosity': 0, 'ignore': False})
    c.handle('widgets/fixtures/widgets.json', **{'database':DEFAULT_DB_ALIAS, 'verbosity': 0, 'ignore': False})

def fake_reverse(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data, fake_reverse),
    ]

