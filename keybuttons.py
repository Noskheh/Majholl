from telebot.types import InlineKeyboardMarkup , InlineKeyboardButton , WebAppInfo
from mainrobot.models import v2panel , products , admins , users , channels , subscriptions , botsettings , shomarekart
import re ,  datetime , jdatetime



class BotkeyBoard:
    
    @staticmethod
    def main_menu_in_user_side(userId : int) :

        keyboard = InlineKeyboardMarkup()
        #web_app_url = 'https://59c1-188-215-166-184.ngrok-free.app/products/'
        #webappinfo = WebAppInfo(url = web_app_url)
        user_side_ui_buttom = [[InlineKeyboardButton('🚀 خرید سرویس جدید' , callback_data ='buy_service')] ,
                               [InlineKeyboardButton('📡 وضعیت سرویس' , callback_data ='service_status') ,InlineKeyboardButton('🔄 تمدید سرویس ' , callback_data ='tamdid_service')] ,
                               [InlineKeyboardButton('📖 حساب کاربری',callback_data ='wallet_profile')]
                              ]
        
        for rows in user_side_ui_buttom:
            keyboard.add(*rows)

        #button_webapp = InlineKeyboardButton('خرید از وبسایت', web_app=webappinfo)
        #keyboard.add(button_webapp)

        for i in admins.objects.all() :
            if userId == i.user_id and (i.is_owner == 1 or i.is_admin == 1) :
                button_robot_management = InlineKeyboardButton(text = '⚙️ مدیریت ربات',callback_data = 'robot_management')
                keyboard.add(button_robot_management)

        
        

        return keyboard
    


    @staticmethod 
    def management_menu_in_admin_side(user_id = None) :
        keyboard = InlineKeyboardMarkup()
        admins_ = admins.objects.get(user_id = user_id)


        admin_side_ui_buttom = [
                                [('🖥 مدیریت پنل ها ' , 'panels_management') , ('🎛مدیریت فروشگاه' , 'products_management')] ,
                                [('📈آمار ربات' , 'bot_statics') ] , 
                                [('👤مدیریت کاربران', 'users_management'), ('🧑🏼‍💻مدیریت ادمین ها' , 'admins_management')] ,
                                [('🤖تنظیمات ربات ', 'bot_managment')]
                                ]
        
        if admins_.is_owner == 1 or (admins_.is_owner == 1 and admins_.is_admin ==1 ):
            admin_side_ui_buttom = admin_side_ui_buttom

        
        if admins_.is_admin == 1 and admins_.is_owner == 0:

            if admins_.acc_botmanagment == 0 :
                bot_setting = ('🤖تنظیمات ربات ', 'bot_managment')
                for inner in admin_side_ui_buttom:
                    if bot_setting in inner :
                        inner.remove(bot_setting)

            if admins_.acc_panels == 0 :
                panels_managements = ('🖥 مدیریت پنل ها ' , 'panels_management')
                for inner in admin_side_ui_buttom :
                    if panels_managements in inner:
                        inner.remove(panels_managements)

            if admins_.acc_products == 0 :
                product_managemets = ('🎛مدیریت فروشگاه' , 'products_management')
                for inner in admin_side_ui_buttom :
                    if product_managemets in inner:
                        inner.remove(product_managemets)


            if admins_.acc_admins == 0 :
                admins_managements = ('🧑🏼‍💻مدیریت ادمین ها' , 'admins_management')
                for inner in admin_side_ui_buttom :
                    if admins_managements in inner:
                        inner.remove(admins_managements)

            if admins_.acc_users == 0 :
                users_managemet = ('👤مدیریت کاربران', 'users_management')
                for inner in  admin_side_ui_buttom :
                    if users_managemet in inner:
                        inner.remove(users_managemet)

        for row in admin_side_ui_buttom :
            row_buttons = []
            for text , data in row :
                buttons = InlineKeyboardButton(text = text , callback_data = data)
                row_buttons.append(buttons)
            keyboard.add(*row_buttons)       



        back_button = InlineKeyboardButton(text='بازگشت به منوی اصلی 🏘' , callback_data='back_from_management')  
        keyboard.add(back_button) 
        return keyboard
    






    @staticmethod
    def bot_management():
        keyboard = InlineKeyboardMarkup()
        bot_management_buttons = [[('🔒مدیریت جوین اجباری ' , 'manage_force_channel_join') , ('💸 مدیریت نحوه پرداخت' , 'manage_bank_cards')]]

        row_buttons = []

        for row in bot_management_buttons:
            for text , data in row:
                buttons = InlineKeyboardButton(text=text , callback_data=data)
                row_buttons.append(buttons)
            keyboard.add(*row_buttons)
        back_button = InlineKeyboardButton('بازگشت ',callback_data='back_to_management_menu')
        keyboard.add(back_button)   
        return keyboard




    @staticmethod 
    def manage_users():
        keyboard = InlineKeyboardMarkup()
        
        botsettings_ = botsettings.objects.all()
        for i in botsettings_:
            irnumber = i.irnumber
        ir_number = lambda txt : '✅' if txt == 1 else '❌'

        buttons_raw = [ [(ir_number(irnumber) , 'ir_number'),('احراز هویت با شماره' , 'ir_number')],
                        [('⬇️⬆️ موجودی کاربر ' , 'increase_decrease_cash'), ('🔴🟢 انسداد کاربر ', 'block_unblock_user')],
                        ]


        for row in buttons_raw:
            buttons_list = []
            for text , data in row:
                buttons = InlineKeyboardButton(text=text , callback_data=data)
                buttons_list.append(buttons)
            keyboard.add(*buttons_list)
        back_buttons = InlineKeyboardButton('بازگشت ', callback_data='back_from_user_management')
        keyboard.add(back_buttons)

        return keyboard



            
# -------------------------Channels----------------------------------------------------------------------------------------
    @staticmethod
    def load_channels(bot , Userid):
        keyboard = InlineKeyboardMarkup()
        channels_ = channels.objects.all()
        channel_list = []
        for i in channels_:
            user_joined = bot.get_chat_member(i.channel_url or i.channel_id  , Userid).status
            if user_joined == 'left':
                if i.ch_status == 1 : 
                    channel_url = bot.get_chat(str(i.channel_id) or str(i.channel_url)).invite_link
                    button = InlineKeyboardButton(i.channel_name , callback_data=channel_url  , url=channel_url)
                    channel_list.append(button)

        button_start=InlineKeyboardButton('✅جوین شدم' , callback_data='channels_joined')
        keyboard.add(*channel_list , button_start ,  row_width=1)
        return keyboard





