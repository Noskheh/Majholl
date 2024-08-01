from mainrobot.models import v2panel , products  , inovices ,users  , payments
from telebot.types import InlineKeyboardButton , InlineKeyboardMarkup , InputMediaPhoto
from tools import QRcode_maker , farsi_parser
import decimal ,  re , panelsapi
import functions.check_fun as check_fun
from bottext import *




#- handling one panel
def plans_loading_for_one_panel(tamdid:bool= False) :
    #capcity_mode = 2 ظرفیت نامحدود / capcity_mode = 1 دارای ظرفیت / capcity_mode = 0 بدون ظرفیت
    #sale_mode = 0 فروش بسته / sale_mode 1 = فروش باز
    keyboard = InlineKeyboardMarkup()
    panels_ = v2panel.objects
    products_ = products.objects
    if not panels_.all().exists() or not products_.all().exists():
        return 'no_panel_product'
    panel_id =  [i.id for i in panels_.all()]
    products_filter = products_.filter(panel_id = panel_id[-1] ).order_by('sort_id')
    for i in panels_.all() :
        #panel_status = 1 enable
        if i.panel_status == 1:
            #sale_mode = 0 فروش بسته 
            if i.panel_sale_mode == 0 :              
                return 'sale_closed'
            #sale_mode 1 = فروش باز
            elif i.panel_sale_mode == 1 :

                if i.capcity_mode == 0:  # نوع ظرفیت :‌ بدون ظرفیت 
                    return 'sale_open_no_zarfit'
                                            
                elif i.capcity_mode == 1:  # نوع ظرفیت : دارای ظرفیت
                    if i.all_capcity > 0 :
                        for product in products_filter : 
                                if product.product_status == 1 :
                                    if tamdid is  False:
                                        call_data_1 =  f"buyservice_{product.id}_open_zarfit"
                                    else : 
                                        call_data_1 = f"newingtamdid_{product.id}_open_zarfit"
                                    buttons = InlineKeyboardButton(text = product.product_name , callback_data = call_data_1)
                                    keyboard.add(buttons) 
                        button_back_1more = InlineKeyboardButton(text = '✤ - بازگشت به منوی قبلی - ✤' , callback_data = 'back_from_chosing_product_one_panel')
                        keyboard.add(button_back_1more) 
                        return keyboard
                    else :
                        return 'sale_open_no_zarfit'
                    
                elif i.capcity_mode == 2 : # نوع ظرفیت :‌ نامحدود                 
                    for product in products_filter : 
                            if product.product_status ==1:
                                if tamdid is  False:
                                    call_data_2 =  f"buyservice_{product.id}_open_namahdod"
                                else : 
                                    call_data_2= f"newingtamdid_{product.id}_open_namahdod"
                                buttons = InlineKeyboardButton(text = product.product_name , callback_data = call_data_2)
                                keyboard.add(buttons ) 
                    button_back_1more = InlineKeyboardButton(text = '✤ - بازگشت به منوی قبلی - ✤', callback_data = 'back_from_chosing_product_one_panel')
                    keyboard.add(button_back_1more) 
                    return keyboard
        #panel_status = 0 disable
        else :
            return 'panel_disable' 







# handling two panel or more
def plans_loading_for_two_more_panel(panel_pk : int , tamdid:bool = False ) :

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
                            for product in products.objects.filter(panel_id = panel_pk).order_by('sort_id'):
                                if product.product_status == 1:
                                    if tamdid is  False:
                                        call_data_1 =  f"buyservice_{product.id}_open_zarfit"
                                    else : 
                                        call_data_1 = f"newingtamdid_{product.id}_open_zarfit"
                                    buttons = InlineKeyboardButton(text= product.product_name , callback_data= call_data_1)
                                    keyboard.add(buttons)
                            button_back_2more = InlineKeyboardButton(text = '✤ - بازگشت به منوی قبلی - ✤' , callback_data = 'back_from_chosing_product_more_panels')
                            keyboard.add(button_back_2more)  
                            return keyboard
                        else :
                            return 'sale_open_no_capcity'



                elif i.capcity_mode == 2 : # ظرفیت :نامحدود
                        for product in products.objects.filter(panel_id = panel_pk).order_by('sort_id'):
                            if product.product_status ==1 :
                                if tamdid is  False:
                                    call_data_2 =  f"buyservice_{product.id}_open_namahdod"
                                else : 
                                    call_data_2 = f"newingtamdid_{product.id}_open_namahdod"  
                                buttons = InlineKeyboardButton(text= product.product_name , callback_data=call_data_2)
                                keyboard.add(buttons)
                        button_back_2more = InlineKeyboardButton(text = '✤ - بازگشت به منوی قبلی - ✤' , callback_data = 'back_from_chosing_product_more_panels')
                        keyboard.add(button_back_2more)  
                        return keyboard

        else : 
            return 'panel_disable'



