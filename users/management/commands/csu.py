from django.core.management import BaseCommand
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):

        user = User.objects.create(
            email='admin@project.upit',
            first_name='Admin',
            last_name='Skypro',)
        user.is_staff=True
        user.is_superuser=True


        user.set_password('admin')
        user.save()