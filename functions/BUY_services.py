from mainrobot.models import v2panel , products  , inovices
from telebot.types import InlineKeyboardButton , InlineKeyboardMarkup
from tools import QRcode_maker




def plans_loading_for_one_panel() :
    
    count_panels = []


    keyboard = InlineKeyboardMarkup()
    panels_ = v2panel.objects.all()
    products_ = products.objects.all()

    for i in panels_ :
        count_panels.append(i.id)

    if not panels_.exists() or not products_.exists():
        return 'no_panel_product'
    
    products_2 = products.objects.filter(panel_id = max(count_panels)).order_by('sort_id')

    for i in panels_ :
        
        if i.panel_status == 1:
            
            if i.panel_sale_mode == 0 : # نوع فروش :‌ بسته                
                return 'sale_closed'


            elif i.panel_sale_mode == 1 : # نوع فروش  :‌ باز 

                if i.capcity_mode == 0:  # نوع ظرفیت :‌ بدون ظرفیت 
                    return 'sale_open_no_zarfit'
                                            

                elif i.capcity_mode == 1:  # نوع ظرفیت : دارای ظرفیت
                    if i.all_capcity > 0 :
                        for i in products_2 : 
                                buttons = InlineKeyboardButton(text = i.product_name , callback_data =  f"buyservice_{i.id}_salemode_open_withcapcity")
                                keyboard.add(buttons) 
                        button_back_1more = InlineKeyboardButton(text = 'back🔙' , callback_data = 'back_to_main_menu_for_one_panels')
                        keyboard.add(button_back_1more) 
                        return keyboard
                    else :
                        return 'sale_open_no_zarfit'



                elif i.capcity_mode == 2 : # نوع ظرفیت :‌ نامحدود                 
                    for i in products_2 : 
                            buttons = InlineKeyboardButton(text = i.product_name , callback_data = f"buyservice_{i.id}_salemode_open_freecapcity")
                            keyboard.add(buttons ) 
                    button_back_1more = InlineKeyboardButton(text = 'back🔙' , callback_data = 'back_to_main_menu_for_one_panels')
                    keyboard.add(button_back_1more) 
                    return keyboard



            elif i.panel_sale_mode == 2 : #  نوع فروش : براساس ظرفیت 

                    if i.capcity_mode == 0 :  # نوع ظرفیت :‌ بدون ظرفیت 
                        return 'sale_zarfit_no_zarfit'
                                        
                                        
                    elif i.capcity_mode == 1 :
                        if i.all_capcity > 0 : # نوع ظرفیت : دارای ظرفیت
                            for i in products_2 :
                                    buttons = InlineKeyboardButton(text = i.product_name , callback_data = f"buyservice_{i.id}_salemode_zarfit_withcapcity")
                                    keyboard.add(buttons ) 
                            button_back_1more = InlineKeyboardButton(text = 'back🔙' , callback_data = 'back_to_main_menu_for_one_panels')
                            keyboard.add(button_back_1more) 
                            return keyboard
                        return 'sale_open_no_zarfit'



                    elif i.capcity_mode == 2 : # نوع ظرفیت :‌ نامحدود 

                        for i in products_2: 
                                buttons = InlineKeyboardButton(text = i.product_name , callback_data =  f"buyservice_{i.id}_salemode_zarfit_freecapcity")
                                keyboard.add(buttons ) 
                        button_back_1more = InlineKeyboardButton(text = 'back🔙' , callback_data = 'back_to_main_menu_for_one_panels')
                        keyboard.add(button_back_1more) 
                        return keyboard


        else :
            return 'panel_disable' 