#- this is dict clear
def clear_dict(op_on_dict , user_id:int=None):
    #clear the hole dict
    if user_id is None :
        op_on_dict.clear()
        return f'dict_cleared : {op_on_dict}'
    
    #pop user in dict
    elif user_id is not None and user_id in op_on_dict:
        op_on_dict.pop(user_id)
        return f'userid : {user_id} in {op_on_dict} poped out'




#username in panel maker 
def make_username_for_panel(message ,bot, user_basket ):
    pattern = re.fullmatch(r'(\w|\d|\_)+', message.text)
    if farsi_parser.parse_farsi(message.text) == False:
        if pattern:
            users_in_panel=panelsapi.marzban(user_basket[message.from_user.id]['panel_number']).get_all_users()
            
            if users_in_panel['total'] == 0:
                user_basket[message.from_user.id]['usernameforacc'] = f'1_{message.text}'

            elif users_in_panel['total'] ==1 :
                for i in users_in_panel['users']:
                    if '_' in i['username']:
                        new_number = i['username'].split("_")[0]
                        if new_number.isdigit() :
                            user_basket[message.from_user.id]['usernameforacc'] = f'{int(new_number) + 1}_{message.text}'


            elif users_in_panel['total'] >1:
                users_username=  [i['username'] for i in users_in_panel['users']]
                new_number = users_username[-1].split("_")[0]
                if new_number.isdigit() : 
                    user_basket[message.from_user.id]['usernameforacc'] = f'{int(new_number) + 1}_{message.text}'
            user_basket[message.from_user.id]['get_username'] = False
        else : 
            bot.send_message(message.chat.id , '⚠️نام کاربری انتخابی اشتباه است لطفامجدد امتحان فرمایید ')
            return 'incorrect_username'
    else :
        bot.send_message(message.chat.id , 'حروف فارسی مجاز نمیباشد \n مجدد امتحان فرمایید')
        return 'incorrect_username'



#-pay with wallet
def pay_with_wallet( call , bot , product_dict , panel_loaded ):
    info = product_dict[call.from_user.id]
    user_ = users.objects.get(user_id = call.from_user.id)
    panel_ = v2panel.objects.get(id = info['panel_number'])
    product_price = info['pro_cost']

    if user_.user_wallet < product_price :
        bot.send_message(call.message.chat.id , '✣موجودی حساب شما کافی نمیباشد ⚠️\n ┊─ ابتدا موجودی خود را افزایش دهید و مجدد اقدام فرمایید .')

    elif user_.user_wallet >= product_price :
        new_wallet = (user_.user_wallet) - decimal.Decimal(product_price)
        try :
            user_.user_wallet = new_wallet
            user_.save()
                
        except Exception as error_1:
            print(f'an error eccured  when updating user wallet: \n\t {error_1}')
        
        if panel_loaded['one_panel'] == True  or panel_loaded['two_panels']:
            if ('open' and 'zarfit') in info['statement'] :
                check_fun.check_capcity(panel_loaded['panel_pk'])

        
        inovivces_ = create_inovices(user_id= user_ , user_username=call.from_user.username , panel_name = panel_.panel_name , product_name= info['product_name'],
                                    data_limit= info['data_limit'] , expire_date= info['expire_date'] , pro_cost= info['pro_cost'] , config_name = info['usernameforacc'] ,
                                    paid_status = 1 , paid_mode= 'wlt' , kind_pay='Buy') # 0 > unpaid , 1 > paid , 2 > waiting  , 3 > disagree
            
        payment = create_payment(user_id=user_ , amount= info['pro_cost'] , paymenent_status= 'accepted' , inovice_id=inovivces_)

        try :
            send_request = panelsapi.marzban(info['panel_number']).add_user(info['usernameforacc'] , info['product_id'])
            if send_request is False :
                return 'requset_false'
            else :
                return send_request 
        except Exception as request_error:
            print(f'error while sending request {request_error}')















