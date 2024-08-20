from django.core.management.base import BaseCommand
from mainrobot.models import admins , botsettings
import getpass , os , time , main 


#/run the bot
class Command(BaseCommand):
    def handle(self , *args , **options):

        if not admins.objects.all().exists():
            clear_console()
            self.stdout.write(self.style.HTTP_INFO('--- Creating Owner Bot !! ----\n \t Notice that this is done for first time next it will be loaded from db'))

            get_user_id = input(self.style.HTTP_INFO('stpe-1 : Send me OWNER user id >>? '))
            get_token_bot = input(self.style.HTTP_INFO('step-2 : Send me your token bot >>?'))
            get_user_passwd = getpass.getpass(self.style.HTTP_INFO('step-3 : Send me a password >>? '))
            confirmation_passwd  = getpass.getpass(self.style.HTTP_INFO('step-4 : Send me password again >>?'))
            
            is_owner = input(self.style.HTTP_INFO('step-5 : Is owner (true/false) >>?'))
            time.sleep(2)

            if get_user_passwd != confirmation_passwd :
                self.stdout.write(self.style.ERROR('Passwords do not match. Exiting...'))
                return
            if  is_owner in ['true' , 'false' , 't' , 'f', 'True', 'False', 'yes','yes' ,'No','no']:
                owner = 1 
                
            admins.objects.create(user_id = get_user_id , is_admin = owner , is_owner = owner , password=get_user_passwd , admin_name ='Owner' , acc_botmanagment=0, acc_panels=0, acc_products=0, acc_admins=0 , acc_users=0)
            botsettings.objects.create(wallet_pay = 0, kartbkart_pay=0, forcechjoin=0, moneyusrtousr=0)
            self.stdout.write(self.style.SUCCESS('Successfully !! Owner bot added to db'))
            write_token(get_token_bot)
   



            time.sleep(3.5)
            clear_console()

            main.bot.token = get_token_bot
            main.bot.send_message(get_user_id, 'بات شما با موفقیت نصب شد ✅ \n برای شروع دستور : /start را بفرستید')
            self.stdout.write('bot is running' , self.style.HTTP_SUCCESS )
            main.bot.infinity_polling()
            #main.bot.polling(non_stop=True)


        else :
            clear_console()  
            
            i = 3
            while True:
                if i > 0 :
                    self.stdout.write(f'running in : {i}')
                    time.sleep(1.5)
                    clear_console()
                    i -=1
                else :
                    break 
            time.sleep(2)
            clear_console()
            
            self.stdout.write('--! Bot is Running !--' , self.style.HTTP_SUCCESS ,)   
            main.bot.infinity_polling()
            #main.bot.polling(non_stop=True)




#/ write token
def write_token(token):
    with open('BOTTOKEN.py' , 'w+') as f:
            f.write(f'TOKEN=["{token}"]')
            f.close()


#/ clear console
def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
