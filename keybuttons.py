import telebot
from telebot.types import InlineKeyboardMarkup , InlineKeyboardButton
from mainrobot.models import v2panel , products , admins , users
from typing import Union , List
import re , panelsapi



class BotkeyBoard:
    

    @staticmethod
    def main_menu_in_user_side(userId : int) :

        keyboard = InlineKeyboardMarkup()

        user_side_ui_buttom = [[InlineKeyboardButton(' 🚀 خرید سرویس جدید ' , callback_data ='buy_service')] ,
                               [InlineKeyboardButton(' 📡 وضعیت سرویس' , callback_data ='service_status') ,InlineKeyboardButton(' 🔄  تمدید سرویس ' , callback_data ='tamdid_service')] ,
                               [InlineKeyboardButton(' 📖 حساب کاربری ',callback_data ='wallet_profile')]
                              ]
        
        for rows in user_side_ui_buttom:
            keyboard.add(*rows)


        for i in admins.objects.all() :
            if userId == i.user_id and (i.is_owner == 1) :
                button_robot_management = InlineKeyboardButton(text = '⚙️ مدیریت ربات',callback_data = 'robot_management')
                keyboard.add(button_robot_management)

        return keyboard
    


    @staticmethod 
    def management_menu_in_admin_side() :
        keyboard = InlineKeyboardMarkup()
        admin_side_ui_buttom = [[('🖥 مدیریت پنل ها ' , 'panels_management') , ('🎛مدیریت فروشگاه' , 'products_management')] ,
                                [('📈آمار ربات' , 'bot_statics') ] , 
                                [('👤مدیریت کاربران', 'users_management'), ('🧑🏼‍💻مدیریت ادمین ها' , 'admins_management')] ,
                                [('🤖تنظیمات ربات ', 'bot_managment')], 
                                [('بازگشت به منوی اصلی 🏘' , 'back_from_management')]]
        for row in admin_side_ui_buttom :
            row_buttons = []
            for text , data in row :
                buttons = InlineKeyboardButton(text = text , callback_data = data)
                row_buttons.append(buttons)
            keyboard.add(*row_buttons)       
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

            remaing_capacity=(int(i.all_capcity) - int(i.sold_capcity)) if i.all_capcity > 0 else 0
            panel_capcity_buttons=[[(capcity_mode , 'capcity_mode') , ('🎚نوع ظرفیت ' , 'capcity_mode')] ,
                                    [(sale_mode , 'sale_mode') , ('💸حالت فروش' , 'sale_mode')] ,
                                    [(f"{abs(i.all_capcity)} عدد" , f'all_capcity_{i.all_capcity}') , ('🔋ظرفیت کلی' , f'all_capcity_{i.all_capcity}')] ,
                                    [(f"{abs(i.sold_capcity)} عدد" , 'sold_capcity') , ('💰ظرفیت فروش رفته' , 'sold_capcity')],
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
    



    """
    @staticmethod 
    def select_inbounds(inbound_selected : any = None):
        keyboard = InlineKeyboardMarkup(row_width= 1)
    

        #button2=InlineKeyboardButton(text='نوع اینباند ها' , callback_data=f'inbounds_selector_{panel_pk}')
        buttons_list = []

        if inbound_selected is not None:
            for i in inbound_selected:
                button = InlineKeyboardButton(text= i  , callback_data= i)
                buttons_list.append(button)
        keyboard.add(*buttons_list)

        done_buttons = InlineKeyboardButton('اتمام ' , callback_data='done_inbounds')
        back_buttons = InlineKeyboardButton('بازگشت' , callback_data='back_from_inbounds_selecting')
        keyboard.add(done_buttons , back_buttons)


        return keyboard 
        """




# -------------------------PRODUCTS MANAGEMENT----------------------------------------------------------------------------------------


    @staticmethod
    def product_management_menu_in_admin_side() :

        keyboard = InlineKeyboardMarkup()

        product_ui_buttom = [[('➖حذف کردن محصول ' , 'remove_product') , ('➕اضافه کردن محصول ' , 'add_product' )] ,
                             [('🔩مدیریت محصولات '  , 'manage_products')]

                            ]
        
        for i in product_ui_buttom : 
            product_ui_buttom_list = []
            for text , data in i :
                buttom = InlineKeyboardButton(text = text , callback_data = data)
                product_ui_buttom_list.append(buttom)

            keyboard.add(*product_ui_buttom_list)


        return keyboard
    








    @staticmethod 
    def product_managemet_remove_products(panel_pk , page : int = 1 , item_peer_page : int = 8) :

        top_row = [[('حذف' , 'remove_actions') , ('نام پنل ' , 'panel_related_name') , ('آدرس پنل' , 'related_panel_url') , ('نام محصول' , 'product_removal_name')]
                  ]
        
        keyboard  = InlineKeyboardMarkup()

        for i in top_row :
            top_row_buttons_list = []

            for text , data in i :
                top_row_button = InlineKeyboardButton( text  = text , callback_data = data)
                top_row_buttons_list.append(top_row_button)

            keyboard.add(*top_row_buttons_list ,row_width = 4)


        products_list = []

        start_index = (page - 1) * item_peer_page
        end_index = (page - 1 ) * item_peer_page + item_peer_page
        
        product_ = products.objects.filter(panel_id = panel_pk)

        count_products = []
        if not product_.exists():
            return 'no_products_to_remove'
        
        else :

            for i , product in enumerate(product_) : 
                count_products.append(i)
                if  start_index < i+1 <= end_index:
                    

                    for x in v2panel.objects.filter(id = product.panel_id) :
                        panelname = x.panel_name 
                        panelurl = re.sub(r'(http|https)://' , '' ,  x.panel_url)

                    product_id = str(product.id) + 'b'
                    products_list_bottom_tuple_list = [('❌' , product_id) , (panelname , panelname) , (panelurl , panelurl) , (product.product_name , product.product_name)]
                    products_list.append(products_list_bottom_tuple_list)

        
        
        
        
        for i in products_list :
            
                bottom_row_buttons_list = []

                for text , data in i :
                    bottom_row_button = InlineKeyboardButton( text = text , callback_data = data)
                    bottom_row_buttons_list.append(bottom_row_button)
                

                keyboard.add(*bottom_row_buttons_list , row_width = 4)


        next_prev_buttons = [InlineKeyboardButton(text= 'صفحه بعدی ⏪' , callback_data = f'next_page_products_{page +1}') , 
                             InlineKeyboardButton(text= 'صفحه قبل ⏩' , callback_data = f'prev_page_products_{page - 1}')
                            ]
        
        if page <= 1 :
            if len(count_products) > item_peer_page:
                keyboard.add(next_prev_buttons[0])
            if len(count_products)  < item_peer_page :
                pass


        if page > 1 and len(products_list) == item_peer_page: 
                keyboard.add(next_prev_buttons[0] , next_prev_buttons[1])
                

        elif page > 1 and len(products_list) < item_peer_page :    
                keyboard.add(next_prev_buttons[1])
#//TODO fix page bug

        back_button = InlineKeyboardButton(text = 'بازگشت ↪️' ,  callback_data = 'back_from_remove_products')  
        keyboard.add( back_button , row_width = 1)


        return keyboard














    @staticmethod
    def products_list(panel_pk , up : int = None , down : int = None , page : int = 1 , item_peer_page : int = 10):
        
        keyboard = InlineKeyboardMarkup()

        top_row = [[ ('پایین' , 'down') , ('بالا' ,'up') , ('محصول' , 'product'), ('ردیف' , 'row') ]
                   ]
        for i in top_row :
            top_buttons_list = []
            for text , data in i:
                button = InlineKeyboardButton(text = text , callback_data = data)
                top_buttons_list.append(button)
            keyboard.add(*top_buttons_list ,row_width = 4)



        bottom_row_list = []
        
        filtered_products = products.objects.filter(panel_id=panel_pk).order_by('sort_id')
        sorted_filtered_list = [(prod.sort_id, prod.id) for prod in filtered_products]
        
        
        if up is not None :
            
            for pro_sortId , pro_id in sorted_filtered_list:
                if pro_id == sorted_filtered_list[up-1][1]:
                    
                    
                    before_sort_id = sorted_filtered_list[up-2][0]
                    after_sort_id = sorted_filtered_list[up-1][0]
                    try :
                        product = products.objects.get(id = sorted_filtered_list[up-1][1])
                        new_sort_id = before_sort_id 
                        product.sort_id = new_sort_id
                        product.save()

                        product2 = products.objects.get(id = sorted_filtered_list[up-2][1])
                        new_sort_id_2 = after_sort_id
                        product2.sort_id = new_sort_id_2
                        product2.save()
                        
                    except Exception as e:
                        print(f'something wentwrong \\\ up section-1 \\\:{e}')




        if down is not None :
            
            for pro_sortId , pro_id in sorted_filtered_list:
                if pro_id == sorted_filtered_list[down-1][1]:
                    
                    if down <= len(sorted_filtered_list) - 1  : 
                        before_sort_id = sorted_filtered_list[down-1][0]
                        after_sort_id = sorted_filtered_list[down][0]
                        try :
                            productـmain = products.objects.get(id = sorted_filtered_list[down-1][1])
                            new_sort_id = after_sort_id 
                            productـmain.sort_id = new_sort_id
                            productـmain.save()

                            product2 = products.objects.get(id = sorted_filtered_list[down][1])
                            new_sort_id_2 = before_sort_id
                            product2.sort_id = new_sort_id_2
                            product2.save()
                            
                        except Exception as e:
                            print(f'something wentwrong \\\ down seciotn-1 \\\ :{e}')
                            
                    elif down >= len(sorted_filtered_list) - 1 :

                        before_sort_id = sorted_filtered_list[down- 1][0]
                        after_sort_id = sorted_filtered_list[down - down ][0]
                        try :
                            productـmain = products.objects.get(id = sorted_filtered_list[down-1][1])
                            new_sort_id = after_sort_id 
                            productـmain.sort_id = new_sort_id
                            productـmain.save()

                            product2 = products.objects.get(id = sorted_filtered_list[down - down][1])
                            new_sort_id_2 = before_sort_id
                            product2.sort_id = new_sort_id_2
                            product2.save()
                            
                        except Exception as e:
                            print(f'something wentwrong \\\ down section-2 \\\ :{e}')




        start_index = (page - 1) * item_peer_page
        end_index = (page -1 ) * item_peer_page + item_peer_page
        all_products_num = []
        
        if not filtered_products.exists():
            return 'no_product_to_manage'
        
        else :
            for num , (sort_id, produ_id) in enumerate(sorted_filtered_list):
                all_products_num.append(num)

                if start_index < num+1 <= end_index : 
                    product = products.objects.get(id=produ_id)
                    num = num + 1 
                    
                    bottom_row = [
                                    ('👇🏻', f'down_{num}'),
                                    ('👆🏻', f'up_{num}'),
                                    (product.product_name, 'detaling_product_' + str(product.id)),
                                    (num, 'row')
                                ]
                    bottom_row_list.append(bottom_row)




        for row in bottom_row_list:
            bottoms_list_unpack = []
            for text , data in row:
                button = InlineKeyboardButton(text = text , callback_data =  data)
                bottoms_list_unpack.append(button)

            keyboard.add(*bottoms_list_unpack , row_width = 5)
        
        
        
        next_prev_buttons = [InlineKeyboardButton(text= 'صفحه بعدی ⏪' , callback_data = f'product_next_page_products_{page +1}') , 
                             InlineKeyboardButton(text= 'صفحه قبل ⏩' , callback_data = f'product_prev_page_products_{page - 1}')
                            ]
        
        if page <=1 :
            if len(all_products_num) <= item_peer_page:
                pass 
            if len(all_products_num) > item_peer_page :
                keyboard.add(next_prev_buttons[0])
            


        if page > 1 and len(bottom_row_list) == item_peer_page: 
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
            buttons = [
                        [(i.product_name  , '_product_name_' + str(i.id)) , ('نام محصول' , 'product_name_')], 

                        [(data_limit_str + ' گیگ ', '_data_limit_' + str(i.id)) , ('حجم محصول' , 'data_limit_')] ,

                        [(str(i.expire_date) + ' روز ', 'ـexpire_date_' + str(i.id)) , ('مدت زمان ' , 'expire_date_')] ,

                        [(pro_cost + ' تومان ' , '_pro_cost_' + str(i.id)) , ('قیمت محمصول' , 'pro_cost_')] , 

                      ]
            

        
        
        for  i , rows in enumerate(buttons) :
            buttons_list = []
            for text , data in rows :
                button = InlineKeyboardButton(text = text , callback_data= data)
                buttons_list.append(button)
            keyboard.add(*buttons_list , row_width=2)


        back_button = InlineKeyboardButton(text = 'بازگشت ↪️' ,  callback_data = 'back_from_manage_products_changing_limit')  
        keyboard.add( back_button , row_width = 1)



        return keyboard



# -------------------------BUY SECTION----------------------------------------------------------------------------------------





    @staticmethod 
    def payby_in_user_side():
        pay_options = [('پرداخت با کیف پول' , 'pay_with_wallet') , ('پرداخت کارت به کارت' , 'pay_with_card') , ('back🔙' , 'back_from_payment')]
        keyboard = InlineKeyboardMarkup()
        for text , data in pay_options :     
            buttons = InlineKeyboardButton(text = text , callback_data = data)
            keyboard.add(buttons , row_width = 1)
        return keyboard
    





    @staticmethod 
    def agree_or_disagree(user_id , pay :int = 0): # 1 = خرید مستقیم با ارسال عکس رسید = 0 \  شارژ کیف پول با ارسال عکس رسید
        keyboard = InlineKeyboardMarkup()

        rows = [InlineKeyboardButton(text ='تایید پرداخت', callback_data= f'agree_{user_id}_{pay}'),
                InlineKeyboardButton(text ='رد پرداخت', callback_data =f'disagree_{user_id}_{pay}')]
        keyboard.add(*rows)
        
        return keyboard    
    

# ------------------------- Wallet Profile ----------------------------------------------------------------------------------------
    @staticmethod 
    def wallet_profile(user_id , info  = False):
        keyboard = InlineKeyboardMarkup()
        
        users_ = users.objects.all().filter(user_id = user_id)
        
        info_box = []     

        for i in users_  :
            wallet_num = int(i.user_wallet)
            fname = i.first_name if i.first_name  else  ''
            lname = i.last_name if i.last_name else ''
            buttons = [ 
                        [(fname + lname, f'{fname + lname}') , ('نام ' , 'fist_last_name')] ,
                        [(i.user_id , 'user_id') , ('ایدی عددی ', 'user_id')] , 
                        [(i.username , 'username') , ('یوزرنیم' , 'username')] , 
                        [(format(wallet_num , ',')+ 'تومان', 'wallet') , ('کیف پول ' , 'wallet')] , 
                        [('انتقال وجه به کاربر 💸 ' , 'tranfert_money_from_wallet')],
                        [('شارژ کیف پول 💰' , 'charge_wallet')],
                        [('بازگشت ↪️' , 'back_from_wallet_profile' )]
                    ]
            info_box.append(i.user_id )
            info_box.append(i.username)
        

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
    def wallet_accepts_or_decline(user_id , pay :int = 1): # 1 = شارژ کیف پول با ارسال عکس رسید
        keyboard = InlineKeyboardMarkup()

        rows = [InlineKeyboardButton(text ='تایید پرداخت', callback_data= f'wallet_accepts_{user_id}_{pay}'),
                InlineKeyboardButton(text ='رد پرداخت', callback_data =f'wallet_decline_{user_id}_{pay}')]
        keyboard.add(*rows)
        
        return keyboard  