#-Tamidi pay with wallet
def tamdid_pay_with_wallet(call , bot , product_dict , panel_loaded):
    info = product_dict[call.from_user.id]
    user_ = users.objects.get(user_id = call.from_user.id)
    panel_ = v2panel.objects.get(id = info['panel_number'])
    product_price = info['pro_cost']

    if user_.user_wallet < product_price :
        bot.send_message(call.message.chat.id , '⚠️موجودی حساب شما کافی نمیباشد ')

    elif user_.user_wallet >= product_price :
        new_wallet = (user_.user_wallet) - decimal.Decimal(product_price)
        try :
            user_.user_wallet = new_wallet
            user_.save()
                
            if panel_loaded['one_panel'] == True :
                if  ('open' and 'withcapcity') in info['statement'] :
                    check_fun.check_capcity(panel_loaded['panel_pk'])

            else :
                if panel_loaded['two_panel'] == True :
                    if  ('open' and 'withcapcity')  in info['statement']:
                        check_fun.check_capcity(panel_loaded['panel_pk'])

        except Exception as error_1:
            print(f'an error eccured  when updating user wallet: \n\t {error_1}')
        

        inovivces_ = create_inovices(user_id= user_ , user_username= call.from_user.username ,
                                        panel_name = panel_.panel_name , product_name= info['product_name'],
                                        data_limit= info['data_limit'] , expire_date= info['expire_date'] ,
                                        pro_cost= info['pro_cost'] , config_name = info['config_name'] ,
                                        paid_status = 1 , # 0 > unpaid , 1 > paid , 2 > waiting  , 3 > disagree 
                                        paid_mode= 'wlt', kind_pay='Tamdid' )
            
        inovivces2_ = inovices.objects.filter(user_id = user_).latest('created_date')
        payments_ = payments.objects.create(user_id = user_ , amount = info['pro_cost'] ,payment_stauts = 'accepted' , inovice_id = inovivces2_)
        send_request = panelsapi.marzban(info['panel_number']).put_user(info['config_name'] , info['product_id'])
        if send_request is False :
            return 'requset_false'
        else :
            return send_request 








def create_paycard_fish(tamdid:bool =False):
    if tamdid is not False:
        user_fish = {'tamdid_fish_send' : False , 'tamdid_accpet_or_reject':False}
        return user_fish
    
    user_fish = {'fish_send' : False , 'accpet_or_reject':False , 'inovices' :None}    
    return user_fish
    

#pay with card

def pay_with_card(call , bot , product_dict , user_fish ):
    info = product_dict[call.from_user.id]
    panel_name = v2panel.objects.get(id=info['panel_number'] ).panel_name
    users_ = users.objects.get(user_id=call.from_user.id )

    inovivces_ = create_inovices(user_id= users_ , user_username=call.from_user.username ,panel_name = panel_name , 
                                product_name= info['product_name'], data_limit= info['data_limit'] , expire_date= info['expire_date'] ,
                                pro_cost= info['pro_cost'] , config_name = info['usernameforacc'] ,paid_status= 2 ,
                                paid_mode= 'kbk' ,kind_pay='Buy')  # 0 > unpaid , 1 > paid , 2 > waiting  , 3 > disagree
    
    
    if call.from_user.id not in user_fish :
        user_fish[call.from_user.id] = create_paycard_fish()
    user_fish[call.from_user.id]['inovices'] = inovivces_
    user_fish[call.from_user.id]['fish_send'] = True
    bot.send_message(chat_id = call.message.chat.id , text = buy_service_section_card_to_card_msg(info['pro_cost']))









