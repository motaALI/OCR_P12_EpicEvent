from django.core.management.base import BaseCommand

from contractManager.models import Role


class Command(BaseCommand):
    help = "Populate roles in the database"

    def handle(self, *args, **options):
        ROLES_TO_CREATE = [
            {"name": Role.SALES},
            {"name": Role.MANAGEMENT},
            {"name": Role.SUPPORT},
        ]

        for role_data in ROLES_TO_CREATE:
            role, created = Role.objects.get_or_create(name=role_data["name"])
            if created:
                self.stdout.write(self.style.SUCCESS(f"Role '{role.name}' created."))
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"Role '{role.name}' already exists.")
                )