# -------------------------PANEL MANAGEMENT----------------------------------------------------------------------------------------
    
    @staticmethod
    def panel_management_menu_in_admin_side():
        keyboard = InlineKeyboardMarkup()
        panel_ui_buttom = [[('➖ حذف کردن پنل ' , 'remove_panel') , ('➕ اضافه کردن پنل' , 'add_panel')] ,
                           [('🔩 مدیریت پنل ','manageing_panels')] ,
                           [('بازگشت به منوی قبلی ↪️' , 'back_from_panel_manageing')]]
        for i in panel_ui_buttom:
            button_to_add = []
            for text , data in i:
                buttom = InlineKeyboardButton(text=text , callback_data=data)
                button_to_add.append(buttom)
            keyboard.add(*button_to_add)
        return keyboard
    




    @staticmethod 
    def panel_management_remove_panel(id_panel:int=None ,kind=False):
        keyboard = InlineKeyboardMarkup()
        keyboard_2 = InlineKeyboardMarkup()
        panel_ = v2panel.objects.all() 
        remove_button_top_row = [[('حذف ' , 'remove_actions') , ('ادرس پنل' , 'panel_removal_url') , ('نام پنل ' , 'panel_removal_name')]]

        for rows_top in remove_button_top_row:
                top_row_buttons_list = []
                for text , data in rows_top:
                    top_row_buttons = InlineKeyboardButton(text=text , callback_data=data )
                    top_row_buttons_list.append(top_row_buttons)
                keyboard.add(*top_row_buttons_list)

        panels_to_list = []
        if not panel_.exists():
            return 'no_panel_to_remove'
        else : 
            for i in panel_:
                call_back_data=f'panel_remove_{i.id}'
                panel_url_shows=re.sub(r'(http|https)://' , '' , i.panel_url)
                three_tuple_row_list=[('❌' , call_back_data ) , (panel_url_shows , call_back_data) , (i.panel_name , call_back_data)]
                panels_to_list.append(three_tuple_row_list)
            for rows_buttom in panels_to_list :
                bottom_row_buttons_list = []
                for text , data in rows_buttom :
                    buttom_row_button = InlineKeyboardButton(text=text , callback_data=data)
                    bottom_row_buttons_list.append(buttom_row_button)
                keyboard.add(*bottom_row_buttons_list)

            back_button_manage_panel = InlineKeyboardButton('بازگشت ↪️' , callback_data = 'back_to_manage_panel')
            keyboard.add(back_button_manage_panel)


            which_to_remove =[[('حذف پنل و تمامی محصولات مرتبط', f'remove_products_panel_{id_panel}') , ('فقط حذف پنل ' , f'remove_only_panel_{id_panel}')] , 
                              [('بازگشت ↪️' , 'back_to_remove_panel_section')]]
            for i in which_to_remove:
                which_to_remove_buttons=[]
                for text , data in i :
                    button=InlineKeyboardButton(text=text , callback_data=data)
                    which_to_remove_buttons.append(button)
                keyboard_2.add(*which_to_remove_buttons)

            if kind is False :
                return keyboard
            else :
                return keyboard_2
        




    @staticmethod 
    def panel_management_manageing_panels():
        keyboard = InlineKeyboardMarkup()
        panel_ = v2panel.objects.all()

        manage_button_top_row = [[('مدیریت پنل' , 'manage_panel_') , ('وضعیت پنل' , 'panel_status') , ('نام پنل', 'panel_name')]]
        
        for i in manage_button_top_row:
            top_row_button_list = []
            for text , data in i:
                top_row_button = InlineKeyboardButton(text=text , callback_data=data)
                top_row_button_list.append(top_row_button)
            keyboard.add(*top_row_button_list)
        
        panels_to_list=[]
        if not panel_.exists() : 
            return 'no_panel_to_manage'
        else :
            for i in panel_:
                panel_status_out='🟢'  if i.panel_status==1 else  '🔴'
                panel_id=f'manageing_panel_{i.id}'
                manage_button_bottom_list=[('⚙️' , panel_id) , (panel_status_out , panel_id ) , (i.panel_name , panel_id )]
                panels_to_list.append(manage_button_bottom_list)

            for i in panels_to_list:
                bottom_row=[]
                for text , data in i:
                    bottom_row_buttons=InlineKeyboardButton(text=text , callback_data=data )
                    bottom_row.append(bottom_row_buttons)
                keyboard.add(*bottom_row)

            back_button = InlineKeyboardButton('بازگشت ↪️' , callback_data = 'back_to_manage_panel')   
            keyboard.add(back_button) 

            return keyboard
        




    @staticmethod
    def manage_selected_panel(panel_pk:int , passwd:bool=False , username:bool=False):
        keyboard = InlineKeyboardMarkup()
        for i in v2panel.objects.filter(id = panel_pk) :
            panel_status_out= '🟢' if i.panel_status == 1 else  '🔴'
            panel_reality_flow_out='None' if i.reality_flow=='' else i.reality_flow  
            panel_url_shows=re.sub(r'(http|https)://' , '' , i.panel_url)
            panel_username ='👁‍🗨👉🏻' if username==False else str(i.panel_username)  
            panel_password='👁‍🗨👉🏻' if passwd==False else str(i.panel_password)   

            selected_panel_list=[
                                [(str(panel_status_out) , f'panel_status_{i.id}' ) , ('وضعیت پنل' , 'panel_status')] ,
                                [(str(i.panel_name) , f'panel_name_{i.id}_{i.panel_name}') , ('نام پنل ' , 'panel_name')] , 
                                [(str(panel_url_shows) , f'panel_url_{i.id}_{panel_url_shows}') , ('ادرس پنل' , 'panel_url')] ,
                                [(panel_username, f'panel_username_{i.id}_{username}') , ('┐ یورزنیم پنل ' , f'view_username_{i.id}')] ,
                                [(panel_password , f"panel_password_{i.id}_{passwd}") , ('┘ پسوورد پنل ' , f'view_password_{i.id}')] ,
                                [(str(panel_reality_flow_out) , f'reality_flow_{i.id}') , ('reality-flow💡' , 'reality_flow')] ,
                                [('⚙️' , f'panel_capacity_{i.id}') , ('🧮ظرفیت پنل ' , 'panel_capacity')]]
        
        buttons_management = []
        for row in selected_panel_list:
            for text , data in row :
                button = InlineKeyboardButton(text=text , callback_data=data)
                buttons_management.append(button)
        keyboard.add(*buttons_management , row_width=2)

        button1=InlineKeyboardButton(text='🔖نوع ارسال اشتراک ' , callback_data= f'send_config_{panel_pk}')
        button2=InlineKeyboardButton(text='📊آمار پنل ' , callback_data=f'panel_statics_{panel_pk}')
        back_button=InlineKeyboardButton('بازگشت ↪️' , callback_data='back_to_manageing_panels')   
        keyboard.add(button1  ,button2 , back_button , row_width=1) 

        return keyboard
    




    @staticmethod
    def changin_reality_flow():
        keyboard=InlineKeyboardMarkup()
        reality_flow_buttons=[[('xtls-rprx-vision' , 'xtls-rprx-vision') , ('None' , 'None_realityFlow')]]
        reality_flow_buttons_list=[]
        for i in reality_flow_buttons:
            for text,data in i:
                buttons=InlineKeyboardButton(text=text , callback_data=data)
                reality_flow_buttons_list.append(buttons)
        keyboard.add(*reality_flow_buttons_list , row_width=2)
        
        return keyboard





    @staticmethod 
    def changin_panel_capcity(panel_pk):
        keyboard=InlineKeyboardMarkup()
        #= capcity-mode 0 : باز \ capcity-mode 1 : بسته 
        #= sale-mode 0 : بدون ظرفیت \ sale-mode : 1 ظرفیت نامحدود \ sale-mode : 2 دارای ظرفیت

        for i in  v2panel.objects.filter(id=panel_pk): 
            if i.capcity_mode==0:
                capcity_mode='بدون ظرفیت'   
            elif i.capcity_mode==1:
                capcity_mode='دارای ظرفیت'
            else:
                capcity_mode='ظرفیت نامحدود'            

            if i.panel_sale_mode==0: 
                sale_mode='بسته'
            elif i.panel_sale_mode==1:
                sale_mode='باز'
            all_capcity =  int(i.all_capcity) if i.all_capcity > 0  else 0

            sold_capcity = i.sold_capcity if i.sold_capcity > 0 else 0

            remaing_capacity= (int(all_capcity) - int(i.sold_capcity)) if i.all_capcity > 0 else 0

            panel_capcity_buttons=[[(capcity_mode , 'capcity_mode') , ('🎚نوع ظرفیت ' , 'capcity_mode')] ,
                                    [(sale_mode , 'sale_mode') , ('💸حالت فروش' , 'sale_mode')] ,
                                    [(f"{abs(all_capcity)} عدد" , f'all_capcity_{i.all_capcity}') , ('🔋ظرفیت کلی' , f'all_capcity_{i.all_capcity}')] ,
                                    [(f"{abs(sold_capcity)} عدد" , 'sold_capcity') , ('💰ظرفیت فروش رفته' , 'sold_capcity')],
                                    [(f"{abs(remaing_capacity)} عدد" , 'remaining_capcity') , ('⏳ظرفیت باقی مانده ' , 'remaining_capcity')] ,
                                    [('بازگشت ↪️' , 'back_from_panel_capcity_list')]]
        
        for row in panel_capcity_buttons:
            buttons_to_list=[]
            for text, callback_data in row:
                button = InlineKeyboardButton(text=text , callback_data=callback_data)
                buttons_to_list.append(button)
            keyboard.add(*buttons_to_list)

        return keyboard





    @staticmethod
    def how_to_send_links(panel_pk):
        keyboard=InlineKeyboardMarkup()
        panel_=v2panel.objects.filter(id=panel_pk)
        for i in panel_:
            if i.send_links_mode==0:
                send_link = 'عدم ارسال'
            elif i.send_links_mode==1:
                send_link = 'لینک هوشمند'
            else:
                send_link='لینک کانفیگ'

            if i.send_qrcode_mode==0:
                send_qrcode='عدم ارسال'
            elif i.send_qrcode_mode==1:
                send_qrcode='لینک هوشمند'
            else:
                send_qrcode='لینک کانفیگ'

            buttons = [[('Qrcode نوع ارسال' , 'qrcode_sending_kind') , ('نوع لینک ارسالی' ,'link_sending_kind')] ,
                        [(send_qrcode , 'qrcode_sending') , (send_link , 'link_sending')]]
        for i in buttons:
            buttons_list=[]
            for text , data in i:
                button = InlineKeyboardButton(text=text , callback_data=data)
                buttons_list.append(button)
            keyboard.add(*buttons_list)

        back_button = InlineKeyboardButton(text ='بازگشت ↪️' ,  callback_data='back_from_panel_howtosend_list')    
        keyboard.add(back_button)
        
        return keyboard
    

    @staticmethod 
    def updating_panel (panel_id=int):
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton('بروزرسانی 🔄' , callback_data=f'updating_panel_{panel_id}')
        button_back = InlineKeyboardButton('بازگشت' , callback_data='back_from_panel_static')
        keyboard.add(button , button_back , row_width=1)
        return keyboard





