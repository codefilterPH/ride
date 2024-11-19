from django.core.management.base import BaseCommand
from ride.models import UserProfile  # Assuming UserProfile is your custom user model
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Create regular users (5 drivers and 5 riders)'

    def handle(self, *args, **kwargs):
        usernames = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9', 'user10']
        roles = ['driver', 'rider']  # Role choices for 5 drivers and 5 riders

        # Create drivers
        for i in range(5):
            username = usernames[i]
            if UserProfile.objects.filter(username=username).exists():
                self.stdout.write(self.style.SUCCESS(f"Driver user {username} already exists. Skipping creation."))
            else:
                password = get_random_string(8)  # Generate a random password
                user = UserProfile.objects.create_user(username=username, password=password, role='driver')
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Driver user created: {username}"))

        # Create riders
        for i in range(5, 10):
            username = usernames[i]
            if UserProfile.objects.filter(username=username).exists():
                self.stdout.write(self.style.SUCCESS(f"Rider user {username} already exists. Skipping creation."))
            else:
                password = get_random_string(8)  # Generate a random password
                user = UserProfile.objects.create_user(username=username, password=password, role='rider')
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Rider user created: {username}"))
