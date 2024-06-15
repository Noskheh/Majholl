from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self , *args , **options):
        import main 
        main.bot.polling(non_stop= True )