def tamdid_pay_with_card(call , bot , product_dict , user_fish ):
    info = product_dict[call.from_user.id]

    panel_name = v2panel.objects.get(id=info['panel_number'] ).panel_name
    users_ = users.objects.get(user_id=call.from_user.id )

    inovivces_ = create_inovices(user_id= users_ , user_username=call.from_user.username ,
                                panel_name = panel_name , product_name= info['product_name'],
                                data_limit= info['data_limit'] , expire_date= info['expire_date'] ,
                                pro_cost= info['pro_cost'] , config_name = info['config_name'] ,
                                paid_status= 2 , # 0 > unpaid , 1 > paid , 2 > waiting  , 3 > disagree
                                paid_mode= 'kbk' , kind_pay='Tamdid' )
   
    
    if call.from_user.id not in user_fish :
        user_fish[call.from_user.id] = create_paycard_fish(tamdid=True)

    user_fish[call.from_user.id]['tamdid_fish_send'] = True
    bot.send_message(chat_id = call.message.chat.id , text = buy_service_section_card_to_card_msg(info['pro_cost']))







def how_to_send(request_ , panel_id , BOT , call_userid):
    panel_ = v2panel.objects.get(id= panel_id)

    if panel_.send_qrcode_mode == 1 : #subscription QRcode
        sub_link = request_['subscription_url']
        
        qr_code_subscription = QRcode_maker.make_qrcode(sub_link)
        link = '\n'.join(request_['links'])
 

        if panel_.send_links_mode == 1: #subscription link 
            BOT.send_photo(call_userid, qr_code_subscription , buy_service_section_product_send('لینک هوشمند ' ,  sub_link))
                    

        elif panel_.send_links_mode == 2: #config link  
            BOT.send_photo(call_userid , caption= buy_service_section_product_send('لینک هوشمند به همراه لینک کانفیگ' , '👇🏻') , photo= qr_code_subscription)
            BOT.send_message(call_userid , f'<code>{link}</code>')


        elif panel_.send_links_mode == 0 : # dont using links in caption
            BOT.send_photo(call_userid , qr_code_subscription , buy_service_section_product_send('لینک هوشمند' , image_only=True))



    elif panel_.send_qrcode_mode == 2 : #config link Qrcode
        config_link = request_['links']
        sub_link = request_['subscription_url'] 
        link = ' \n '.join(config_link)
        config_list = []

        for config in config_link :
            qr_code_config = QRcode_maker.make_qrcode(config) 
            config_list.append(InputMediaPhoto(qr_code_config))


        if panel_.send_links_mode == 1: # subsctrption link 
            config_list[-1] = InputMediaPhoto(config_list[-1].media  ,buy_service_section_product_send('qrcode کانفیگ به همراه لینک هوشمند' , sub_link ) , parse_mode="HTML" )
            BOT.send_media_group(call_userid , config_list)
           
                        


        if panel_.send_links_mode == 2: # config link 
            config_list[-1] = InputMediaPhoto(config_list[-1].media , buy_service_section_product_send('لینک کانفیگ به همراه qrcode کانفیگ ' , '👇🏻') , parse_mode="HTML")
            BOT.send_media_group(call_userid,  config_list)
            BOT.send_message(call_userid ,link )



        if panel_.send_links_mode == 0 :
            config_list[-1] = InputMediaPhoto(config_list[-1].media , buy_service_section_product_send('qrcode کانفیگ ', image_only= True) , parse_mode="HTML" )
            BOT.send_media_group(call_userid , config_list)







#------------------------------ creations db objects ---------------------------------------------------------
def create_payment(user_id , amount , paymenent_status , inovice_id):
    try:
        payment_ =payments.objects.create(user_id=user_id , amount=amount , payment_stauts=paymenent_status , inovice_id=inovice_id)
        return payment_
    except Exception as payment_error:
        print(f'an error eccoured when adding payment {payment_error}')



def create_inovices(user_id  , panel_name , product_name , data_limit , expire_date , pro_cost ,  paid_status , kind_pay ,config_name : None , paid_mode : str , gift_code : int = None , discount : int = None , user_username : str = None):  
    try :
        inovices_ = inovices.objects.create(user_id=user_id ,user_username=user_username ,panel_name=panel_name ,
                            product_name=product_name  ,data_limit=data_limit ,expire_date=expire_date ,
                            pro_cost=pro_cost ,gift_code=gift_code ,discount=discount ,
                            config_name=config_name ,  paid_status = paid_status ,paid_mode=paid_mode ,
                            kind_pay=kind_pay)   
        return inovices_
    except Exception as error:
        print(f'an error eccoured when adding inovices : {error}')