# -------------------------PRODUCTS MANAGEMENT----------------------------------------------------------------------------------------


    @staticmethod
    def product_management_menu_in_admin_side():
        keyboard =InlineKeyboardMarkup()
        product_ui_buttom = [[('➖حذف کردن محصول ' , 'remove_product') , ('➕اضافه کردن محصول ' , 'add_product' )] ,
                            [('🔩مدیریت محصولات '  , 'manage_products')] ,
                            [('بازگشت به منوی قبلی ↪️' , 'back_from_products_manageing' )] ]
        for i in product_ui_buttom: 
            product_ui_buttom_list=[]
            for text , data in i:
                buttom = InlineKeyboardButton(text=text , callback_data=data)
                product_ui_buttom_list.append(buttom)
            keyboard.add(*product_ui_buttom_list)
        return keyboard
    

    @staticmethod
    def load_panel_add_product(add_product=False , remove_product=False , manage_product=False):
        panel_=v2panel.objects.all()
        keyboard=InlineKeyboardMarkup()
        if not panel_.exists():
            return "no_panel_to_load"
        else:
            call_data = ''
            if add_product is not False and remove_product is False and manage_product is False:
                call_data = "panel_product_"
            elif remove_product is not False and add_product is False and manage_product is False:
                call_data = "remove_panel_product_"
            elif manage_product is not False and add_product is False and remove_product is False:
                call_data = 'managing_panel_product_'

            for i in panel_:
                buttons=InlineKeyboardButton(text=i.panel_name , callback_data = f'{call_data}{i.id}')
                keyboard.add(buttons)
            back_button_add = InlineKeyboardButton(text = 'بازگشت ↪️'  , callback_data = f'back_{call_data}')
            keyboard.add(back_button_add)
            return keyboard
           
    

    @staticmethod 
    def select_inbounds(inbound_selected:any=None):
        keyboard=InlineKeyboardMarkup(row_width=1)
        buttons_list=[]
        if inbound_selected is not None:
            for i in inbound_selected:
                button = InlineKeyboardButton(text=i  , callback_data=i)
                buttons_list.append(button)
        keyboard.add(*buttons_list)
        done_buttons = InlineKeyboardButton('اتمام و ذخیره محصول 🧷' , callback_data='done_inbounds')
        back_buttons = InlineKeyboardButton(' بازگشت و لغو ثبت محصول ↪️ ' , callback_data='back_from_inbounds_selecting')
        keyboard.add(done_buttons , back_buttons)
        return keyboard 
        













    @staticmethod 
    def product_managemet_remove_products(panel_pk , page:int=1 , item_peer_page:int=8) :
        keyboard=InlineKeyboardMarkup()
        product_=products.objects.filter(panel_id=panel_pk)
        top_row=[[('حذف' , 'remove_actions') , ('آدرس پنل' , 'related_panel_url') , ('نام محصول' , 'product_removal_name')]]        
        for i in top_row:
            top_row_buttons_list=[]
            for text , data in i:
                top_row_button=InlineKeyboardButton(text=text , callback_data=data)
                top_row_buttons_list.append(top_row_button)
            keyboard.add(*top_row_buttons_list , row_width=4)
        products_list=[]
        start_index=(page-1) * item_peer_page
        end_index=(page-1) * item_peer_page + item_peer_page
        count_products=[]
        if not product_.exists():
            return 'no_products_to_remove'
        else:
            for i , product in enumerate(product_) : 
                count_products.append(i)
                if  start_index < i+1 <= end_index:
                    for x in v2panel.objects.filter(id=product.panel_id) :
                        panelurl=re.sub(r'(http|https)://' , '' ,  x.panel_url)
                    product_id=f'delete_prodcut_{product.id}'
                    products_list_bottom_tuple_list = [('❌' , product_id) , (panelurl , product_id) , (product.product_name , product_id)]
                    products_list.append(products_list_bottom_tuple_list)

        for i in products_list:
                bottom_row_buttons_list=[]
                for text , data in i:
                    bottom_row_button=InlineKeyboardButton(text =text , callback_data=data)
                    bottom_row_buttons_list.append(bottom_row_button)
                keyboard.add(*bottom_row_buttons_list , row_width=3)
        next_prev_buttons = [InlineKeyboardButton(text='صفحه بعدی ⏪' , callback_data = f'remove_next_page_products_{page +1}') , 
                             InlineKeyboardButton(text='صفحه قبل ⏩' , callback_data = f'remove_prev_page_products_{page - 1}')]
        if page <= 1:
            if len(count_products) > item_peer_page:
                keyboard.add(next_prev_buttons[0])
        if page > 1 and len(products_list)==item_peer_page: 
                keyboard.add(next_prev_buttons[0] , next_prev_buttons[1])
        elif page > 1 and len(products_list) < item_peer_page :    
                keyboard.add(next_prev_buttons[1])

        back_button=InlineKeyboardButton(text ='بازگشت ↪️' , callback_data='back_from_remove_products')  
        keyboard.add( back_button , row_width = 1)
        return keyboard














    @staticmethod
    def products_list(panel_pk , up:int=None , down:int=None , page:int=1 , item_peer_page:int=10):
        keyboard=InlineKeyboardMarkup()
        top_row = [[('🔻پایین' , 'down') , ('🔺بالا' , 'up') , ('محصول' , 'product')]]
        for i in top_row:
            top_buttons_list=[]
            for text , data in i:
                button = InlineKeyboardButton(text=text , callback_data=data)
                top_buttons_list.append(button)
            keyboard.add(*top_buttons_list ,row_width=3)


        bottom_row_list=[]
        filtered_products=products.objects.filter(panel_id=panel_pk).order_by('sort_id')
        sorted_filtered_list=[(prod.sort_id, prod.id) for prod in filtered_products]
        if up is not None:
            for pro_sortId , pro_id in sorted_filtered_list:
                if pro_id==sorted_filtered_list[up - 1][1]:
                    before_sort_id=sorted_filtered_list[up - 2][0]
                    after_sort_id=sorted_filtered_list[up - 1][0]
                    try:
                        product=products.objects.get(id=sorted_filtered_list[up - 1][1])
                        new_sort_id = before_sort_id 
                        product.sort_id = new_sort_id
                        product.save()
                        product2 = products.objects.get(id=sorted_filtered_list[up - 2][1])
                        new_sort_id_2=after_sort_id
                        product2.sort_id=new_sort_id_2
                        product2.save()
                    except Exception as up_error:
                        print(f'something wentwrong \\\ up section-1 \\\:{up_error}')
        if down is not None:
            for pro_sortId , pro_id in sorted_filtered_list:
                if pro_id==sorted_filtered_list[down - 1][1]:      
                    if down<=len(sorted_filtered_list) - 1: 
                        before_sort_id=sorted_filtered_list[down - 1][0]
                        after_sort_id=sorted_filtered_list[down][0]
                        try:
                            productـmain=products.objects.get(id=sorted_filtered_list[down - 1][1])
                            new_sort_id=after_sort_id 
                            productـmain.sort_id=new_sort_id
                            productـmain.save()
                            product2 = products.objects.get(id=sorted_filtered_list[down][1])
                            new_sort_id_2=before_sort_id
                            product2.sort_id=new_sort_id_2
                            product2.save() 
                        except Exception as down_error_1:
                            print(f'something wentwrong \\\ down seciotn-1 \\\ :{down_error_1}')     
                    elif down>=len(sorted_filtered_list)-1:
                        before_sort_id = sorted_filtered_list[down - 1][0]
                        after_sort_id = sorted_filtered_list[down - down][0]
                        try :
                            productـmain=products.objects.get(id=sorted_filtered_list[down - 1][1])
                            new_sort_id=after_sort_id 
                            productـmain.sort_id=new_sort_id
                            productـmain.save()

                            product2=products.objects.get(id=sorted_filtered_list[down - down][1])
                            new_sort_id_2=before_sort_id
                            product2.sort_id=new_sort_id_2
                            product2.save()   
                        except Exception as down_error_2:
                            print(f'something wentwrong \\\ down section-2 \\\ :{down_error_2}')

        start_index = (page - 1) * item_peer_page
        end_index = (page - 1 ) * item_peer_page + item_peer_page
        all_products_num = []
        
        if not filtered_products.exists():
            return 'no_product_to_manage'
        else:
            for num , (sort_id, produ_id) in enumerate(sorted_filtered_list):
                all_products_num.append(num)
                if start_index < num+1 <=end_index : 
                    product=products.objects.get(id=produ_id)
                    num=num+1 
                    bottom_row = [('👇🏻' , f'down_{num}') ,
                                ('👆🏻' , f'up_{num}') ,
                                (product.product_name , f'detaling_product_{product.id}')]
                    bottom_row_list.append(bottom_row)

        for row in bottom_row_list:
            bottoms_list_unpack=[]
            for text , data in row:
                button = InlineKeyboardButton(text=text , callback_data=data)
                bottoms_list_unpack.append(button)

            keyboard.add(*bottoms_list_unpack , row_width =3)

        next_prev_buttons =[InlineKeyboardButton(text='صفحه بعدی ⏪' , callback_data =f'product_next_page_products_{page +1}') , 
                             InlineKeyboardButton(text='صفحه قبل ⏩' , callback_data =f'product_prev_page_products_{page - 1}')]
        if page <=1:
            if len(all_products_num)<=item_peer_page:
                pass 
            if len(all_products_num) > item_peer_page :
                keyboard.add(next_prev_buttons[0])

        if page > 1 and len(bottom_row_list)==item_peer_page: 
                keyboard.add(next_prev_buttons[0] , next_prev_buttons[1])  

        elif page > 1 and len(bottom_row_list) < item_peer_page :    
                keyboard.add(next_prev_buttons[1])
        back_button = InlineKeyboardButton(text = 'بازگشت ↪️' ,  callback_data = 'back_from_manage_products_list_updown')  
        keyboard.add( back_button , row_width = 1)

        return keyboard









    @staticmethod
    def product_changing_details(product_id : int ) :

        keyboard = InlineKeyboardMarkup()
        for i in products.objects.filter(id = int(product_id)):
            data_limit_str = str(i.data_limit) if i.data_limit else 'N/A'
            pro_cost = format(i.pro_cost , ',')
            product_status='🟢' if i.product_status else '🔴'
            buttons = [[(product_status , f'_pr_status_{i.id}') , ('وضعیت محصول ' , f'_pr_status_{i.id}') ] ,
                       [(i.product_name  , f"_product_name_{i.id}" ) , ('📝نام محصول' , f"_product_name_{i.id}")], 
                       [(data_limit_str + ' گیگ ', f'_data_limit_{i.id}') , ('🔋حجم محصول' , f'_data_limit_{i.id}')] ,
                       [(str(i.expire_date) + ' روز ', f'ـexpire_date_{i.id}') , ('⏳مدت زمان ' , f'ـexpire_date_{i.id}')] ,
                       [(pro_cost + ' تومان ' , f'_pro_cost_{i.id}') , ('💸قیمت محمصول' , f'_pro_cost_{i.id}')],
                       [('📡اینباند های محصول' , f'_inbounds_product_{i.id}')]]
            
        for  i , rows in enumerate(buttons) :
            buttons_list = []
            for text , data in rows :
                button = InlineKeyboardButton(text = text , callback_data= data)
                buttons_list.append(button)
            keyboard.add(*buttons_list , row_width=2)


        back_button = InlineKeyboardButton(text = 'بازگشت ↪️' ,  callback_data = 'back_from_manage_products_changing_limit')  
        keyboard.add( back_button , row_width = 1)



        return keyboard

    @staticmethod 
    def change_inbounds(inbound_selected:any=None):
        keyboard=InlineKeyboardMarkup(row_width=1)
        buttons_list=[]
        if inbound_selected is not None:
            for i in inbound_selected:
                button = InlineKeyboardButton(text=i  , callback_data=i)
                buttons_list.append(button)
        keyboard.add(*buttons_list)
        done_buttons = InlineKeyboardButton('اتمام و ذخیره 🧷' , callback_data='change_inbound_done')
        back_buttons = InlineKeyboardButton('بازگشت و لغو ↪️' , callback_data='back_from_inbounds_chaging')
        keyboard.add(done_buttons , back_buttons)
        return keyboard 








