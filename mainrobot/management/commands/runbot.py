from django.core.management.base import BaseCommand
from mainrobot.models import admins , botsettings
from django.db import OperationalError, connection
import getpass , os , time , main , colorama
from TeleBot.settings import DATABASES




#/run the bot
class Command(BaseCommand):
    def handle(self , *args , **options):
        
            with open(os.getcwd()+'/mainrobot/management/commands/'+'dbinfo.py' , 'r') as f:
               
                if len(f.readline()) <= (6 or 8): 

                    clear_console()

                    print(self.style.HTTP_INFO(colorama.Fore.WHITE + " ... Creating DataBase ... " + colorama.Style.RESET_ALL))
                    db_name = input(colorama.Fore.BLUE + '\tGive me your database name >>?' + colorama.Style.RESET_ALL) 
                    
                    

                    if os.name =='posix':
                        os.system(f'sudo mysql -e CREATE DATABASE {db_name} || exit ; || python3 manage.py migrate')
                    else:
                        print(colorama.Fore.CYAN+ 'To connect to the database on windows you have to do it manally.' + colorama.Style.RESET_ALL)

                    DATABASES['default']['NAME'] = db_name

                    try :
                        ch = connection.cursor()
                        ch.execute("select 1")
                        reslut = ch.fetchone()
                        print(colorama.Fore.GREEN + f'Database connected Succsfully \n {reslut}'+ colorama.Style.RESET_ALL)
                        write_db_name(db_name)

                    except OperationalError as e:
                        print(f'Database connection failed : {e}')
                
                time.sleep(5)
            
            

            if not admins.objects.all().exists():
                print(colorama.Fore.GREEN + 'Database is Connected' + colorama.Style.RESET_ALL)

                self.stdout.write(self.style.HTTP_INFO('--- Creating Owner Bot !! ----\n \t Notice that this is done for first time next it will be loaded from db'))

                get_user_id = input(self.style.HTTP_INFO('stpe-1 : Send me OWNER user id >>? '))

                get_token_bot = input(self.style.HTTP_INFO('step-2 : Send me your token bot >>?'))


                get_user_passwd = getpass.getpass(self.style.HTTP_INFO('step-6 : Send me a password for owner >>? '))

                confirmation_passwd  = getpass.getpass(self.style.HTTP_INFO('step-7 : Send me password again >>?'))
                
                is_owner = input(self.style.HTTP_INFO('step-8 : Is owner (yes/NO) >>?'))
                time.sleep(2)

                if get_user_passwd != confirmation_passwd :
                    self.stdout.write(self.style.ERROR('Passwords do not match. Exiting...'))
                    return
                
                if  is_owner in ['true' , 'false' , 't' , 'f', 'True', 'False', 'yes','Yes' ,'No','no']:
                    
                    owner = 1 
                    
                admins.objects.create(user_id = get_user_id , is_admin = owner , is_owner = owner , password=get_user_passwd , admin_name ='Owner' , acc_botmanagment=0, acc_panels=0, acc_products=0, acc_admins=0 , acc_users=0, acc_staticts=0)
                
                botsettings.objects.create(wallet_pay = 0, kartbkart_pay=0, forcechjoin=0, moneyusrtousr=0, irnumber=0)
                
                self.stdout.write(self.style.SUCCESS('Successfully !! Owner bot added to db'))
                
                write_token(get_token_bot)

                time.sleep(3.5)
                
                clear_console()

                main.bot.token = get_token_bot

                main.bot.send_message(get_user_id, 'بات شما با موفقیت نصب شد ✅ \n برای شروع دستور : /start را بفرستید')
                
                self.stdout.write(colorama.Fore.GREEN + '--! Bot is Running !--' + colorama.Style.RESET_ALL)

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
                """"""
                
                self.stdout.write(colorama.Fore.GREEN + '--! Bot is Running !--' + colorama.Style.RESET_ALL)
                main.bot.infinity_polling()
                #main.bot.polling(non_stop=True)




#/ write token
def write_token(token):
    with open('BOTTOKEN.py' , 'w+') as f:
            f.write(f'TOKEN=["{token}"]')
            f.close()
            return




def write_db_name(dbname , dbuser=None, dbpass=None):
    with open(os.getcwd()+'/mainrobot/management/commands/'+'dbinfo.py' ,'w+') as f:
            f.write(f'db=["{dbname}"]')
            f.close()
            return



#/ clear console
def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
