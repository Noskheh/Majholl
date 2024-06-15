
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options) :
        from functions import check_valid_inovices
        check_valid_inovices.change_inovice_status()