# -------------------------BUY SECTION----------------------------------------------------------------------------------------



    @staticmethod 
    def chosing_panels_in_buying_section():
        panels_ = v2panel.objects.all()
        keyboard = InlineKeyboardMarkup()

        buttons_panel_list = []
        if panels_.count() >= 2:
            for i in panels_:
                button = InlineKeyboardButton(text= str(i.panel_name), callback_data=f'TBSpanel_pk_{str(i.id)}')
                buttons_panel_list.append(button)
            button_back = InlineKeyboardButton(text='✤ - بازگشت به منوی قبلی - ✤' , callback_data='back_from_chosing_panels_buying')
        keyboard.add(*buttons_panel_list , button_back , row_width=1)

        return keyboard



    @staticmethod
    def confirmation():
        keyboard = InlineKeyboardMarkup()

        button_1 = InlineKeyboardButton('✅ تایید محصول ' , callback_data= 'verify_product')
        button_2 = InlineKeyboardButton('✤ - بازگشت به منوی قبلی - ✤' , callback_data = 'back_from_verfying')
        
        keyboard.add(button_1 , button_2 , row_width = 1)
        
        return keyboard





    @staticmethod 
    def payby_in_user_side(tamdid:bool= False ):
        keyboard = InlineKeyboardMarkup()
        
        data_wallet = 'pay_with_wallet' if tamdid is False else 'tamdid_pay_with_wallet'
        data_card = 'pay_with_card' if tamdid is False else 'tamdid_pay_with_card'
        back_data = 'back_from_payment' if tamdid is False else 'back_from_payment_tamdid'

        pay_options = []

        for i in botsettings.objects.all():

            if i.wallet_pay ==1 and i.kartbkart_pay ==1 :
                pay_options.append(('👝 پرداخت با کیف پول' , data_wallet))
                pay_options.append(('💳پرداخت کارت به کارت' , data_card))

            elif i.wallet_pay ==1 :
                pay_options.append(('👝 پرداخت با کیف پول' , data_wallet))    

            elif i.kartbkart_pay ==1 :
                pay_options.append(('💳پرداخت کارت به کارت' , data_card))
            


        for text , data in pay_options :
            buttons = InlineKeyboardButton(text = text , callback_data = data)
            keyboard.add(buttons , row_width = 1)
        
        back_button = InlineKeyboardButton('✤ - بازگشت به منوی قبلی - ✤', callback_data=back_data)
        keyboard.add(back_button)

        return keyboard
    





    @staticmethod 
    def agree_or_disagree(user_id , tamdid:bool=None):
        keyboard = InlineKeyboardMarkup()
        data_agree =  f'agree_{user_id}' if tamdid is None else   f'tamdid_agree_{user_id}'
        data_disagree = f'disagree_{user_id}' if tamdid is None else  f'tamdid_disagree_{user_id}'

        rows = [InlineKeyboardButton(text ='✅ تایید پرداخت ', callback_data = data_agree),
                InlineKeyboardButton(text ='❌ رد پرداخت ', callback_data = data_disagree)]
        
        keyboard.add(*rows)
        
        return keyboard    
    






