from django.contrib.auth.models import User


def run():
    user, _ = User.objects.get_or_create(username='admin')
    user.set_password('admin')
    user.save()
