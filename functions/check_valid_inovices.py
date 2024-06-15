from django.core.management.base import BaseCommand
from mainrobot.models import inovices
from datetime import datetime ,timedelta



def change_inovice_status():

    thirty_minutes_ago = datetime.now() - timedelta(minutes=30)
    invoices_to_update = inovices.objects.filter(paid_mode='kbk', paid_status = 2, created_date__lte=thirty_minutes_ago)
    if invoices_to_update :
        for invoice in invoices_to_update:
            invoice.paid_status = 0  # 0 > unpaid , 1 > paid , 2 > waiting , 3 > disagree
            invoice.save()
            print(f"Updated invoice {invoice.id} to unpaid status")
    else:
        print('noting found')