# ------------------------- tamdidi_service ----------------------------------------------------------------------------------------
    
    @staticmethod
    def show_user_subsctription(user_id):
        keyboard = InlineKeyboardMarkup()
        user_ = users.objects.get(user_id = user_id)
        subscriptions_ = subscriptions.objects.filter(user_id = user_)
        if subscriptions_.count() >= 1:
            for i in subscriptions_:
                buttons = InlineKeyboardButton(text= i.user_subscription , callback_data= f'Tamidi:{i.user_subscription}:{i.user_id.user_id}')
                keyboard.add(buttons)
        else :
            return 'no_sub_user_have'
        back_button = InlineKeyboardButton('✤ - بازگشت به منوی قبلی - ✤' , callback_data='back_from_user_tamdid_service')
        keyboard.add(back_button)
        return keyboard
    






# ------------------------- User_service status ----------------------------------------------------------------------------------------
    @staticmethod
    def show_service_status(user_id):
        keyboard = InlineKeyboardMarkup()
        users_ = users.objects.get(user_id = user_id)
        subscriptions_ = subscriptions.objects.filter(user_id = users_).order_by('date_created').reverse()

        buttons_list = []
        for i in subscriptions_:
            buttons = InlineKeyboardButton(text= i.user_subscription , callback_data=f'serviceshow.{users_.user_id}.({i.user_subscription})')
            buttons_list.append(buttons)
        button_back = InlineKeyboardButton(text='✤ - بازگشت به منوی قبلی - ✤'  , callback_data='back_from_service_status')
        button_notinlist = InlineKeyboardButton(text='🚦 سرویس من در لیست نیست 🚦'  , callback_data='service_not_inlist')

        keyboard.add(*buttons_list , button_notinlist , button_back , row_width=1)

        return keyboard
    



    @staticmethod 
    def user_service_status(user_id , request):
        keyboard = InlineKeyboardMarkup( )
        users_ = users.objects.get(user_id = user_id)
        
        service_status = '✅ فعال' if request['status'] == 'active' else '❌ غیر فعال'
        used_traffic = request['used_traffic'] / ( 1024 * 1024 * 1024)


        online_at = request['online_at'] if request['online_at'] is not None else 'empty'
        if online_at != 'empty':
            dt = datetime.datetime.strptime(online_at.split('.')[0], '%Y-%m-%dT%H:%M:%S')
            last_online = jdatetime.datetime.fromgregorian(datetime=dt)
        else:
            last_online = 'بدون اتصال'

        buttons_list = [
                    [(f'{service_status} ' , f'{service_status}') , ('وضعیت سرویس ' , 'en_di_service')] , 
                    [(f'{round(used_traffic , 2)} گیگ ' , f'{round(used_traffic , 2)}') , ('🔋حجم مصرفی', 'config_usage')],
                    [(f'{str(last_online)}' ,f'{str(last_online)}') , ('👁‍🗨زمان آخرین اتصال' , 'last_connection')] ,
                    [('📥 دریافت لینک اشتراک' , 'get_config_link') , ('🖼 دریافت QRcode اشتراک' , 'get_qrcode_link')]]
        
        button_list = []
        for row in buttons_list:
            for text , data in row:
                buttons = InlineKeyboardButton(text= text , callback_data=data)
                button_list.append(buttons)
        back_button = InlineKeyboardButton('✤ - بازگشت به منوی قبلی - ✤' , callback_data='back_from_user_service_status')
        get_new_link = InlineKeyboardButton('❌ حذف لینک فعلی و دریافت لینک جدید ❌',  callback_data='get_new_link')
        get_removing_account = InlineKeyboardButton('❌ حذف کامل اشتراک ❌' , callback_data='get_removing_account')
        keyboard.add(*button_list , row_width=2)
        keyboard.add(get_new_link, get_removing_account, back_button ,row_width=1)

        return keyboard
    






