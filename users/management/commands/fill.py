import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Loads the groups fixture'

    def handle(self, *args, **options):
        with open('groups.json') as f:
            data = json.load(f)

        for group_data in data:
            group, created = Group.objects.get_or_create(name=group_data['fields']['name'])
            if created:
                self.stdout.write(f'Created group "{group.name}"')
            else:
                self.stdout.write(f'Group "{group.name}" already exists')