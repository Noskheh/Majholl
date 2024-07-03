from mainrobot.models import v2panel , products
from keybuttons import BotkeyBoard as BotKb
import random , string , time, re
#this is functions that managing panels




#-Adding panel to Database
def add_panel_database(panel_name , panel_url , panel_username , panel_password ,panel_information , message , BOT):
    panel_id_STRgenerated = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4))
    try :
        panel_=v2panel.objects.create(panel_name=panel_name , panel_url=panel_url , panel_username=panel_username , panel_password=panel_password , panel_id_str=panel_id_STRgenerated)
        panel_information.update({key: '' for key in panel_information })
        Text_1='✅.پنل با موفقیت به دیتابیس اضافه شد'
        BOT.send_message(message.chat.id , Text_1 , reply_markup=BotKb.panel_management_menu_in_admin_side())
    except Exception as panel_creation:
            print(f'Error during creating panel \n\t Error-msg : {panel_creation}')
            Text_2='❌هنگام اضافه کردن پنل به دیتابیس مشکلی به وجود امد \n\n مجددا امتحان فرمایید یا لاگ را بررسی کنید'
            BOT.send_message(message.chat.id , Text_2)





#-Removing panel from Database
def remove_panel_database(panel_id , BOT , call ,panel=None , product=None ):
    if product is not None:
        try :  
            panel_to_remove = v2panel.objects.get(id = panel_id).delete()
            BOT.answer_callback_query(call.id , 'در حال حذف کردن پنل...')

        except Exception as panel_remove :
            print(f'Error !! during removing panel \n\t Error-msg : {panel_remove}')
            BOT.send_message('مشکلی در حذف کردن پنل به وجود امد' , call.message.chat.id)

        time.sleep(2)
        try : 
            products_to_remove = products.objects.filter(panel_id = panel_id).delete()  
            BOT.answer_callback_query(call.id , 'در حال حذف کردن محصولات مرتبط با پنل ....')

        except Exception as products_remove:
            print(f'Error !! during removing panel\'s product \n\t Error-msg :  {products_remove}')
            
        time.sleep(2)
        Text_1='✅پنل و تمامی محصولات مرتبط با اون باموفقیت از دیتابیس پاک شدند '  
        BOT.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.panel_management_remove_panel())
    

    if panel is not None :
        try :  
            panel_to_remove = v2panel.objects.get(id = panel_id).delete()
            products_ = products.objects.filter(panel_id = panel_id).all()
            for i in products_:
                i.panel_id = None
                i.save()
            Text_2='✅پنل باموفقیت از دیتابیس پاک شد'  
            BOT.edit_message_text(Text_2 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.panel_management_remove_panel())
        except Exception as panel_remove :
            print(f'Error !! during removing panel \n\t Error-msg : {panel_remove}')
            BOT.send_message('مشکلی در حذف کردن پنل به وجود امد' , call.message.chat.id)




# Manageing Panel from Database
#- panel_STATUS
def change_panel_status(panel_id , BOT , call):
        try :
            panel_ = v2panel.objects.get(id = panel_id)
            panel_new_status = 0 if panel_.panel_status == 1 else 1
            panel_.panel_status = panel_new_status
            panel_.save()
        except Exception as changeing_status:
            print(f'Error during changing panel status \n\t Error-msg : {changeing_status}')
        Text_1=f'🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n وضعیت پنل تغییر کرد \n وضعیت فعلی : {"🟢فعال" if panel_.panel_status == 1 else "🔴غیر-فعال"}'
        Text_2=f'{"🟢فعال" if panel_.panel_status == 1 else "🔴غیر-فعال"}'
        BOT.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_selected_panel(panel_pk = panel_id))      
        BOT.answer_callback_query(call.id , Text_2)



#- panel_NAME
def change_panel_name(panel_id , BOT , message , panel_dict):      
    if panel_dict['Panel_Name']==True and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        Text_1='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n تغییر نام پنل لغو شد '
        panel_dict['Panel_Name']=False
        BOT.send_message(message.chat.id , Text_1 ,reply_markup = BotKb.manage_selected_panel(panel_pk=panel_id))   
    else:        
        try:
            panel_ = v2panel.objects.get(id = panel_id)
            panel_new_name = message.text 
            panel_.panel_name = panel_new_name
            panel_.save()
            panel_dict['Panel_Name']=False  
        except Exception as change_name:
            print(f'Error during changing panel name \n\t  Error-msg : {change_name}')
        Text_2='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n اسم پنل تغییر کرد \n دقت کنید که این تغییر در هنگام خرید سرویس نمایش داده خواهد شد'
        BOT.send_message(message.chat.id ,Text_2 , reply_markup=BotKb.manage_selected_panel(panel_pk=panel_id))