# ------------------------- Wallet Profile ----------------------------------------------------------------------------------------
    @staticmethod 
    def wallet_profile(user_id , info  = False):
        keyboard = InlineKeyboardMarkup()
        
        users_ = users.objects.all().filter(user_id = user_id)
        botsettings_ = [i for i in botsettings.objects.all()]
        info_box = []     

        for i in users_  :
            wallet_num = int(i.user_wallet)
            fname = i.first_name if i.first_name  else  ''
            lname = i.last_name if i.last_name else ''
            buttons = [ 
                        [(fname + lname, f'{fname + lname}') , ('👤- نام ' , 'fist_last_name')] ,
                        [(i.user_id , 'user_id') , ('ایدی عددی -🆔', 'user_id')] , 
                        [(i.username , 'username') , ('🌀- یوزرنیم' , 'username')] , 
                        [(format(wallet_num , ',')+ ' تومان ', 'wallet') , ('👝- کیف پول' , 'wallet')] , 
                        # place for moneyusrtousr
                        [('شارژ کیف پول 💰' , 'charge_wallet')],
                        [('✤ - بازگشت به منوی قبلی - ✤' , 'back_from_wallet_profile' )]]
            
            info_box.append(i.user_id )
            info_box.append(i.username)
        


        if botsettings_[0].moneyusrtousr == 1 :
                buttons.insert(4 , [('انتقال وجه به کاربر 💸 ' , 'tranfert_money_from_wallet')])


        for i in buttons :
            buttons_list = []
            for text , data in i:
                button = InlineKeyboardButton(text= text , callback_data=  data)
                buttons_list.append(button)
            keyboard.add(*buttons_list)



        if info == False :
            return keyboard
        else :
            return info_box 
        




    @staticmethod 
    def wallet_accepts_or_decline(user_id ):
        keyboard = InlineKeyboardMarkup()

        rows = [InlineKeyboardButton(text ='✅ تایید پرداخت ', callback_data= f'wallet_accepts_{user_id}'),
                InlineKeyboardButton(text ='❌ رد پرداخت ', callback_data =f'wallet_decline_{user_id}')]
        keyboard.add(*rows)
        
        return keyboard  
    




# ------------------------- admin-section ----------------------------------------------------------------------------------------



#//TODO improve this section
    @staticmethod 
    def show_admins(who = None , num_toshow_items:int=2 , page_items:int=1):

        keyboard = InlineKeyboardMarkup()
        admins_ = admins.objects.filter(is_admin=1).all()
        admin_name_id = f'{admins_.first().admin_name}-{admins_.first().user_id}'
        admin_id = f'{str(admins_.first().user_id)}'

        if who is not None: 
            try :
                admins_who = admins.objects.get(user_id = int(who))
                admin_name_id = f'{admins_who.admin_name}-{admins_who.user_id}'
                admin_id = f'{str(admins_who.user_id)}'
            except Exception as notfounding :
                print(f'user not found in admin db // error msg : {notfounding}')
  
             

        
        buttons_row_list = [[(f'🟢انتخاب شده : {admin_name_id}', f'loads_{admin_id}')],
                            [('❌حذف کردن ادمین ' ,f'adminremove_{admin_id}') , ('🕹مدیریت دسترسی ها' , f'adminaccess_{admin_id}')],
                            [('🔻انتخاب ادمین های دیگر🔻' ,'Choose_other_admins')]]


        buttons_add_list = []
        for row in buttons_row_list:
            for text , data in row:
                button = InlineKeyboardButton(text , callback_data=data)
                buttons_add_list.append(button)
        keyboard.add(buttons_add_list[0])
        keyboard.add(buttons_add_list[1] , buttons_add_list[2] , row_width=2)
        keyboard.add(buttons_add_list[3])


        start = (page_items - 1) * num_toshow_items
        end = start + num_toshow_items

        admin_list = [i for i in admins_]

        if  who is not None  and admins_.first() not in admin_list:
            admin_list.append(admins_.first())
        

        items_button = []

            
        for ind , items in enumerate(admin_list , 0):
            if start < ind <= end :
                items_button.append(items)
                
        
              
        if who is not None :
            user_admin = admins.objects.get(user_id = who)
            if user_admin in items_button:
               indx =  items_button.index(user_admin)
               items_button.pop(indx)
               items_button.insert(indx , admins_.first())
        
        buttons_bottom_list = []
        
        if len(items_button) ==1:
            if page_items == 1 :
                buttons_bottom_list = [[(f'{items_button[0].admin_name}-{items_button[0].user_id}' , f'load_{items_button[0].user_id}')],]
            elif page_items > 1:
                    buttons_bottom_list = [[(f'{items_button[0].admin_name}-{items_button[0].user_id}' , f'load_{items_button[0].user_id}')],
                                        [('◀️ قبلی ' , f'Abefore_{page_items - 1}')]]

        elif len(items_button) ==2:
            if page_items == 1 and len(admin_list) >= 4:
                buttons_bottom_list = [[(f'{items_button[0].admin_name}-{items_button[0].user_id}' , f'load_{items_button[0].user_id}') , (f'{items_button[1].admin_name}_{items_button[1].user_id}' , f'load_{items_button[1].user_id}')],
                                      [('▶️ بعدی ' , f'Anext_{page_items + 1}')]]
                
            elif page_items == 1 and len(admin_list)-1 == len(items_button):
                    buttons_bottom_list = [[(f'{items_button[0].admin_name}-{items_button[0].user_id}' , f'load_{items_button[0].user_id}') , (f'{items_button[1].admin_name}_{items_button[1].user_id}' , f'load_{items_button[1].user_id}')],]
                    

            else:
                if len(admin_list)-1 == (page_items*2):
                    buttons_bottom_list = [[(f'{items_button[0].admin_name}-{items_button[0].user_id}' , f'load_{items_button[0].user_id}') , (f'{items_button[1].admin_name}_{items_button[1].user_id}' , f'load_{items_button[1].user_id}')],
                                        [('◀️ قبلی ' , f'Abefore_{page_items - 1}')]]
                
                else:
                    buttons_bottom_list = [[(f'{items_button[0].admin_name}-{items_button[0].user_id}' , f'load_{items_button[0].user_id}') , (f'{items_button[1].admin_name}_{items_button[1].user_id}' , f'load_{items_button[1].user_id}')],
                                        [('◀️ قبلی ' , f'Abefore_{page_items - 1}'), ('▶️ بعدی ' , f'Anext_{page_items + 1}')]]



        bottom_list = []
        
        for bottom in buttons_bottom_list:
            for text , data in bottom:
                button = InlineKeyboardButton(text= text , callback_data=data)
                bottom_list.append(button)

        back_admin_buttons = InlineKeyboardButton('بازگشت به منوی قبلی↪️' , callback_data='back_from_admin_menu')
        admin_add = InlineKeyboardButton('➕اضافه کردن ادمین ' , callback_data='add_new_admin')
        
        keyboard.add(*bottom_list, row_width=2)

        keyboard.add(admin_add , back_admin_buttons ,  row_width=1)

        return keyboard 







    @staticmethod
    def manage_admin_acc(user_id = None):
        keyboard = InlineKeyboardMarkup()
        admins_ = admins.objects.get(user_id = user_id)
        status_txt = lambda txt : "❌" if txt == 0 else '✅'
        #status_txt = lambda botstatus : '❌غیر فعال' if botstatus == 0 else  '✅فعال'
        

        buttons_raw  = [[(status_txt(admins_.acc_panels) , f'accpanels_{str(admins_.user_id)}') , ('دسترسی به تنظیمات پنل ها' , f'accpanel_{str(admins_.user_id)}')],
                       [(status_txt(admins_.acc_products) , f'accproducts_{str(admins_.user_id)}') , ('دسترسی به تنظیمات محصولات ها' , f'accprodu_{str(admins_.user_id)}')],
                       [(status_txt(admins_.acc_botmanagment) , f'accpbotseeting_{str(admins_.user_id)}') , ('دسترسی به تنظیمات مدیریت بات' , f'accpbotseeting_{str(admins_.user_id)}')],
                       [(status_txt(admins_.acc_admins) , f'accadmins_{str(admins_.user_id)}') , ('دسترسی به تنظیمات ادمین ها ', f'accadmins_{str(admins_.user_id)}')],
                        [(status_txt(admins_.acc_users) , f'accusermanagment_{str(admins_.user_id)}') , ('دسترسی به مدیریت یوزر ها', f'accusermanagment_{str(admins_.user_id)}')]]

        for row in buttons_raw:
            buttons_list = []
            for text , data in row:
                button = InlineKeyboardButton(text=text , callback_data=data)
                buttons_list.append(button)
            keyboard.add(*buttons_list)
        back_button= InlineKeyboardButton('بازگشت به منوی قبلی↪️' , callback_data='back_from_admin_access')
        keyboard.add(back_button)
        return keyboard







