from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Delete all users'

    def handle(self, *args, **options):
        User = get_user_model()  
        User.objects.all().delete() 
        self.stdout.write(self.style.ERROR('Todos os usuários foram deletados com sucesso.'))