#- panel_URL
def change_panel_url(panel_id , BOT , message , panel_dict):
    if panel_dict['Panel_Url']==True and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        panel_dict['Panel_Url']=False
        Text_1='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n تغییر ادرس پنل لغو شد'
        BOT.send_message(message.chat.id , Text_1 , reply_markup=BotKb.manage_selected_panel(panel_pk=panel_id))
    else :
        pattern=(
                r'^(http|https):\/\/' 
                r'('
                    r'[\w.-]+'
                    r'|'
                    r'(\d{1,3}\.){3}\d{1,3}'
                r')'
                r'(:\d{1,5})?$'
                )   
        http_or_https_chekcer = re.search(pattern , message.text)
        
        if http_or_https_chekcer:
            try:
                panel_ = v2panel.objects.get(id=panel_id)
                panel_new_name = http_or_https_chekcer.group(0)
                panel_.panel_url = panel_new_name
                panel_.save()
                panel_dict['Panel_Url'] = False

            except Exception as change_url:
                print(f'Error during changing panel url \n\t  Error-msg : {change_url}')
            Text_2='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n اسم پنل تغییر کرد '
            BOT.send_message(message.chat.id ,Text_2 ,reply_markup=BotKb.manage_selected_panel(panel_pk= panel_id))
        else:
            Text_3='ادرس پنل اشتباه است\n فرمت های صحیح :\nhttp://panelurl.com:port\nhttps://panelurl.com:port\nhttp://ip:port\nhttps://ip:port\n\nTO CANCEL : /CANCEL'
            BOT.send_message(message.chat.id , Text_3)
 



#- panel_USERNAME
def change_panel_username(panel_id , BOT , message , panel_dict):
    if panel_dict['Panel_Username']==True and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        panel_dict['Panel_Username'] = False
        Text_1='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n تغییر یوزرنییم پنل لغو شد'
        BOT.send_message(message.chat.id ,  Text_1 ,reply_markup=BotKb.manage_selected_panel(panel_pk=panel_id))
    else:
        try:
            panel_=v2panel.objects.get(id=panel_id)
            panel_new_name=message.text 
            panel_.panel_username=panel_new_name
            panel_.save()
            panel_dict['Panel_Username']=False
        except Exception as change_username:
            print(f'Error during changing panel username \n\t  Error-msg : {change_username}')
        Text_2='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n یوزرنیم پنل تغییر کرد '
        BOT.send_message(message.chat.id , Text_2 , reply_markup=BotKb.manage_selected_panel(panel_pk = panel_id))
    


#- panel_PASSWORD
def change_panel_password(panel_id , BOT , message , panel_dict):
    if panel_dict['Panel_Password']==True and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        panel_dict['Panel_Password']=False
        Text_1='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n تغییر پسورد پنل لغو شد'    
        BOT.send_message(message.chat.id , Text_1 , reply_markup=BotKb.manage_selected_panel(panel_pk=panel_id))
    else : 
        try:
            panel_ = v2panel.objects.get(id=panel_id)
            panel_new_name = message.text 
            panel_.panel_password = panel_new_name
            panel_.save()
            panel_dict['Panel_Password']=False

        except Exception as change_password:
            print(f'Error during changing panel username \n\t  Error-msg : {change_password}')
        Text_2='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n پسورد پنل تغییر کرد '
        BOT.send_message(message.chat.id , Text_2 , reply_markup=BotKb.manage_selected_panel(panel_pk= panel_id))



#- panel_REALITYFLOW
def change_panel_realityflow(panel_id , BOT , call , reality=None , none_reality=None):
    Text_0='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n ریلیتی - فلو پنل تغییر کرد '
    if call.data=='xtls-rprx-vision' and reality is not None:
        try: 
            panel_=v2panel.objects.get(id=panel_id)
            panel_new_reality=call.data 
            panel_.reality_flow=panel_new_reality
            panel_.save()
        except Exception as change_reality:
            print(f'Error during changing panel reality \n\t  Error-msg : {change_reality}')
        BOT.edit_message_text(Text_0,call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_selected_panel(panel_pk=panel_id))

    if call.data=='None_realityFlow' and  none_reality is not None:
        
        try: 
            panel_=v2panel.objects.get(id=panel_id)
            panel_new_reality=call.data.split('_')[0].lower()
            panel_.reality_flow=panel_new_reality
            panel_.save()
        except Exception as change_nonereality:
            print(f'Error during changing panel username \n\t  Error-msg : {change_nonereality}')
        BOT.edit_message_text(Text_0 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_selected_panel(panel_pk=panel_id))


#- panel_CAPCITMODE                           
def change_panel_capcitymode(panel_id , BOT , call):
    panel_=v2panel.objects.get(id=panel_id)
    if panel_.capcity_mode==0:
        try:
            new_capcity=1
            panel_.capcity_mode=new_capcity
            panel_.save()
        except Exception as capcity_mode_1 :
            print(f'Error during changing panel capcity mode \n\t  Error-msg :{capcity_mode_1}')

    elif panel_.capcity_mode==1:
        try:
            new_capcity=2
            panel_.capcity_mode=new_capcity
            panel_.save()
        except Exception as capcity_mode_2 :
            print(f'Error during changing panel capcity mode \n\t  Error-msg :{capcity_mode_2}')

    else :
        try:
            new_capcity=0
            panel_.capcity_mode=new_capcity
            panel_.save()
        except Exception as capcity_mode_3 :
            print(f'Error during changing panel capcity mode \n\t  Error-msg :{capcity_mode_3}')
    Text_0='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n حالت ظرفیت  پنل تغییر کرد '
    BOT.edit_message_text(Text_0,call.message.chat.id , call.message.message_id , reply_markup=BotKb.changin_panel_capcity(panel_pk=panel_id))