# ------------------------- karts-section ----------------------------------------------------------------------------------------


    @staticmethod 
    def manage_howtopay():
        status_txt = lambda botstatus : '❌غیر فعال' if botstatus == 0 else  '✅فعال'
        keyboard = InlineKeyboardMarkup()

        botsettings_ = botsettings.objects.all()
        for i in botsettings_:
            raw_buttons = [
                        [(status_txt(i.wallet_pay), 'walletpay_status') , ('پرداخت با کیف پول ','walletpay_status')],
                        [(status_txt(i.kartbkart_pay) , 'kartbkart_status'), ('پرداخت با کارت به کارت' , 'kartbkart_status')],
                        [(status_txt(i.moneyusrtousr) , 'moneyusrtousr_status'), ('انتقال وجه یوزر به یوزر' , 'moneyusrtousr_status')],
                        ]

        buttons = []
        for i in raw_buttons:
            for text , data in i:
                button = InlineKeyboardButton(text=text , callback_data=data)
                buttons.append(button)
        keyboard.add(*buttons , row_width=2)

        button_manage_shomare_kart = InlineKeyboardButton('مدیریت شماره کارت ها ' , callback_data='manage_shomare_kart')
        back_button = InlineKeyboardButton('✤ - بازگشت به منوی قبلی - ✤' , callback_data='back_from_mange_howtopay')
        keyboard.add(button_manage_shomare_kart , back_button , row_width=1)


        return keyboard    
    

    
    @staticmethod
    def manage_shomarekart():
        keyboard = InlineKeyboardMarkup()
        shomarekart_ = shomarekart.objects.all()
        
        raw_top_buttons = [[('مدیریت کارت' ,'mangene') , ('شماره کارت','kart_number') , ('نام بانک' , 'bank_name')]]

        top_buttons =[]
        for i in raw_top_buttons:
            for text , data in i:
                button = InlineKeyboardButton(text=text , callback_data=data )
                top_buttons.append(button)
        keyboard.add(*top_buttons , row_width=3)


        raw_bottom_buttons = []
        for i in shomarekart_:
            button = [('⚙️' , f'mkart_{str(i.bank_card)}') , (f'{str(i.bank_card)}' , f'mkart_{str(i.bank_card)}') , (f'{str(i.bank_name)}' , f'mkart_{str(i.bank_card)}')]
            raw_bottom_buttons.append(button)
        

        
        for i in raw_bottom_buttons:
            bottom_buttons = []
            for text , data in i:
                button = InlineKeyboardButton(text=text , callback_data=data)
                bottom_buttons.append(button)

            keyboard.add(*bottom_buttons, row_width=3)
        

        add_shomare_kart = InlineKeyboardButton('اضافه کردن شماره کارت جدید' , callback_data='add_new_kart_number')
        back_button = InlineKeyboardButton('✤ - بازگشت به منوی قبلی - ✤' , callback_data='back_from_manage_shomare_karts')
        keyboard.add(add_shomare_kart, back_button , row_width=1)

        return keyboard




    @staticmethod 
    def manage_kart(kart_number):
        shomarekart_ = shomarekart.objects.get(bank_card= int(kart_number))
        status = 'فعال کردن' if shomarekart_.bank_status == 0 else 'غیر فعال کردن'
        use_status = 'استفاده در پرداخت ها' if shomarekart_.bank_inmsg == 0 else 'عدم استفاده در پرداخت ها'

        keyboard = InlineKeyboardMarkup()
        buttons = [[(use_status , f'userin_pays_{str(kart_number)}') , (status , f'chstatus_shomarekart_{str(kart_number)}')],
                   [('حذف شماره کارت' , f'rmkart_{str(kart_number)}')]]
                     
        for row in buttons:
            button_list = []
            for text , data in row:
                button = InlineKeyboardButton(text=text , callback_data=data)
                button_list.append(button)
            keyboard.add(*button_list)

        back_button = InlineKeyboardButton('✤ - بازگشت به منوی قبلی - ✤' , callback_data='back_from_manage_shomare_kart')
        keyboard.add(back_button , row_width=1)
        return keyboard
    