def plans_loading_for_two_more_panel(panel_pk : int ) :

    keyboard = InlineKeyboardMarkup()
    panels_ = v2panel.objects.filter(id = panel_pk)



    
    for i in panels_ :

        if i.panel_status == 1:
            if not products.objects.filter(panel_id = panel_pk ).exists():
                return 'no_products'
            
            if i.panel_sale_mode == 0: # فروش : بسته
                return 'sale_closed'


            elif i.panel_sale_mode == 1: #فروش : باز 
                if i.capcity_mode == 0 : # ظرفیت : بدون ظرفیت
                    return 'sale_open_no_capcity'
                

                elif i.capcity_mode == 1 :
                        if i.all_capcity > 0: # ظرفیت : دارای ظرفیت
                            for i in products.objects.filter(panel_id = panel_pk).order_by('sort_id'):
                                buttons = InlineKeyboardButton(text= i.product_name , callback_data= f"buyservice_{i.id}_salemode_open_withcapcity")
                                keyboard.add(buttons)
                            button_back_2more = InlineKeyboardButton(text = 'بازگشت🔙' , callback_data = 'back_to_main_menu_for_two_panels')
                            keyboard.add(button_back_2more)  
                            return keyboard
                        else :
                            return 'sale_open_no_capcity'



                elif i.capcity_mode == 2 : # ظرفیت :نامحدود
                        for i in products.objects.filter(panel_id = panel_pk).order_by('sort_id'):
                            buttons = InlineKeyboardButton(text= i.product_name , callback_data= f"buyservice_{i.id}_salemode_open_freecapcity")
                            keyboard.add(buttons)
                        button_back_2more = InlineKeyboardButton(text = 'بازگشت🔙' , callback_data = 'back_to_main_menu_for_two_panels')
                        keyboard.add(button_back_2more)  
                        return keyboard
                         

            

            elif i.panel_sale_mode == 2 : # فروش : براساس ظرفیت

                
                if i.capcity_mode == 0 : # ظرفیت : بدون ظرفیت
                    return 'sale_zarfit_no_capcity'
                


                elif i.capcity_mode == 1 :
                        if  i.all_capcity > 0 : # ظرفیت : دارای ظرفیت
                            for i in products.objects.filter(panel_id = panel_pk):
                                buttons = InlineKeyboardButton(text= i.product_name , callback_data= f"buyservice_{i.id}_salemode_zarfit_withcapcity")
                                keyboard.add(buttons)
                            button_back_2more = InlineKeyboardButton(text = 'بازگشت🔙' , callback_data = 'back_to_main_menu_for_two_panels')
                            keyboard.add(button_back_2more)  
                            return keyboard
                        else :
                            return 'sale_zarfit_no_capcity'   
                


                elif i.capcity_mode == 2 : # ظرفیت :نامحدود                    
                        for i in products.objects.filter(panel_id = panel_pk):
                            buttons = InlineKeyboardButton(text= i.product_name , callback_data= f"buyservice_{i.id}_salemode_zarfit_freecapcity")
                            keyboard.add(buttons)
                        button_back_2more = InlineKeyboardButton(text = 'بازگشت🔙' , callback_data = 'back_to_main_menu_for_two_panels')
                        keyboard.add(button_back_2more)  
                        return keyboard


        else : 
            return 'panel_disable'











def create_inovices(user_id  , panel_name , product_name , data_limit , expire_date , pro_cost ,  paid_status ,config_name : None , paid_mode : str , gift_code : int = None , discount : int = None , user_username : str = None):
     
     
    try :
        inovices_ = inovices.objects.create(user_id = user_id ,
                            user_username = user_username ,
                            panel_name = panel_name ,
                            product_name=product_name ,
                            data_limit=data_limit ,
                            expire_date = expire_date ,
                            pro_cost = pro_cost ,
                            gift_code = gift_code ,
                            discount = discount ,
                            config_name = config_name , 
                            paid_status = paid_status ,
                            paid_mode = paid_mode )   
        return 'done'   
    except Exception as error:
        print(f'an error eccoured when adding inovices : {error}')




def how_to_send(request_ , panel_id , BOT , call):
    panel_ = v2panel.objects.get(id= panel_id)
    if panel_.send_qrcode_mode == 1 : #sub QRcode
        if request_ is False:
                print('requset is failed')
        else:
            sub_link = request_['subscription_url']
            qr_code_sub = QRcode_maker.make_qrcode(sub_link)
            if panel_.send_links_mode == 1: #sub link 
                    BOT.send_photo(call.message.chat.id , caption=f'this is sub link : \n\n{sub_link} ' , photo=qr_code_sub)


            elif panel_.send_links_mode == 2: #config link  
                            links_str = '\n'.join(request_['links'])
                            BOT.send_photo(call.message.chat.id , caption= None , photo= qr_code_sub)
                            BOT.send_message(call.message.chat.id , links_str)



            elif panel_.send_links_mode == 0 : # dont using links in caption
                        BOT.send_photo(call.message.chat.id , qr_code_sub)



    elif panel_.send_qrcode_mode == 2 : #config link Qrcode
            if request_ is False:
                print('request is failed')
            else:
                    config_link = request_['links']
                    sub_link = request_['subscription_url'] 
                        

                    if panel_.send_links_mode == 2: # config link 
                        for config in config_link:
                            qr_code_config = QRcode_maker.make_qrcode(config) 
                            BOT.send_photo(call.message.chat.id , caption= f'link : \n\n {config}' , photo= qr_code_config)

                    if panel_.send_links_mode == 1: # sub link 
                        for config in config_link:
                            qr_code_config = QRcode_maker.make_qrcode(config) 
                            BOT.send_photo(call.message.chat.id , photo= qr_code_config)
                        BOT.send_message(call.message.chat.id , sub_link)


                    if panel_.send_links_mode == 0 :
                        for config in config_link:
                            qr_code_config = QRcode_maker.make_qrcode(config) 
                            BOT.send_photo( call.message.chat.id , qr_code_config)

    else:
        pass     