#- panel_SALEMODE
def change_panel_salemode(panel_id , BOT , call):
    panel_ = v2panel.objects.get(id=panel_id)
    if panel_.panel_sale_mode==0:
        try:
            new_panel_sale_mode=1
            panel_.panel_sale_mode=new_panel_sale_mode
            panel_.save()
        except Exception as sale_mode_1 :
            print(f'Error during changing panel sale mode \n\t  Error-msg :{sale_mode_1}')
    else: 
        try:
            new_panel_sale_mode=0
            panel_.panel_sale_mode=new_panel_sale_mode
            panel_.save()
        except Exception as sale_mode_2 :
            print(f'Error during changing panel sale mode \n\t  Error-msg : {sale_mode_2}')
    Text_0='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n حالت فروش  پنل تغییر کرد '
    BOT.edit_message_text(Text_0 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.changin_panel_capcity(panel_pk=panel_id))
        



#- panel_ALLCAPCITY
def change_panel_allcapcity(panel_id , BOT , message , panel_dict):
    if panel_dict['All_Capcity']==True and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        panel_dict['All_Capcity']=False 
        Text_1='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n تغییر ظرفیت-کلی پنل لغو شد'  
        BOT.send_message(message.chat.id , Text_1 , reply_markup=BotKb.changin_panel_capcity(panel_pk=panel_id))
    else:
        if message.text.isdigit():
            try: 
                panel_=v2panel.objects.get(id=panel_id)
                panel_new_all_capcity=message.text
                panel_.all_capcity=panel_new_all_capcity
                panel_.save()
                panel_dict['All_Capcity']=False 
            except Exception as change_allcapcity :
                    print(f'Error during changing panel capcity changing \n\t  Error-msg : {change_allcapcity}')
            Text_2='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n ظرفیت-کلی پنل تغییر کرد '        
            BOT.send_message(message.chat.id , Text_2 , reply_markup=BotKb.changin_panel_capcity(panel_pk=panel_id))

        else: 
            Text_3='❌برای تغییر ظرفیت کلی پنل مقدار عددی ارسال کنید'
            BOT.send_message(message.chat.id  , Text_3)  



#- panel_QRCODE
def change_panel_qrcode(panel_id , BOT , call ):
    if call.data=='qrcode_sending':
        panel_=v2panel.objects.get(id=panel_id)
        if panel_.send_qrcode_mode==0:
            try:
                new_send_qrcode_moode=1
                panel_.send_qrcode_mode=new_send_qrcode_moode 
                panel_.save()   
            except Exception as change_qrcode_1 :
                print(f'Error during changing panel Qrcode changing \n\t  Error-msg : {change_qrcode_1}')

        elif panel_.send_qrcode_mode==1:
            try:
                new_send_qrcode_moode=2
                panel_.send_qrcode_mode=new_send_qrcode_moode 
                panel_.save()    
            except Exception as change_qrcode_2:
                print(f'Error during changing panel Qrcode changing \n\t  Error-msg : {change_qrcode_2}')

        else:
            try:
                new_send_qrcode_moode=0
                panel_.send_qrcode_mode=new_send_qrcode_moode 
                panel_.save()  
            except Exception as change_qrcode_3 :
                print(f'Error during changing panel Qrcode changing \n\t  Error-msg : {change_qrcode_3}')    
        Text_1='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n حالت ارسال کیوارکد پنل تغییر کرد '   
        BOT.edit_message_text(Text_1,call.message.chat.id , call.message.message_id , reply_markup= BotKb.how_to_send_links(panel_id))




#- panel_CONFIG
def change_panel_config(panel_id , BOT , call):
    if call.data=='link_sending':
        panel_=v2panel.objects.get(id=panel_id)

        if panel_.send_links_mode==0:
            try:
                new_send_links_mode=1
                panel_.send_links_mode=new_send_links_mode
                panel_.save()    
            except Exception as change_link_1 :
                print(f'Error during changing panel link changing \n\t  Error-msg : {change_link_1}')

        elif panel_.send_links_mode==1:
            try:
                new_send_links_mode=2
                panel_.send_links_mode=new_send_links_mode
                panel_.save()    
            except Exception as change_link_2 :
                print(f'Error during changing panel link changing \n\t  Error-msg : {change_link_2}') 

        else:
            try:
                new_send_links_mode=0
                panel_.send_links_mode=new_send_links_mode
                panel_.save()   
            except Exception as change_link_3:
                print(f'Error during changing panel link changing \n\t  Error-msg : {change_link_3}')          
        Text_1='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید\n\n حالت ارسال کانفیگ پنل تغییر کرد '
        BOT.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id ,reply_markup=BotKb.how_to_send_links(panel_id))
        