# ------------------------- joinCH-section ----------------------------------------------------------------------------------------

    @staticmethod 
    def manage_joinch():
        keyboard = InlineKeyboardMarkup()
        botsettings_ = botsettings.objects.all()
        status_txt = lambda botstatus : '❌غیر فعال' if botstatus == 0 else  '✅فعال'
        for i in botsettings_:
            buttons = [[(status_txt(i.forcechjoin), 'forcechjoin') , ('جوین اجباری' , 'forcechjoin')],
                       [('مدیریت کردن چنل ها ' ,'manage_forcejoin')],]
        
        button_list = []
        for row in buttons:
            for text , data in row:
                button = InlineKeyboardButton(text=text , callback_data= data)
                button_list.append(button)
        keyboard.add(*button_list , row_width=2)

        back_button = InlineKeyboardButton('✤ - بازگشت به منوی قبلی - ✤' , callback_data='back_from_manage_force_ch')
        keyboard.add(back_button , row_width=1)

        return keyboard
    





    @staticmethod
    def manage_channels():
        keyboard = InlineKeyboardMarkup()
        channels_ = channels.objects.all()
        
        raw_top_buttons = [[('مدیریت چنل' ,'mangene') , ('ایدی چنل' , 'ch_url') , ('نام چنل' , 'ch_name')]]

        top_buttons =[]
        for i in raw_top_buttons:
            for text , data in i:
                button = InlineKeyboardButton(text=text , callback_data=data )
                top_buttons.append(button)
        keyboard.add(*top_buttons , row_width=3)


        row_button_channel = []
        for i in channels_:
            buttons = [('⚙️' , f'mfch_{str(i.id)}') , (i.channel_url or i.channel_id ,  f'mfch_{str(i.id)}') , (i.channel_name , f'mfch_{str(i.id)}')]
            row_button_channel.append(buttons)

        for row in row_button_channel:
            button_channel = []
            for text , data in row:
                button = InlineKeyboardButton(text=text , callback_data=data)
                button_channel.append(button)
            keyboard.add(*button_channel , row_width=3)

        add_ch = InlineKeyboardButton('اضافه کردن چنل جدید' , callback_data='add_new_force_channel')
        back_button = InlineKeyboardButton('✤ - بازگشت به منوی قبلی - ✤' , callback_data='back_from_managing_force_ch')
        keyboard.add(add_ch, back_button , row_width=1)
        

        return keyboard




    @staticmethod 
    def manage_ch(channel_id):
        channel_ = channels.objects.get(id = int(channel_id))
        status = 'فعال کردن' if channel_.ch_status == 0 else 'غیر فعال کردن'

        keyboard = InlineKeyboardMarkup()
        buttons = [[(status , f'status_chf_{str(channel_.id)}'), ('حذف کردن چنل' , f'rm_chf_{str(channel_.id)}')]]

        for row in buttons:
            button_list = []
            for text , data in row:
                button = InlineKeyboardButton(text=text , callback_data=data)
                button_list.append(button)
            keyboard.add(*button_list)

        back_button = InlineKeyboardButton('✤ - بازگشت به منوی قبلی - ✤' , callback_data='back_from_manage_channel')
        keyboard.add(back_button , row_width=1)
        return keyboard
    


# ------------------------- increase or decrease-section ----------------------------------------------------------------------------------------
    @staticmethod 
    def increase_or_decrease(amount_add = 1, user_id = None , current_cash = 5000 , operator = None ,):
        keyboard = InlineKeyboardMarkup()
        if amount_add == None :
            amount_add =1 
        elif amount_add  == 0:
            current_cash = current_cash * amount_add
        elif amount_add > 0 :
            current_cash = current_cash *  amount_add
        elif amount_add < 0:
            amount_add = 0
            current_cash = current_cash * amount_add
        operator_verify = 'plus' if operator == '➕' else 'mines' if operator == '➖' else None

        raw_buttons = [[(format(current_cash , ',') , 'current_cash')], 
                       [('➖' , 'operator_mines') , (str(operator) , 'operator'), ('➕' , 'operator_plus')],
                       [(f'{str(5000)} کاهش' , f'amount_decrease_{str(amount_add - 1 )}') , (f'{str(5000)} افزایش' , f'amount_increase_{str(amount_add + 1)}')],
                       [('تایید عملیات ✅' , f'verify_inde_{current_cash}_{operator_verify}_{user_id}')],
                       [('مبلغ دلخواه🔖' , 'wish_amount')],
                       [('بازگشت ' , 'back_from_increase_decrease_cash')],]
        
        for row in raw_buttons:
            buttons_list = []
            for text , data in row:
                button = InlineKeyboardButton(text=text , callback_data=data)
                buttons_list.append(button)
            keyboard.add(*buttons_list)

        return keyboard
    


# ------------------------- bot-static-section ----------------------------------------------------------------------------------------
    @staticmethod
    def bot_static(users = None, products = None, panels =None, inovices=None, payments=None):
        keyboard = InlineKeyboardMarkup()
        users_choose = '👥 -کاربران ' if users is None else '👥- کاربران☑️ '
        products_choose = '🛍 -محصولات ' if products is None else '🛍- محصولات☑️'
        panels_choose = '🎛 -پنل‌ها' if panels is None else '🎛- پنل‌ها☑️'
        inovices_choose = '📑-فاکتورها' if inovices is None else '📑- فاکتورها☑️'
        payments_choose = '💰- پرداخت‌ها ' if payments is None else "💰- پرداخت‌ها☑️"
        raw_buttons = [
                        [   
                            (panels_choose, 'panels_static'),
                            (products_choose , 'products_static'),
                            (users_choose, 'users_static'),
                            (inovices_choose, 'inovices_static'),
                            (payments_choose, 'payments_static'),
                            #('کارت ها ', 'karts_static'),
                        ],
                        [
                            ('بازگشت به منوی قبلی↪️', 'back_from_bot_statics')
                        ]
                    ]
        
        for row in raw_buttons:
            buttons_list = []
            for text , data in row :
                button = InlineKeyboardButton(text=text , callback_data=data)
                buttons_list.append(button)
            keyboard.add(*buttons_list)
        return keyboard
    

# ------------------------- block-unblock-section ----------------------------------------------------------------------------------------
    @staticmethod
    def block_unblock(user_id = None , block = None , unblock = None):
        keyboard = InlineKeyboardMarkup()
        user_id = str(user_id)
        users_ =users.objects.get(user_id=user_id)

        if block is not None :
            block_text = '✅مسدود کردن'
        else :
            block_text = 'مسدود کردن'
        
        if unblock is not None:
            unblock_text = '✅ رفع مسدودی'
        else:
            unblock_text = 'رفع مسدودی'

        block_unblock_txt = 'مسدود' if users_.block_status == 1 else 'عدم مسدودی'
        raw_button = [[(f'وضعیت یوزر :‌ {block_unblock_txt}' , f'userid_{user_id}')],
                        [(block_text , f'block_user_{user_id}'), (unblock_text , f'unblock_user_{user_id}')],
                        [('📍تایید و ارسال پیام به یوزر', f'verify_sendmsg_{user_id}')],
                        [('بازگشت ' , 'back_from_block_unblock')],]
        
        for raw in raw_button:
            button_list = []
            for text , data in raw:
                button = InlineKeyboardButton(text=text , callback_data=data)
                button_list.append(button)
            keyboard.add(*button_list)

        return keyboard