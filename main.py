#all modules imported in here
import telebot , re , json , BOTTOKEN , panelsapi 
from telebot.types import InlineKeyboardMarkup , InlineKeyboardButton , ReplyKeyboardMarkup, KeyboardButton  , ReplyKeyboardRemove
from mainrobot.models import users , admins , v2panel , products , inovices , payments , subscriptions , shomarekart ,botsettings
from keybuttons import BotkeyBoard as BotKb
from django.db.models import Max , Min , Avg , Sum , Count
from functions.USERS_onstarts import *
from functions.PANEL_managing import *
from functions.PRODUCTS_managing import *
from functions.BUY_services import * 
from functions.check_fun import *
from tools import QRcode_maker
from bottext import *
import jdatetime , datetime
#------------------------------------------------------------

bot = telebot.TeleBot(token=BOTTOKEN.TOKEN[0], parse_mode="HTML", colorful_logs=True)



#??//TODO avoid user from populating dictionaries  i mean when user wants to find his service and call its button he may leave it alone for long time and dicts will be populate for long time


#= Welcomer

@bot.message_handler(func=lambda message: '/start' in message.text)
def start_bot(message) :
    user_ = message.from_user 
    CHECKING_USER = CHECK_USER_EXITENCE(user_.id , user_.first_name , user_.last_name , user_.username , 0 )

    if message.text and '/start' in message.text:
        
        if PHONE_NUMBER(user_.id) is False: 
            if BLOCK_OR_UNBLOCK(UserId= user_.id) is False :
                if FORCE_JOIN_CHANNEL(UserId=user_.id , Bot=bot) == True :
                    #- Canceling operations : panels , product
                    PANEL_RECEIVING_STATE['Enable_Panel_Adding'] = False
                    PRODUCT_RECEIVING_STATE['enable_product_adding'] = False
                    CHANGING_PANEL_DETAILS.update({key : False for key in CHANGING_PANEL_DETAILS})
                    CHNAGING_PRODUCT_DETAILS['Enable_Changing_Product_Deatails'] = False
                    USER_ADMIN_INFO['admin_name'] = False
                    USER_ADMIN_INFO['add_admin'] = False
                    
                    #clear requests 
                    clear_dict(marzban_panel_api_user , message.from_user.id)
                    #clear USER_BASKETS 
                    clear_dict(USERS_BASKET , message.from_user.id)
                    clear_dict(USER_PAYCARD_FISH , message.from_user.id)   
                    #clear TAMDID_BASKERS_USER 
                    clear_dict(TAMDID_BASKETS_USER , message.from_user.id)
                    clear_dict(TAMDID_FISH , message.from_user.id )
                    #clear USER_STATE
                    clear_dict(USER_STATE , message.from_user.id)
                    #clear USER_QUERY_SERVICE
                    clear_dict(USER_QUERY_SERVICE , message.from_user.id)
                    #clear TRANSFER_MONEY_USRTOUSR
                    clear_dict(TRANSFER_MONEY_USRTOUSR , message.chat.id )
                    # clear CHARGE_WALLET
                    clear_dict(CHARGE_WALLET , message.from_user.id)
                    #clear INCREASE_DECREASE CAHS
                    clear_dict(USER_INCREASE_DECREASE_CASH , message.from_user.id)

                    bot.send_message(message.chat.id , welcome_msg , reply_markup= BotKb.main_menu_in_user_side(message.from_user.id))

                else :
                    bot.send_message(message.chat.id , text=force_channel_join_msg, reply_markup=BotKb.load_channels(bot , user_.id))
            else :
                bot.send_message(message.chat.id , text='⚠️شما در ربات مسدود شده اید\n و امکان استفاده از ربات را ندارید ')

        else:
            USER_PHONE_NUMBER[message.from_user.id] = {'get_number':True}
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True ,one_time_keyboard=True)
            button = KeyboardButton('ارسال شماره', request_contact=True )
            keyboard.add(button)
            Text_1 =  'پیش از ادامه کار با ربات لطفا شماره خود را ارسال نمایید'
            bot.send_message(message.chat.id , Text_1 , reply_markup=keyboard)





#- handles all incoming channels_joined call.data 
@bot.callback_query_handler(func=lambda call : call.data=='channels_joined')
def channels_joined(call):
    if call.data=='channels_joined':
        if FORCE_JOIN_CHANNEL(call.from_user.id , bot) == True:
            bot.edit_message_text(welcome_msg , call.message.chat.id , call.message.message_id , reply_markup= BotKb.main_menu_in_user_side(call.message.from_user.id))
        else:
            Text_1='⚠️شما هنوز در چنل های ما جوین نشده اید⚠️'
            bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.load_channels(bot , call.from_user.id))



USER_PHONE_NUMBER = {}

#- get user contact 
@bot.message_handler(func= lambda message:  message.from_user.id in USER_PHONE_NUMBER and len(USER_PHONE_NUMBER)>=1 and USER_PHONE_NUMBER[message.from_user.id]['get_number'] ==True and message.content_type =='contact', content_types=['contact'])
def get_user_phone(message):
    if message.from_user.id in USER_PHONE_NUMBER and len(USER_PHONE_NUMBER)>=1 and USER_PHONE_NUMBER[message.from_user.id]['get_number'] ==True :
        patter = r'^([+98]|[+225]|[+7])+[0-9]{10}$'
        contact_msg = message.contact.phone_number
        check_phone_number = re.search(patter , contact_msg)
        if check_phone_number:
            
            try :
                if BLOCK_OR_UNBLOCK(UserId= message.from_user.id) is False :
                    if FORCE_JOIN_CHANNEL(UserId=message.from_user.id , Bot=bot) == True :
                        users_ = users.objects.get(user_id = message.from_user.id)
                        users_.phone_number = check_phone_number.group(0)
                        users_.save()
                        clear_dict(USER_PHONE_NUMBER , message.from_user.id)
                        bot.send_message(message.chat.id , 'اطلاعات شما با موفقیت دریافت شد' , reply_markup=ReplyKeyboardRemove())
                        time.sleep(1.5)
                        bot.send_message(message.chat.id , welcome_msg , reply_markup= BotKb.main_menu_in_user_side(message.from_user.id))

                    else :

                        bot.send_message(message.chat.id , text=force_channel_join_msg, reply_markup=BotKb.load_channels(bot , message.from_user.id))
                else :
                    bot.send_message(message.chat.id , text='⚠️شما در ربات مسدود شده اید\n و امکان استفاده از ربات را ندارید ')
            
            except Exception as phone_number_error:
                print(f'error while adding phone number to user: error_msg : {phone_number_error}')
        else:
            bot.send_message(message.chat.id , 'شماره های غیر ایرانی مجازی نمیباشد', reply_markup=ReplyKeyboardRemove())
        










# - 1 user-side
# --------------------------------------------------------------------------------------------------------------------------
# ------------------------- BUY-SERVICES -----------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------

#> ./buy_services : selecting all plans if olny have on panel

def create_product_entry(tamdid :bool =False):
    if tamdid is False :
        return {'panel_number':'', 'product_id': 0, 'product_name':'',
            'data_limit':'', 'expire_date':'', 'pro_cost':'',
            'get_username':False, 'usernameforacc':'',
            'statement':[]}
    else:
        return {'panel_number':'', 'product_id':0, 'product_name':'',
            'data_limit':'', 'expire_date':'', 'pro_cost':'',
            'config_name':str, 'statement':[]}
    

def payment_decline_reason_create():
    payment_decline_reason_on_buy = {'reason' : False  , 'user_id' : int , 'payment':None}
    return payment_decline_reason_on_buy
   

USER_STATE  = {}
USERS_BASKET = {}
USER_PAYCARD_FISH = {}
PAYMENT_DECLINE_REASON_ON_BUY = {}
NUMBER_OF_PANEL_LOADED={'one_panel':False ,'two_panels':False , 'panel_pk':int}
    




@bot.callback_query_handler(func=lambda call:call.data in ['buy_service' , 'back_from_chosing_product_one_panel', 'back_from_chosing_panels_buying', 'back_from_chosing_product_more_panels' ])
def handler_buy_service_one_panel(call):   
    panels_ = v2panel.objects.all()
    panel_id = [i.id for i in panels_]

    if BLOCK_OR_UNBLOCK(UserId= call.from_user.id) is False :
    #check user is joined or not
        if FORCE_JOIN_CHANNEL(call.from_user.id , bot) ==True :
            
            #check received call.data and panels count
            if  call.data == 'buy_service' and  panels_.count() <= 1  : 


                if plans_loading_for_one_panel() == 'panel_disable' :
                    bot.send_message(call.message.chat.id , '⌛️پنل در حال بروزرسانی میباشد . لطفا بعدا مراجعه فرمایید')
                else : 
                    if isinstance(plans_loading_for_one_panel() , InlineKeyboardMarkup):
                        bot.edit_message_text(buy_service_section_product_msg , call.message.chat.id , call.message.message_id , reply_markup = plans_loading_for_one_panel())      

                        NUMBER_OF_PANEL_LOADED['one_panel'] = True
                        NUMBER_OF_PANEL_LOADED['panel_pk'] = panel_id[-1]

                        if call.from_user.id not in USERS_BASKET:
                                USERS_BASKET[call.from_user.id] = create_product_entry()
                        USERS_BASKET[call.from_user.id]['panel_number']= panel_id[-1]


                if plans_loading_for_one_panel() == 'sale_closed' :
                    bot.send_message(call.message.chat.id , '⛔️فروش سرویس بسته میباشد ، بعدا مراجعه فرمایید')

                if plans_loading_for_one_panel() == 'sale_open_no_zarfit' :
                    bot.send_message(call.message.chat.id , '🪫ظرفیت فروش به اتمام رسیده است . بعدا مراجعه فرمایید')

                if plans_loading_for_one_panel() == 'no_panel_product' : 
                    bot.send_message(call.message.chat.id , '‼️متاسفیم ، هنوز هیچ سرور یا محصولی برای ارائه وجود ندارد' )


                
            if call.data == 'buy_service' and panels_.count() >= 2 :
                bot.edit_message_text(buy_service_section_choosing_panel_msg , call.message.chat.id , call.message.message_id , reply_markup=BotKb.chosing_panels_in_buying_section())


        else :
            bot.send_message(call.message.chat.id , text=force_channel_join_msg, reply_markup=BotKb.load_channels(bot , call.from_user.id))
    
    else :
        bot.send_message(call.message.chat.id , text='⚠️شما در ربات مسدود شده اید\n و امکان استفاده از ربات را ندارید ')



    #-back - buttons - for one panel 
    if call.data == 'back_from_chosing_product_one_panel' : 
         bot.edit_message_text( welcome_msg , call.message.chat.id , call.message.message_id , reply_markup = BotKb.main_menu_in_user_side(call.from_user.id))
        
    if call.data == 'back_from_chosing_panels_buying':
        bot.edit_message_text(welcome_msg, call.message.chat.id , call.message.message_id , reply_markup = BotKb.main_menu_in_user_side(call.from_user.id))

    if call.data == 'back_from_chosing_product_more_panels':
        bot.edit_message_text(buy_service_section_choosing_panel_msg , call.message.chat.id , call.message.message_id , reply_markup=BotKb.chosing_panels_in_buying_section())












#> ./buy service : two panels buying / TBSpanel = TWO PANEL BUY SERVICE
@bot.callback_query_handler(func = lambda call : call.data.startswith('TBSpanel_pk_'))
def handle_buy_service_two_panel(call):

    if BLOCK_OR_UNBLOCK(UserId= call.from_user.id) is False :
    #check user is joined or not
        if FORCE_JOIN_CHANNEL(call.from_user.id , bot) == True :

            if call.data.startswith('TBSpanel_pk_') :
                call_data = call.data.split('_')
                if plans_loading_for_two_more_panel(panel_pk= call_data[-1]) == 'panel_disable':
                    bot.send_message(call.message.chat.id , '⌛️پنل در حال بروزرسانی میباشد . لطفا بعدا مراجعه فرمایید')
                
                else :
                    if isinstance(plans_loading_for_two_more_panel(panel_pk= call_data[-1]) , InlineKeyboardMarkup) :
                        bot.edit_message_text(buy_service_section_product_msg , call.message.chat.id , call.message.message_id , reply_markup = plans_loading_for_two_more_panel(panel_pk= call_data[-1]))
                        
                        NUMBER_OF_PANEL_LOADED['two_panels'] = True
                        NUMBER_OF_PANEL_LOADED['panel_pk']= call.data.split('_')[-1]

                        if call.from_user.id not in USERS_BASKET:
                            USERS_BASKET[call.from_user.id] = create_product_entry()

                        USERS_BASKET[call.from_user.id]['panel_number'] =  call.data.split('_')[-1]

                if plans_loading_for_two_more_panel(panel_pk= call_data[-1]) == 'sale_closed':
                    bot.send_message(call.message.chat.id , '⛔️فروش سرویس بسته میباشد ، بعدا مراجعه فرمایید')

                if  plans_loading_for_two_more_panel(panel_pk= call_data[-1]) == 'sale_open_no_capcity':
                    bot.send_message(call.message.chat.id , '🪫ظرفیت فروش به اتمام رسیده است . بعدا مراجعه فرمایید')

                if plans_loading_for_two_more_panel(panel_pk= call_data[-1]) == 'no_products':
                    bot.send_message(call.message.chat.id , '‼️متاسفیم ، هنوز هیچ سرور یا محصولی برای ارائه وجود ندارد')
        else :
            bot.send_message(call.message.chat.id , text=force_channel_join_msg, reply_markup=BotKb.load_channels(bot , call.from_user.id))
    
    else :
        bot.send_message(call.message.chat.id , text='⚠️شما در ربات مسدود شده اید\n و امکان استفاده از ربات را ندارید ')










#> ./buy_services > selecting products plans
@bot.callback_query_handler(func = lambda call : call.data.startswith('buyservice_'))
def handle_buyService_select_proplan(call) :
    if BLOCK_OR_UNBLOCK(UserId= call.from_user.id) is False :
        if FORCE_JOIN_CHANNEL(call.from_user.id , bot) == True:

            if call.data.startswith('buyservice_') :
                if call.from_user.id in USERS_BASKET:
                    call_data = call.data.split("_")
                    USERS_BASKET[call.from_user.id]['get_username'] = True
                    USERS_BASKET[call.from_user.id]['product_id'] = call_data[1]
                    USERS_BASKET[call.from_user.id]['statement'] = [call_data[2] , call_data[3]] 


                    
                    if call.from_user.id in USER_STATE and USER_STATE[call.from_user.id][0] in ('find_user_service' , 'charge_wallet'):
                        clear_dict(USER_QUERY_SERVICE , call.from_user.id)
                        clear_dict(CHARGE_WALLET , call.from_user.id)

                    USER_STATE[call.from_user.id] = ['buying_new_service' , time.time()]

                    bot.edit_message_text(buy_service_section_choosing_username_msg , call.message.chat.id , call.message.message_id)
        else :
            bot.send_message(call.message.chat.id , text=force_channel_join_msg, reply_markup=BotKb.load_channels(bot , call.from_user.id))
    else :
        bot.send_message(call.message.chat.id , text='⚠️شما در ربات مسدود شده اید\n و امکان استفاده از ربات را ندارید ')








#> ./buy_services > get user username 
@bot.message_handler(func=lambda message:(message.from_user.id in USERS_BASKET and len(USERS_BASKET) != 0  and USERS_BASKET[message.from_user.id]['get_username']==True))
def get_username_for_config_name(message):

    if BLOCK_OR_UNBLOCK(UserId= message.from_user.id) is False :

        if FORCE_JOIN_CHANNEL(UserId=message.from_user.id , Bot=bot)==True:

            if USERS_BASKET[message.from_user.id]['get_username']==True:
                if message.text == '/cancel' or message.text == '/cancel'.upper():
                    clear_dict(USERS_BASKET , message.from_user.id)
                    bot.send_message(message.chat.id , welcome_msg , reply_markup=BotKb.main_menu_in_user_side(message.from_user.id)) 
                else: 
                    if make_username_for_panel(message , bot , USERS_BASKET) != 'incorrect_username':
                        USERS_BASKET[message.from_user.id] ['get_username'] = False
                        call_data = USERS_BASKET[message.from_user.id]['product_id']
                        product_ = products.objects.get(id = call_data)
                        USERS_BASKET[message.from_user.id] ['product_name'] = product_.product_name
                        USERS_BASKET[message.from_user.id] ['data_limit'] = product_.data_limit
                        USERS_BASKET[message.from_user.id] ['expire_date'] = product_.expire_date
                        USERS_BASKET[message.from_user.id] ['pro_cost'] = product_.pro_cost
                        bot.send_message(message.chat.id , product_info_msg(USERS_BASKET[message.from_user.id]) , reply_markup=BotKb.confirmation())
        else :
            bot.send_message(message.chat.id , text=force_channel_join_msg, reply_markup=BotKb.load_channels(bot , message.from_user.id))
    else :
        bot.send_message(message.chat.id , text='⚠️شما در ربات مسدود شده اید\n و امکان استفاده از ربات را ندارید ')





#> ./buy_services > proccess selected product plan 
@bot.callback_query_handler(func = lambda call : call.data in ['verify_product' , 'pay_with_wallet' , 'pay_with_card' , 'back_from_verfying' , 'back_from_payment'] )
def handle_selected_products(call) : 
    if BLOCK_OR_UNBLOCK(UserId= call.from_user.id) is False :

        if FORCE_JOIN_CHANNEL(UserId=call.from_user.id , Bot=bot)==True:

            if call.data == 'verify_product' :
                bot.edit_message_text('⚪️ یک روش پرداخت را انتخاب نمایید' , call.message.chat.id , call.message.message_id , reply_markup=BotKb.payby_in_user_side()) 
        else :
            bot.send_message(call.message.chat.id , text=force_channel_join_msg, reply_markup=BotKb.load_channels(bot , call.from_user.id))
    else :
        bot.send_message(call.message.chat.id , text='⚠️شما در ربات مسدود شده اید\n و امکان استفاده از ربات را ندارید ')




    #pay wallet
    if call.data == 'pay_with_wallet':
        req =pay_with_wallet(call , bot , USERS_BASKET , NUMBER_OF_PANEL_LOADED)
        if req != ('requset_false' or 'insufficent' or None) :
            if isinstance(req , dict):
                bot.edit_message_text(paied_msg , call.message.chat.id , call.message.message_id)
                bot.send_chat_action(chat_id=call.message.chat.id, action='typing')
                time.sleep(2.5)
                how_to_send(req , int(USERS_BASKET[call.from_user.id]['panel_number']) , bot , call.from_user.id)
                users_ = users.objects.get(user_id = call.from_user.id)
                panels_= v2panel.objects.get(id = USERS_BASKET[call.from_user.id]['panel_number'])
                products_ = products.objects.get(id =USERS_BASKET[call.from_user.id]['product_id'] )
                subscriptions_ = subscriptions.objects.create(user_id = users_ , product_id = products_ , panel_id = panels_ , user_subscription = USERS_BASKET[call.from_user.id]['usernameforacc'])
                clear_dict(USERS_BASKET , call.from_user.id)  
        else :
            print(f'something happened when sending request : {req}')


    #pay card
    if call.data == 'pay_with_card':
        pay_with_card(call , bot , USERS_BASKET , USER_PAYCARD_FISH)



    #back - buttons
    if call.data == 'back_from_verfying':
        bot.edit_message_text(welcome_msg , call.message.chat.id , call.message.message_id , reply_markup = BotKb.main_menu_in_user_side(call.from_user.id))
        bot.answer_callback_query(call.id , 'ادامه خرید محصول لغو شد')
        clear_dict(USERS_BASKET , call.from_user.id)


    #back - buttons
    if call.data == 'back_from_payment':
        bot.edit_message_text(welcome_msg , call.message.chat.id , call.message.message_id , reply_markup= BotKb.main_menu_in_user_side(call.from_user.id))
        bot.answer_callback_query(call.id , 'پرداخت لغو شد')
        clear_dict(USERS_BASKET , call.from_user.id)











# ./buy_service > seding fish section
@bot.message_handler(func = lambda message : (message.from_user.id in USER_PAYCARD_FISH and len(USER_PAYCARD_FISH) > 0  and USER_PAYCARD_FISH[message.from_user.id]['fish_send'] ==True) , content_types=['photo' , 'text'])
def getting_fish_image(message):

    users_ = users.objects.get(user_id = message.from_user.id)
    admins_ = admins.objects.all()
    inovices_ = inovices.objects
    if message.from_user.id in USER_PAYCARD_FISH and len(USER_PAYCARD_FISH) > 0  and USER_PAYCARD_FISH[message.from_user.id]['fish_send'] ==True :
        #if user cancel his inovice
        if message.content_type  == 'text'  and message.text =='/cancel' or message.text=='/cancel'.upper():
            inovieces_ = inovices.objects.get(id = USER_PAYCARD_FISH[message.from_user.id]['inovices'].id)
            inovieces_.paid_status = 0 
            inovieces_.save()
            clear_dict(USERS_BASKET , message.from_user.id)
            clear_dict(USER_PAYCARD_FISH ,message.from_user.id)
            bot.send_message(message.chat.id , welcome_msg , reply_markup= botkb.main_menu_in_user_side(message.from_user.id))
        else:
        #check time
            if check_time_passed(USER_PAYCARD_FISH[message.from_user.id]['inovices'].id) == 'time_passed':
                update_inovice_status = inovices_.get(id = int(USER_PAYCARD_FISH[message.from_user.id]['inovices'].id))   
                update_inovice_status.paid_status = 0 # paid_status = 0 / unpaid due to passing time
                update_inovice_status.save()
                bot.send_message(message.chat.id , inovice_time_passed_msg)

            else :
                
                panel_id = NUMBER_OF_PANEL_LOADED['panel_pk'] if NUMBER_OF_PANEL_LOADED['one_panel'] == True else NUMBER_OF_PANEL_LOADED['panel_pk']
                panel_name = v2panel.objects.get(id = panel_id).panel_name
                user_info = users.objects.get(user_id = message.from_user.id)  
                if message.content_type == 'photo':
                    for i in admins_:
                            bot.send_photo(i.user_id , message.photo[-1].file_id , caption = send_user_buy_request_to_admins(USERS_BASKET[message.from_user.id] ,user_info , panel_name ) , reply_markup= BotKb.agree_or_disagree(message.from_user.id))
                    bot.send_message(message.chat.id ,send_success_msg_to_user)
                USER_PAYCARD_FISH[message.from_user.id]['fish_send'] = False
                USER_PAYCARD_FISH[message.from_user.id]['accpet_or_reject'] = True





@bot.callback_query_handler(func = lambda call : call.data.startswith('agree_') or call.data.startswith('disagree_') )
def agree_or_disagree_kbk_payment(call):
    
    call_data = call.data.split('_')

    user_basket = USERS_BASKET[int(call_data[1])]
    #agree section
    if call.data.startswith('agree_')  and (int(call_data[1]) in USER_PAYCARD_FISH and len(USER_PAYCARD_FISH) >=1 and  USER_PAYCARD_FISH[int(call_data[1])]['accpet_or_reject']) == True:

        inovices_ = inovices.objects.get(id = USER_PAYCARD_FISH[int(call_data[1])]['inovices'].id)
        users_ = users.objects.get(user_id = int(call_data[1]))
        inovices_.paid_status = 1
        inovices_.save()
        payments = create_payment(user_id=users_ , amount= user_basket['pro_cost'] , paymenent_status='accepted' , inovice_id= inovices_)
        #check panel capcity       
        if NUMBER_OF_PANEL_LOADED['one_panel'] == True  or NUMBER_OF_PANEL_LOADED['two_panels']:
            if ('open' and 'zarfit') in user_basket['statement'] :
                PANEL_managing.check_capcity(NUMBER_OF_PANEL_LOADED['panel_pk'])
                
        bot.reply_to(call.message, f'درخواست پرداخت یوزر : {str(call_data[1])} انجام شد')
        bot.send_message(int(call_data[1]) , paied_msg)

        try :
            send_request = panelsapi.marzban(user_basket['panel_number']).add_user(user_basket['usernameforacc'] , user_basket['product_id'])
        except Exception as request_error:
            print(f'error while sending request {request_error}')
            
        bot.send_chat_action(int(call_data[1]) , action='typing')
        time.sleep(3)
        how_to_send(send_request , user_basket['panel_number'] , bot , int(call_data[1]))

        users_ = users.objects.get(user_id = int(call_data[1]))
        panels_= v2panel.objects.get(id = USERS_BASKET[int(call_data[1])]['panel_number'])
        products_ = products.objects.get(id =USERS_BASKET[int(call_data[1])]['product_id'] )
        subscriptions_ = subscriptions.objects.create(user_id = users_ , product_id = products_ , panel_id = panels_ , user_subscription = USERS_BASKET[int(call_data[1])]['usernameforacc'])
           
        clear_dict(USERS_BASKET , int(call_data[1])) 
        clear_dict(USER_PAYCARD_FISH , int(call_data[1]))




    #reject payment 
    if call.data.startswith('disagree_')  and (int(call_data[1]) in USER_PAYCARD_FISH and len(USER_PAYCARD_FISH) >=1 and  USER_PAYCARD_FISH[int(call_data[1])]['accpet_or_reject']) == True:
        users_ = users.objects.get(user_id = int(call_data[1]))
        inovices_ = inovices.objects.get(id = USER_PAYCARD_FISH[int(call_data[1])]['inovices'].id)
        inovices_.paid_status = 3
        inovices_.save()
        payments = create_payment(user_id=users_ , amount= user_basket['pro_cost'] , paymenent_status='declined' , inovice_id= inovices_)
        
        bot.send_message(call.message.chat.id , 'علت رد پرداخت را ارسال کنید')
        
        if int(call_data[1]) not in PAYMENT_DECLINE_REASON_ON_BUY :
                PAYMENT_DECLINE_REASON_ON_BUY[int(call_data[1])] = payment_decline_reason_create()

        PAYMENT_DECLINE_REASON_ON_BUY[int(call_data[1])]['reason'] = True
        PAYMENT_DECLINE_REASON_ON_BUY[int(call_data[1])]['user_id'] = int(call_data[1])
        PAYMENT_DECLINE_REASON_ON_BUY[int(call_data[1])]['payment'] = payments
        USER_PAYCARD_FISH[int(call_data[1])]['accpet_or_reject'] = False



# ./buy services > disagree of fish : getting reason
@bot.message_handler(func= lambda message :  len(PAYMENT_DECLINE_REASON_ON_BUY) ==1 )
def get_decline_reason(message):   


    user_id = str 
    for i in PAYMENT_DECLINE_REASON_ON_BUY.keys():
        user_id = i

    if PAYMENT_DECLINE_REASON_ON_BUY[user_id]['reason'] == True : 
        payments_ = payments.objects.get(id = PAYMENT_DECLINE_REASON_ON_BUY[int(user_id)]['payment'].id)
        payments_.decline_reason = message.text
        payments_.save()
        user_reject_reason = f"""
🔴درخواست شما رد شد 
       ┘ 🔻 علت : ‌ {message.text}
.
       """
        
        admin_reject_reason= f"""
درخواست پرداخت رد شد ❌
     ¦─  یوزر درخواست کننده: ‌{user_id}
     ¦─  علت رد درخواست : ‌{message.text}
     ¦─  شماره فاکتور :‌ {payments_.inovice_id.pk}
     ¦─  شماره پرداخت :‌  {payments_.id}
     
.
     """
        
        bot.send_message(user_id ,  user_reject_reason)
        bot.send_message(message.chat.id , admin_reject_reason)
        #cleaning dicts
        clear_dict(USERS_BASKET , user_id)
        clear_dict(USER_PAYCARD_FISH , user_id)
        clear_dict(PAYMENT_DECLINE_REASON_ON_BUY , user_id)
















# - 2 user-side
# --------------------------------------------------------------------------------------------------------------------------
# ------------------------- SERVICE-STATUS ---------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------

marzban_panel_api_user = {}
RM_MYSUB = {}
USER_QUERY_SERVICE = {}


@bot.callback_query_handler(func= lambda call: call.data in ['service_status' ,  'get_config_link' , 'get_qrcode_link' , 'back_from_service_status' , 'back_from_user_service_status', 'get_removing_account', 'service_not_inlist']  or call.data.startswith(('serviceshow.' , 'get_new_link')))
def show_services(call):

    Text_0 = 'برای نمایش وضعیت سرویس بر روی آن کلیک کنید'
    if BLOCK_OR_UNBLOCK(UserId= call.from_user.id) is False :

        if FORCE_JOIN_CHANNEL(UserId=call.from_user.id , Bot=bot)==True:

            if call.data=='service_status':
                bot.edit_message_text(Text_0 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.show_service_status(call.from_user.id))
        else :
            bot.send_message(call.message.chat.id , text=force_channel_join_msg, reply_markup=BotKb.load_channels(bot , call.from_user.id))
    else :
        bot.send_message(call.message.chat.id , text='⚠️شما در ربات مسدود شده اید\n و امکان استفاده از ربات را ندارید ')




    if call.data.startswith('serviceshow.'):
        call_data = call.data.split('.')
        user_config_name =  call_data[-1].removeprefix("(").removesuffix(")")
        subscriptions_ = subscriptions.objects.get(user_subscription = user_config_name )
        request = panelsapi.marzban(int(subscriptions_.panel_id.pk)).get_user(user_config_name)
        expire_date = jdatetime.datetime.fromtimestamp(request["expire"])

        created_at_raw = request['created_at'] if request['created_at'] is not None else 'empty'
        if created_at_raw != 'empty':
            dt = datetime.datetime.strptime(created_at_raw.split('.')[0], '%Y-%m-%dT%H:%M:%S')
            created_at = jdatetime.datetime.fromgregorian(datetime=dt)

        Text_1 = f"""
👀 وضعیت فعلی سرویس شما

── نام اشتراک :‌ {subscriptions_.user_subscription}
──جزییات بسته 
  ──  💬نام بسته :‌ {subscriptions_.product_id.product_name if subscriptions_.product_id is not None else '⚠️اطلاعاتی موجود نیست ⚠️'}
  ──  📅مدت زمان : {subscriptions_.product_id.expire_date if subscriptions_.product_id is not None else '⚠️اطلاعاتی موجود نیست ⚠️' } روز 
  ──  💰قیمت محصول : {subscriptions_.product_id.pro_cost if subscriptions_.product_id is not None else '⚠️اطلاعاتی موجود نیست ⚠️'} تومان

──تاریخ انقضا :
    {str(expire_date)}
── تاریخ ساخت اکانت : 
    {str(created_at)}

برای حذف کردن اشتراک از لیست خود :  /rm_mysub_{subscriptions_.pk}
.
""" 
        RM_MYSUB[call.from_user.id] = {'user_sub': subscriptions_.pk , 'rm_sub' : True }
        marzban_panel_api_user[call.from_user.id] = request
        bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.user_service_status(call_data[1] , request))


    if call.data == 'get_config_link':
        if call.from_user.id in marzban_panel_api_user:
            user_sub_link =marzban_panel_api_user[call.from_user.id]['subscription_url']
            Text_2 = f"""
 ─🧷نوع لینک : لینک هوشمند 
 این لینک به صورت هوشمند میباشد و حاوی کانفیگ های اشتراک شما به همراه دیگر جزییات میباشد

    <code>{user_sub_link}</code>
"""
            bot.send_message(call.message.chat.id , Text_2)
        else:
            bot.answer_callback_query(call.id , 'نمیتوانید از این پیام استفاده کنید')
            bot.send_message(call.message.chat.id , Text_0 , reply_markup=BotKb.show_service_status(call.from_user.id))            






    if call.data == 'get_qrcode_link':
        if call.from_user.id in marzban_panel_api_user:
            Text_4 =marzban_panel_api_user[call.from_user.id]['subscription_url']
            qr = QRcode_maker.make_qrcode(Text_4)
            bot.send_photo(call.message.chat.id , qr , caption='─🧷نوع تصویر : حاوی لینک هوشمند \nاین تصویر حاوی اطلاعات حساب شما به صورت هوشمند میباشد')
        else:
            bot.answer_callback_query(call.id , 'نمیتوانید از این پیام استفاده کنید')
            bot.send_message(call.message.chat.id , Text_0 , reply_markup=BotKb.show_service_status(call.from_user.id))            
            





    if call.data.startswith('get_new_link'):
        if call.from_user.id in marzban_panel_api_user:
            user_name = marzban_panel_api_user[call.from_user.id]['username']
            subscriptions_ = subscriptions.objects.get(user_subscription = user_name)
            req = panelsapi.marzban(subscriptions_.panel_id.pk).revoke_sub(user_name)
            marzban_panel_api_user[call.from_user.id] = req
            bot.send_message(call.message.chat.id , req['subscription_url'])
        else :
            bot.answer_callback_query(call.id , 'نمیتوانید از این پیام استفاده کنید')
            bot.send_message(call.message.chat.id , Text_0 , reply_markup=BotKb.show_service_status(call.from_user.id))            



    if call.data.startswith('get_removing_account'):
        if call.from_user.id in marzban_panel_api_user:
            bot.answer_callback_query(call.id ,'درحال حذف اشتراک شما ....' , cache_time=3)
            time.sleep(1.5)
            try:
                user_subscription = marzban_panel_api_user[call.from_user.id]['username']
            
                remove_subscription = subscriptions.objects.get(user_subscription =user_subscription )

                remove_from_panel = panelsapi.marzban(remove_subscription.panel_id.pk).remove_user(user_subscription)
                time.sleep(1)
                remove_subscription.delete()
            except Exception as any_error:
               print(f'get_error when removing user from panel or db \n error_msg : {any_error}')

            clear_dict(marzban_panel_api_user , call.from_user.id)
            bot.edit_message_text(Text_0 , call.from_user.id , call.message.message_id  , reply_markup=BotKb.show_service_status(call.from_user.id))
        else :
            bot.answer_callback_query(call.id , 'نمیتوانید از این پیام استفاده کنید')
            bot.send_message(call.message.chat.id , Text_0 , reply_markup=BotKb.show_service_status(call.from_user.id))            



    if call.data =='service_not_inlist':
        Text_5=f"""
🚦برای اضافه کردن اشتراک خود در ربات یا دسترسی به اشتراک خود به دو طریق میتوانید عمل کنید

  ── 1️⃣ ارسال لینک هوشمند اشتراک 
    - در این روش دقت کنید که لینک کانفیگ را ارسال نکنید و تنها لینک هوشمندی که ابتدای آن دارای (https / http) هست را ارسال کنید

  ── 2️⃣ ارسال نام دقیق اشتراک 
    - در این روش نام اشتراک خود را ارسال نمایید . این نام همان نامی است که در هنگام خرید اشتراک وارد نمودید 

TO CANCEL : /cancel
.
"""
        USER_QUERY_SERVICE[call.from_user.id] = {'query':True}

        if call.from_user.id in USER_STATE and USER_STATE[call.from_user.id][0] in ('buying_new_service' , 'charge_wallet'):
            clear_dict(USERS_BASKET , call.from_user.id)
            clear_dict(CHARGE_WALLET , call.from_user.id)

        USER_STATE[call.from_user.id] = ['find_user_service' , time.time()]

        bot.edit_message_text(Text_5, call.message.chat.id , call.message.message_id)



    if call.data =='back_from_service_status':
        bot.edit_message_text(welcome_msg , call.message.chat.id , call.message.message_id , reply_markup=BotKb.main_menu_in_user_side(call.from_user.id))

    if call.data =='back_from_user_service_status':
        clear_dict(marzban_panel_api_user , call.from_user.id)
        clear_dict(RM_MYSUB , call.from_user.id)
        bot.edit_message_text(Text_0 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.show_service_status(call.from_user.id))





@bot.message_handler(func=lambda message: (len(RM_MYSUB) >= 1 and message.from_user.id in RM_MYSUB and RM_MYSUB[message.from_user.id]['rm_sub'] == True))
def rm_mysub(message):
    if message.from_user.id in RM_MYSUB and RM_MYSUB[message.from_user.id]['rm_sub']==True:
        if message.text.startswith('/rm_mysub_'):
            sub_id = message.text.split('_')
            try :
                subscription_ = subscriptions.objects.get(id = sub_id[-1])
                if subscription_.user_id.user_id == message.from_user.id :
                    subscription_.delete()
                Text_0 = f'برای نمایش وضعیت سرویس بر روی آن کلیک کنید \n'
                bot.send_message(message.chat.id , Text_0 , reply_markup=BotKb.show_service_status(message.from_user.id))
                clear_dict(RM_MYSUB , message.from_user.id)
                clear_dict(marzban_panel_api_user , message.from_user.id)
            except Exception as error_mysub:
                print(f'Error when removing user sub; {error_mysub}')
        else:
            pass




@bot.message_handler(func=lambda message: (len(USER_QUERY_SERVICE) >= 1 and message.from_user.id in USER_QUERY_SERVICE and USER_QUERY_SERVICE[message.from_user.id]['query'] == True))
def query_for_user_service(message):
    if message.from_user.id in USER_QUERY_SERVICE and USER_QUERY_SERVICE[message.from_user.id]['query'] == True:

        if message.text == '/cancel' or message.text =='/cancel'.upper():
            clear_dict(USER_QUERY_SERVICE , message.from_user.id)
            Text_cancel = f'برای نمایش وضعیت سرویس بر روی آن کلیک کنید \n'
            bot.send_message(message.chat.id , Text_cancel, reply_markup=BotKb.show_service_status(message.from_user.id))
        else:
            
            msg = message.text
            patt = r'^https?:\/\/[\d\w\.\-\_\/]+'
            if re.search(patt, msg) is not None:
                try:
                    sub_token = msg.split('/')[-1]
                    panels_ = [i.id for i in v2panel.objects.all()]
                    for i in panels_:
                        try:
                            req = panelsapi.marzban(panel_id=int(i)).get_info_by_token(sub_token)
                            if req:
                                username = req["username"]
                                try:
                                    subscription_user = subscriptions.objects.get(user_subscription=str(username))
                                    if subscription_user.user_id != message.from_user.id:
                                        bot.send_message(message.chat.id, '⚠️این اشتراک متلعق به شما نیست⚠️')
                                    else :
                                        bot.send_message(message.chat.id , '⚠️این اشتراک در لیست اشتراکهای شما قرار دارد⚠️')  

                                except subscriptions.DoesNotExist:
                                    panel_id = v2panel.objects.get(id=int(i))
                                    user_ = users.objects.get(user_id=message.from_user.id)
                                    subscription_ = subscriptions.objects.create(user_subscription=username, panel_id=panel_id, user_id=user_)
                                    Text_0 = f'برای نمایش وضعیت سرویس بر روی آن کلیک کنید \n ✅اشتراک شما بانام {username} با موفقیت اضافه شد'
                                    bot.send_message(message.chat.id, Text_0, reply_markup=BotKb.show_service_status(message.from_user.id))

                                break
                            else:
                                bot.send_message(message.chat.id, 'اشتراکی با این توکن وجود ندارد')
                                
                        except Exception as api_error:
                            print(f"API error for panel {i}: {api_error}") 
                                
                except Exception as eror_by_token:  
                    bot.send_message(message.chat.id, 'همچین لینکی در سیستم وجود ندارد')
                clear_dict(USER_QUERY_SERVICE , message.from_user.id)

            else:
                try:
                    panels_ = [i.id for i in v2panel.objects.all()]
                    for i in panels_:
                        req = panelsapi.marzban(panel_id=int(i)).get_user(username=str(message.text))
                        if req:
                            username = req['username']
                            try:
                                subscription_find = subscriptions.objects.get(user_subscription=str(username))
                                if subscription_find.user_id != message.from_user.id:
                                    bot.send_message(message.chat.id, '⚠️این اشتراک متلعق به شما نیست⚠️')
                                else:
                                    bot.send_message(message.chat.id, '⚠️این اشتراک در لیست اشتراک‌های شما قرار دارد⚠️')
                            except subscriptions.DoesNotExist:
                                panel_id = v2panel.objects.get(id=int(i))
                                user_ = users.objects.get(user_id=message.from_user.id)
                                subscription_ = subscriptions.objects.create(user_subscription=username, panel_id=panel_id, user_id=user_)
                                Text_0 = f'برای نمایش وضعیت سرویس بر روی آن کلیک کنید \n ✅اشتراک شما با نام {username} با موفقیت اضافه شد'
                                bot.send_message(message.chat.id, Text_0, reply_markup=BotKb.show_service_status(message.from_user.id))
                                clear_dict(USER_QUERY_SERVICE, message.from_user.id)
                            break
                    else:
                        bot.send_message(message.chat.id, 'همچین نامی وجود ندارد')
                    clear_dict(USER_QUERY_SERVICE, message.from_user.id)
                except Exception as eror_by_token:
                    bot.send_message(message.chat.id, 'همچین نامی در سیستم وجود ندارد')
                    clear_dict(USER_QUERY_SERVICE, message.from_user.id)






# - 3 user-side
# --------------------------------------------------------------------------------------------------------------------------
# ------------------------- RENEW-SERVICE ----------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------


TAMDID_PANEL_LOADING = {'panel_pk' : int , 'one_panel' : False , 'two_panel' : False}


def tamdid_payment_decline_reason_create():
    tamdid_payment_decline_reason = {'tamdid_reason' : False  , 'tamdid_user_id' : int , 'payment_ob':None}
    return tamdid_payment_decline_reason


TAMDID_payment_decline_reason={}
TAMDID_BASKETS_USER  = {}
TAMDID_FISH = {}


@bot.callback_query_handler(func= lambda call : call.data in ['tamdid_service', 'tamdid_pay_with_wallet', 'tamdid_pay_with_card',   'verify_product_for_tamdid', 'back_from_user_tamdid_service', 'tamdid_back_two_panel', 'back_from_verfying_tamdid', 'back_from_payment_tamdid'] or call.data.startswith(('Tamidi:' , 'tamdid_panelid-' , 'newingtamdid_')))
def tamdid_service(call):

    if BLOCK_OR_UNBLOCK(UserId= call.from_user.id) is False :

        if FORCE_JOIN_CHANNEL(UserId=call.from_user.id , Bot=bot)==True:

            if call.data == 'tamdid_service':
                user_sub = BotKb.show_user_subsctription(call.from_user.id)
                Text_1= ' ✢ برای تمدید سرویس اشتراکی را که میخواهید انتخاب نمایید '
                if user_sub =='no_sub_user_have':
                    bot.answer_callback_query(call.id , 'شما هیچ سرویسی برای تمدید ندارید')
                else:
                    bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.show_user_subsctription(call.from_user.id))
        else :
            bot.send_message(call.message.chat.id , text=force_channel_join_msg, reply_markup=BotKb.load_channels(bot , call.from_user.id))
    else :
        bot.send_message(call.message.chat.id , text='⚠️شما در ربات مسدود شده اید\n و امکان استفاده از ربات را ندارید ')



    if call.data.startswith('Tamidi:'):
        panels_ = v2panel.objects.all()
        if panels_.count() <= 1: 
            if plans_loading_for_one_panel() == 'panel_disable' :
                bot.send_message(call.message.chat.id , '⌛️پنل در حال بروزرسانی میباشد . لطفا بعدا مراجعه فرمایید')
            else : 
                if isinstance(plans_loading_for_one_panel() , InlineKeyboardMarkup):
                    bot.edit_message_text(buy_service_section_product_msg , call.message.chat.id , call.message.message_id , reply_markup = plans_loading_for_one_panel(tamdid=True))      
                    
                    #panel_id = v2panel.objects.all()[0].id
                    panel_id = panels_[0].id
                    TAMDID_PANEL_LOADING['one_panel'] = True
                    TAMDID_PANEL_LOADING['panel_pk'] = panel_id
                
                    if call.from_user.id not in TAMDID_BASKETS_USER:
                            TAMDID_BASKETS_USER[call.from_user.id] = create_product_entry(tamdid=True)
                    TAMDID_BASKETS_USER[call.from_user.id]['panel_number']= panel_id
                    TAMDID_BASKETS_USER[call.from_user.id]['config_name'] = call.data.split(':')[1]

                    
                    
            if plans_loading_for_one_panel() == 'sale_closed' :
                bot.send_message(call.message.chat.id , '⛔️فروش سرویس بسته میباشد ، بعدا مراجعه فرمایید')

            if plans_loading_for_one_panel() == 'sale_open_no_zarfit' :
                bot.send_message(call.message.chat.id , '🪫ظرفیت فروش به اتمام رسیده است . بعدا مراجعه فرمایید')

            if plans_loading_for_one_panel() == 'no_panel_product' : 
                bot.send_message(call.message.chat.id , '‼️متاسفیم ، هنوز هیچ سرور یا محصولی برای ارائه وجود ندارد' )
    

        else :
            subscriptions_name= call.data.split(':')[1]
            keyboard = InlineKeyboardMarkup()
            for i in panels_ :
                button = InlineKeyboardButton(text=i.panel_name , callback_data=f'tamdid_panelid-{str(i.id)}-{subscriptions_name}')
                keyboard.add(button)
            button_back_2more = InlineKeyboardButton(text='✤ - بازگشت به منوی قبلی - ✤', callback_data='tamdid_back_two_panel')
            keyboard.add(button_back_2more)
            bot.edit_message_text(buy_service_section_choosing_panel_msg , call.message.chat.id , call.message.message_id , reply_markup=keyboard)


    if call.data.startswith('tamdid_panelid-') :
        call_data = call.data.split('-')
        state_panel = plans_loading_for_two_more_panel(panel_pk= int(call_data[1]))
        if state_panel == 'panel_disable':
                bot.send_message(call.message.chat.id , '⌛️پنل در حال بروزرسانی میباشد . لطفا بعدا مراجعه فرمایید')
        else :
            if isinstance(state_panel , InlineKeyboardMarkup) :
                bot.edit_message_text(buy_service_section_product_msg , call.message.chat.id , call.message.message_id , reply_markup = plans_loading_for_two_more_panel(panel_pk= int(call_data[1]) , tamdid=True))

                TAMDID_PANEL_LOADING['two_panel'] = True
                TAMDID_PANEL_LOADING['panel_pk'] = int(call_data[1])

                if call.from_user.id not in TAMDID_BASKETS_USER:
                    TAMDID_BASKETS_USER[call.from_user.id] = create_product_entry(tamdid=True)

                TAMDID_BASKETS_USER[call.from_user.id]['panel_number'] = int(call_data[1])
                TAMDID_BASKETS_USER[call.from_user.id]['config_name'] = str(call_data[2])
                    

        if state_panel == 'sale_closed':
            bot.send_message(call.message.chat.id , '⛔️فروش سرویس بسته میباشد ، بعدا مراجعه فرمایید')

        if  state_panel == 'sale_open_no_capcity':
            bot.send_message(call.message.chat.id , '🪫ظرفیت فروش به اتمام رسیده است . بعدا مراجعه فرمایید')

        if state_panel == 'no_products':
            bot.send_message(call.message.chat.id , '‼️متاسفیم ، هنوز هیچ سرور یا محصولی برای ارائه وجود ندارد')






    if call.data.startswith('newingtamdid_'):
            call_data = call.data.split("_")
            product_ = products.objects.get(id = int(call_data[1]))
            TAMDID_BASKETS_USER[call.from_user.id]['product_id'] = int(call_data[1])
            TAMDID_BASKETS_USER[call.from_user.id]['product_name'] = product_.product_name
            TAMDID_BASKETS_USER[call.from_user.id]['data_limit'] = product_.data_limit
            TAMDID_BASKETS_USER[call.from_user.id]['expire_date'] = product_.expire_date
            TAMDID_BASKETS_USER[call.from_user.id]['pro_cost'] = product_.pro_cost
            TAMDID_BASKETS_USER[call.from_user.id]['statement'] = [call_data[2] , call_data[3]]



            keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('✅ تایید محصول ', callback_data='verify_product_for_tamdid') , InlineKeyboardButton('✤ - بازگشت به منوی قبلی - ✤' , callback_data='back_from_verfying_tamdid') , row_width = 1 )
            bot.edit_message_text(product_info_msg(TAMDID_BASKETS_USER[call.from_user.id] , tamdid=True) , call.message.chat.id , call.message.message_id ,  reply_markup=keyboard)







    if call.data =='verify_product_for_tamdid':
        Text_2 ='⚪️ یک روش پرداخت را انتخاب نمایید'
        bot.edit_message_text(Text_2 , call.message.chat.id , call.message.message_id , reply_markup=botkb.payby_in_user_side(tamdid=True))



    if call.data =='tamdid_pay_with_wallet':
        req = tamdid_pay_with_wallet(call , bot , TAMDID_BASKETS_USER , TAMDID_PANEL_LOADING)
        if req != ('requset_false' or 'insufficent' or None):
            if isinstance(req , dict):
                bot.edit_message_text(paied_msg , call.message.chat.id , call.message.message_id)
                bot.send_chat_action(chat_id=call.message.chat.id, action='typing')
                time.sleep(2.5)
                how_to_send(req, int(TAMDID_BASKETS_USER[call.from_user.id]['panel_number']) , bot , call.from_user.id)
                clear_dict(TAMDID_BASKETS_USER , call.from_user.id)
        else :
            print(f'requset is failed related to the api')





    if call.data =='tamdid_pay_with_card':
        tamdid_pay_with_card(call , bot , TAMDID_BASKETS_USER , TAMDID_FISH)



    #back - buttons
    if call.data in ['back_from_user_tamdid_service', 'tamdid_back_two_panel']:
        clear_dict(TAMDID_BASKETS_USER , call.from_user.id)
        bot.edit_message_text(welcome_msg , call.message.chat.id , call.message.message_id , reply_markup=BotKb.main_menu_in_user_side(call.from_user.id))        

    #back - buttons
    if call.data in ['back_from_verfying_tamdid' , 'back_from_payment_tamdid']:
        clear_dict(TAMDID_BASKETS_USER , call.from_user.id)
        bot.answer_callback_query(call.id , 'ادامه تمدید محصول لغو گردید')
        bot.edit_message_text(welcome_msg , call.message.chat.id , call.message.message_id , reply_markup=BotKb.main_menu_in_user_side(call.from_user.id))        







@bot.message_handler(func = lambda message : (message.from_user.id in TAMDID_FISH and len(TAMDID_FISH) > 0  and TAMDID_FISH[message.from_user.id]['tamdid_fish_send'] == True) , content_types=['text' , 'photo'])
def getting_fish_image(message):

    users_ = users.objects.get(user_id = message.from_user.id)
    admins_ = admins.objects.all()
    if message.from_user.id in TAMDID_FISH and len(TAMDID_FISH) > 0  and TAMDID_FISH[message.from_user.id]['tamdid_fish_send']==True:
        if message.content_type  == 'text'  and message.text == '/cancel' or message.text == '/cancel'.upper():
            inovieces_ = inovices.objects.get(id = TAMDID_FISH[message.from_user.id]['inovices'].id)
            inovieces_.paid_status = 0 
            inovieces_.save()
            clear_dict(TAMDID_BASKETS_USER , message.from_user.id)
            clear_dict(TAMDID_FISH , message.from_user.id)
            bot.send_message(message.chat.id , welcome_msg , reply_markup= botkb.main_menu_in_user_side(message.from_user.id))

        else:

            if check_time_passed(TAMDID_FISH[message.from_user.id]['inovices'].id) == 'time_passed':
                update_inovice_status = inovices.objects.get(id = TAMDID_FISH[message.from_user.id]['inovices'].id)
                update_inovice_status.paid_status = 0 # paid_status = 0 / unpaid due to passing time
                update_inovice_status.save()
                bot.send_message(message.chat.id , inovice_time_passed_msg)
            else :
                panel_id = TAMDID_PANEL_LOADING['panel_pk'] if TAMDID_PANEL_LOADING['one_panel'] == True else TAMDID_PANEL_LOADING['panel_pk']
                panel_name = v2panel.objects.get(id = panel_id).panel_name
                if message.content_type == 'photo':
                    for i in admins_:
                            bot.send_photo(i.user_id , message.photo[-1].file_id , caption = send_user_buy_request_to_admins(TAMDID_BASKETS_USER[message.from_user.id] ,users_ , panel_name , tamdid=True ) , reply_markup= BotKb.agree_or_disagree(message.from_user.id , tamdid=True))
                    bot.send_message(message.chat.id ,send_success_msg_to_user)
                    
                TAMDID_FISH[message.from_user.id]['tamdid_fish_send'] = False
                TAMDID_FISH[message.from_user.id]['tamdid_accpet_or_reject'] = True





@bot.callback_query_handler(func = lambda call : call.data.startswith('tamdid_agree_') or call.data.startswith('tamdid_disagree_') )
def agree_or_disagree_kbk_payment(call):

    call_data = call.data.split('_')
    user_basket = TAMDID_BASKETS_USER[int(call_data[-1])]

    if call.data.startswith('tamdid_agree_')  and (int(call_data[-1]) in TAMDID_FISH and len(TAMDID_FISH) >=1 and  TAMDID_FISH[int(call_data[-1])]['tamdid_accpet_or_reject']) == True:

        inovices_1 = inovices.objects.get(id= TAMDID_FISH[int(call_data[-1])]['inovices'].id)
        inovices_1.paid_status = 1 # accpeted
        inovices_1.save()
        users_ = users.objects.get(user_id = int(call_data[-1]))
        payments_ = payments.objects.create(user_id = users_ , amount = user_basket['pro_cost']  , payment_status = 'accepted' , inovice_id = inovices_1)

        if NUMBER_OF_PANEL_LOADED['one_panel'] == True  or NUMBER_OF_PANEL_LOADED['two_panels'] == True:
            if ('open' and 'zarfit') in user_basket['statement'] :
                PANEL_managing.check_capcity(NUMBER_OF_PANEL_LOADED['panel_pk'])
                        
        bot.reply_to(call.message , f'درخواست پرداخت یوزر : {str(call_data[-1])} انجام شد')

        bot.send_message(int(call_data[-1]) , paied_msg)
        try :
            send_request = panelsapi.marzban(user_basket['panel_number']).put_user(user_basket['config_name'] , user_basket['product_id'])
        except Exception as request_error:
            print(f'error while sending reques {request_error}')

        bot.send_chat_action(int(call_data[-1]), action='typing')
        time.sleep(3)
        how_to_send(send_request , user_basket['panel_number'] , bot , int(call_data[-1]))

        clear_dict(TAMDID_BASKETS_USER , int(call_data[-1]))
        clear_dict(TAMDID_FISH , int(call_data[-1]))



    if call.data.startswith('tamdid_disagree_')  and (int(call_data[-1]) in TAMDID_FISH and len(TAMDID_FISH) >=1 and  TAMDID_FISH[int(call_data[-1])]['tamdid_accpet_or_reject']) == True:
        users_ = users.objects.get(user_id = call_data[-1])
        inovices_2 = inovices.objects.get(id = TAMDID_FISH[int(call_data[-1])]['inovices'].id)
        inovices_2.paid_status = 3 # rejected
        inovices_2.save()
        payments_ = payments.objects.create(user_id = users_ , amount = user_basket['pro_cost'] ,payment_status = 'declined' , inovice_id = inovices_2)
        
        bot.send_message(call.message.chat.id , 'علت رد پرداخت را ارسال کنید')
        
        if int(call_data[-1])  not in TAMDID_payment_decline_reason :
            TAMDID_payment_decline_reason[int(call_data[-1])] = payment_decline_reason_create()

        TAMDID_payment_decline_reason[int(call_data[-1])]['tamdid_reason'] = True
        TAMDID_payment_decline_reason[int(call_data[-1])]['tamdid_user_id'] = int(call_data[-1])
        TAMDID_payment_decline_reason[int(call_data[-1])]['payment_ob'] = payments_
        TAMDID_FISH[int(call_data[-1])]['tamdid_accpet_or_reject'] = False





# ./buy services > disagree of fish : getting reason
@bot.message_handler(func= lambda message :  len(TAMDID_payment_decline_reason) ==1 )
def get_decline_reason(message):
    
    user_id = str
    for i in TAMDID_payment_decline_reason.keys():
        user_id =  i

    if TAMDID_payment_decline_reason[user_id]['tamdid_reason'] == True : 
        payments_ = payments.objects.get(id = TAMDID_payment_decline_reason[int(user_id)]['payment_ob'].id)
        payments_.decline_reason = message.text
        payments_.save()
        user_reject_reason = f"""
🔴درخواست شما رد شد 
       ┘ 🔻 علت : ‌ {message.text}
.
       """
        admin_reject_reason= f"""
درخواست پرداخت رد شد ❌
     ¦─  یوزر درخواست کننده: ‌{user_id}
     ¦─  علت رد درخواست : ‌{message.text}
     ¦─  شماره فاکتور :‌ {payments_.inovice_id.pk}
     ¦─  شماره پرداخت :‌  {payments_.id}
     
.
     """
        bot.send_message(user_id , user_reject_reason)
        bot.send_message(message.chat.id ,admin_reject_reason)

        clear_dict(TAMDID_BASKETS_USER , message.from_user.id)
        clear_dict(TAMDID_FISH , message.from_user.id)
        clear_dict(TAMDID_payment_decline_reason , user_id)
















# - 4 user-side
# --------------------------------------------------------------------------------------------------------------------------
# ------------------------- WALLET-PROFILE ---------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------


TRANSFER_MONEY_USRTOUSR  = {}
CHARGE_WALLET = {}


def transfer_money_usrtousr_dict():
    transfer_money_usrtousr_dict = {'transfer_money_to_user':False, 'get_amount':False , 'userid_to_transfer':int}
    return transfer_money_usrtousr_dict


def charge_wallet_dict():
    charge_wallet_dict = {'charge_wallet':False ,'get_amount':False , 'send_fish':False  , 'reason':False , 'user_id':int ,'amount':int, 'payment_ob':None}
    return charge_wallet_dict



# ./wallet-profile
@bot.callback_query_handler(func = lambda call : call.data in ['wallet_profile', 'back_from_wallet_profile', 'user_id','username', 'tranfert_money_from_wallet' ,'charge_wallet']) 
def wallet_profile(call):

    if BLOCK_OR_UNBLOCK(UserId= call.from_user.id) is False :

        if FORCE_JOIN_CHANNEL(UserId=call.from_user.id , Bot=bot)==True:

            if call.data=='wallet_profile':
                Text_1 ='✤ - پروفایل من : '
                bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup= BotKb.wallet_profile(call.from_user.id))
        else :
            bot.send_message(call.message.chat.id , text=force_channel_join_msg, reply_markup=BotKb.load_channels(bot , call.from_user.id))
    else :
        bot.send_message(call.message.chat.id , text='⚠️شما در ربات مسدود شده اید\n و امکان استفاده از ربات را ندارید ')




    if call.data=='user_id':
        info_list_def = BotKb.wallet_profile(call.from_user.id , True)
        Text_2 = f""" 
✤ - پروفایل من :
   ┘ - آیدی عددی :‌ <code>{info_list_def[0]}</code> 
."""
        bot.edit_message_text(Text_2 , call.message.chat.id , call.message.message_id ,parse_mode="HTML" ,reply_markup= BotKb.wallet_profile(call.from_user.id))



    if call.data =='username':
        info_list_def = BotKb.wallet_profile(call.from_user.id , True)
        Text_3 = f""" 
✤ - پروفایل من :
   ┘ - یوزرنیم : @{info_list_def[1]}
."""
        bot.edit_message_text(Text_3 , call.message.chat.id , call.message.message_id ,parse_mode="HTML" ,reply_markup= BotKb.wallet_profile(call.from_user.id))
        


    if call.data=='tranfert_money_from_wallet':
        clear_dict(TRANSFER_MONEY_USRTOUSR , call.message.chat.id )
        TRANSFER_MONEY_USRTOUSR[call.from_user.id] = transfer_money_usrtousr_dict()
        TRANSFER_MONEY_USRTOUSR[call.from_user.id]['transfer_money_to_user'] = True
        bot.send_message(call.message.chat.id , '🔻 لطفا ایدی عددی کاربر مقصد را وارد نمایید  \n\n برای کنسل کردن انتقال  : /CANCEL')




    if call.data == 'charge_wallet':
        clear_dict(CHARGE_WALLET , call.from_user.id)
        CHARGE_WALLET[call.from_user.id] = charge_wallet_dict()
        CHARGE_WALLET[call.from_user.id]['charge_wallet'] = True

        if call.from_user.id in USER_STATE and USER_STATE[call.from_user.id] in ('buying_new_service' , 'find_user_service'):
            clear_dict(USERS_BASKET , call.from_user.id)
            clear_dict(USER_QUERY_SERVICE , call.from_user.id)

        USER_STATE[call.from_user.id] = ['charge_wallet' , time.time()]


        bot.send_message(call.message.chat.id ,'💰مبلغ مورد نظر را به تومان برای شارژ کیف پول خود را وارد نمایید \n\n برای کنسل کردن انتقال  : /CANCEL')



    #back-button
    if call.data=='back_from_wallet_profile':
        bot.edit_message_text(welcome_msg , call.message.chat.id , call.message.message_id , reply_markup= BotKb.main_menu_in_user_side(call.from_user.id))





# ./wallet-profile > charge - wallet
@bot.message_handler(func= lambda message: message.text =='/add_money'  or( message.from_user.id in CHARGE_WALLET and len(CHARGE_WALLET) >=1  and CHARGE_WALLET[message.from_user.id]['charge_wallet'] == True) or (message.from_user.id in CHARGE_WALLET and len(CHARGE_WALLET) >=1 and CHARGE_WALLET[message.from_user.id]['send_fish'] == True) , content_types=['text','photo'])
def charge_wallet_profilewallet(message):

    if message.text == '/add_money' and message.content_type =='text':
        clear_dict(CHARGE_WALLET , message.from_user.id)
        CHARGE_WALLET[message.from_user.id] = charge_wallet_dict()
        CHARGE_WALLET[message.from_user.id]['charge_wallet'] = True
        bot.send_message(message.chat.id ,'💰مبلغ مورد نظر را به تومان برای شارژ کیف پول خود را وارد نمایید \n\n برای کنسل کردن انتقال  : /CANCEL')
        return

    if CHARGE_WALLET[message.from_user.id]['charge_wallet'] == True:
        if message.text =='/cancel' or message.text =='/cancel'.upper():
            clear_dict(CHARGE_WALLET,message.from_user.id)
            Text_1 ='✤ - پروفایل من : '
            bot.send_message(message.chat.id, Text_1 , reply_markup=BotKb.wallet_profile(message.chat.id))

        else:
            if message.text.isdigit(): 
                load_shomarekart = buy_service_section_card_to_card_msg(int(message.text))
                if load_shomarekart == 'هیچ شماره کارت فعالی وجود نداره':
                    bot.send_message(message.chat.id , 'هیچ شماره کارت فعالی وجود ندارد')
                    clear_dict(CHARGE_WALLET , message.from_user.id)
                else:
                    bot.send_message(message.chat.id , load_shomarekart)
                    users_ = users.objects.get(user_id = message.chat.id )
                    payments_ = payments.objects.create(user_id = users_ , amount = message.text , payment_status = 'waiting' )
                    CHARGE_WALLET[message.from_user.id]['charge_wallet'] = False
                    CHARGE_WALLET[message.from_user.id]['send_fish'] = True
                    CHARGE_WALLET[message.from_user.id]['amount']= message.text
                    CHARGE_WALLET[message.from_user.id]['payment_ob'] = payments_
            else:
                bot.send_message(message.chat.id , 'لطفا مقدار عددی  وارد کنید \n\n برای لغو کردن انتقال :  /CANCEL')
        return
    


    if CHARGE_WALLET[message.from_user.id]['send_fish'] == True :
        if message.text =='/cancel' or message.text =='/cancel'.upper():
            clear_dict(CHARGE_WALLET,message.from_user.id)
            Text_1 ='✤ - پروفایل من : '
            bot.send_message(message.chat.id, Text_1 , reply_markup=BotKb.wallet_profile(message.chat.id))

        else:
            if message.content_type == 'photo':
                user_ = users.objects.get(user_id = message.from_user.id)
                Text_2 = f'درخواست شارژ کیف پول شما برای ادمین ارسال شد '
                amount = CHARGE_WALLET[message.from_user.id]['amount']
                charge_wallet_txt = f'''
【✣ درخواست شارژ کیف پول در سیستم ثبت شده است ✣】
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

┊──👤: ایدی عددی : {message.from_user.id}
┊──🆔 یوزرنیم تلگرام :‌ @‌{message.from_user.username}
┊──💰موجودی کیف پول :‌ {format(user_.user_wallet, ",")} تومان
┊── 💸مبلغ شارژ : {format(int(amount),',')} تومان

    ¦─ در صورت تایید گزینه تایید پرداخت ✅ را بزنید در غیر این صورت رد پرداخت ❌  را بزنید
'''
                CHARGE_WALLET[message.from_user.id]['send_fish'] = False
                CHARGE_WALLET[message.from_user.id]['user_id'] = message.from_user.id
                bot.send_message(message.chat.id , Text_2)
                bot.send_photo((i.user_id for i in admins.objects.all()) , message.photo[-1].file_id, caption=charge_wallet_txt , reply_markup=BotKb.wallet_accepts_or_decline(message.chat.id))
            else:
                bot.send_message(message.chat.id , 'مورد ارسالی باید به صورت تصویر باشد\n مجدد امتحان فرمایید\n /add_money')
                clear_dict(CHARGE_WALLET , message.from_user.id)
        return
        





payments_decline = {'reason' : False  , 'userid':int}
# ./wallet-profile > charge - wallet : accpeting fish
@bot.callback_query_handler(func= lambda call : call.data.startswith('wallet_accepts_') or call.data.startswith('wallet_decline_'))
def accepts_decline(call):
    userId = call.data.split('_')

    if call.data.startswith('wallet_accepts_'):
        if int(userId[-1]) in CHARGE_WALLET:
            payments_ = CHARGE_WALLET[int(userId[-1])]['payment_ob']
            payments_.payment_status = 'accepted'
            payments_.save()

            users_ = users.objects.get(user_id = userId[-1])
            users_.user_wallet = users_.user_wallet + int(payments_.amount)
            users_.save()
            keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('مشاهده کیف پول' , callback_data='wallet_profile'))
        
            bot.send_message(call.message.chat.id , 'درخواست شارژ کیف پول قبول شد')
            bot.send_message(userId[-1] ,  '✅درخواست شارژ کیف پول شما با موفقیت انجام شد 👇🏻' , reply_markup=keyboard)
            clear_dict(CHARGE_WALLET , int(userId[-1]))


    if call.data.startswith('wallet_decline_'):
        if int(userId[-1]) in CHARGE_WALLET:
            CHARGE_WALLET[int(userId[-1])]['reason'] = True
            bot.send_message(call.message.chat.id , 'دلیل رد کردن درخواست را ثبت بفرمایید')





# ./wallet-profile > charge - wallet : getting decline reason
@bot.message_handler(func = lambda message : len(CHARGE_WALLET) == 1)
def get_decline_reason(message):
    if len(CHARGE_WALLET) >=1:
        for i in CHARGE_WALLET.keys():
            user_id = i
        payments_ = CHARGE_WALLET[user_id]['payment_ob']
        payments_.payment_status = 'declined'
        payments_.decline_reason = message.text
        payments_.save()
        user_reject_reason = f"""
🔴درخواست شما رد شد 
       ┘ 🔻 علت : ‌ {message.text}
.
       """
        
        admin_reject_reason= f"""
درخواست شارژ کیف رد شد ❌
     ¦─  یوزر درخواست کننده: ‌{user_id}
     ¦─  علت رد درخواست : ‌{message.text}
     ¦─  شماره فاکتور :‌ {payments_.id}
     ¦─  شماره پرداخت :‌  {payments_.id}
     
.
     """
        bot.send_message(message.chat.id , admin_reject_reason)
        bot.send_message(CHARGE_WALLET[i]['user_id'] , user_reject_reason)
        clear_dict(CHARGE_WALLET ,user_id)





# ./wallet_profile > tranfert_money_from_wallet
@bot.message_handler(func= lambda message : (len(TRANSFER_MONEY_USRTOUSR) >= 1 and TRANSFER_MONEY_USRTOUSR[message.from_user.id]['transfer_money_to_user'] == True) or  (len(TRANSFER_MONEY_USRTOUSR) >= 1 and TRANSFER_MONEY_USRTOUSR[message.from_user.id]['get_amount'] == True))
def tranfert_money_from_wallet(message):

    if  TRANSFER_MONEY_USRTOUSR[message.from_user.id]['transfer_money_to_user'] == True:
        if message.text == '/cancel' or message.text == '/cancel'.upper():
            clear_dict(TRANSFER_MONEY_USRTOUSR , message.from_user.id)
            Text_1 ='✤ - پروفایل من : '
            bot.send_message(message.chat.id , Text_1 , reply_markup=BotKb.wallet_profile(message.from_user.id))
        else:
            if  message.text.isdigit():
                try :
                    user_search = users.objects.filter(user_id = int(message.text))
                    if user_search.exists() :
                        TRANSFER_MONEY_USRTOUSR[message.from_user.id]['transfer_money_to_user'] = False
                        TRANSFER_MONEY_USRTOUSR[message.from_user.id]['get_amount'] = True
                        TRANSFER_MONEY_USRTOUSR[message.from_user.id]['userid_to_transfer'] = message.text
                        bot.send_message(message.chat.id , '💰 مبلغ مورنظر را وارد نمایید \n\n برای کنسل کردن انتقال  : /CANCEL')
                    else :
                        bot.send_message(message.chat.id , '🔎 اکانتی با ایدی عددی ارسال شده وجود ندارد \n\n برای کنسل کردن انتقال  : /CANCEL')
                except users.DoesNotExist as error_users:
                    bot.send_message(message.chat.id , '🔎 اکانتی با ایدی عددی ارسال شده وجود ندارد \n\n برای کنسل کردن انتقال  : /CANCEL')
            else :
                bot.send_message(message.chat.id , '⚠️مقدار وارد شده باید عددی باشد⚠️ ')
        return


    if TRANSFER_MONEY_USRTOUSR[message.chat.id]['get_amount'] == True :
        if message.text == '/cancel' or message.text == '/cancel'.upper():
            clear_dict(TRANSFER_MONEY_USRTOUSR , message.from_user.id)
            Text_2 ='✤ - پروفایل من : '
            bot.send_message(message.chat.id , Text_2 , reply_markup = BotKb.wallet_profile(message.from_user.id))

        else :

            if  not message.text.isdigit():
                bot.send_message(message.chat.id , '⚠️مقدار وارد شده باید عددی باشد⚠️\n\n برای کنسل کردن انتقال  : /CANCEL')
            else :
                try :
                    users_want_to_transfer = users.objects.get(user_id = message.from_user.id)
                    if users_want_to_transfer.user_wallet  == 0:
                        clear_dict(TRANSFER_MONEY_USRTOUSR , message.from_user.id)
                        bot.send_message(message.chat.id , '❌موجودی حساب شما برای انتقال کافی نمیباشد❌')
                    else:
                        users_get_transfer = users.objects.get(user_id = TRANSFER_MONEY_USRTOUSR[message.from_user.id]['userid_to_transfer'])
                        #user gets the money
                        new_wallet = users_get_transfer.user_wallet + int(message.text)
                        users_get_transfer.user_wallet = new_wallet
                        users_get_transfer.save()

                        #user transer the money
                        new_wallet2 = users_want_to_transfer.user_wallet - int(message.text)
                        users_want_to_transfer.user_wallet = new_wallet2
                        users_want_to_transfer.save()
                        amount = format(int(message.text) , ',')
                        Text_who_transfer = f"""
✅مبلغ مورد نظر با موفقیت انتقال یافت 
   - شما مبلغ {amount} به شماره ایدی {TRANSFER_MONEY_USRTOUSR[message.from_user.id]["userid_to_transfer"]} ارسال کردید .
   - موجودی فعلی کیف پول شما : {users_want_to_transfer.user_wallet}
.
"""
                        Text_who_get = f"""
💝 مبلغ {amount} به کیف پول شما منتقل شد
    - این انتقال توسط شخص  دیگری برای شما انجام شده است . 
.
"""                     
                        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('👁مشاهده حساب کاربری ' , callback_data='wallet_profile'))
                        bot.send_message(message.chat.id , Text_who_transfer , reply_markup= keyboard)
                        bot.send_message(TRANSFER_MONEY_USRTOUSR[message.from_user.id]['userid_to_transfer'] , Text_who_get ,reply_markup=keyboard)   
                        clear_dict(TRANSFER_MONEY_USRTOUSR, message.from_user.id)

                except Exception as failed_totransfer_money:
                    clear_dict(TRANSFER_MONEY_USRTOUSR, message.from_user.id)
                    bot.send_message(message.chat.id , '❌انتقال وجه با مشکل مواجه شد❌')
                    print(failed_totransfer_money)
        return













# ---------------------------- MANAGEMENT ----------------------------------------------------------------------------------------


#> ./management
@bot.callback_query_handler(func=lambda call:call.data in ['robot_management' , 'back_from_management'])
def bot_mangement(call) :
    if call.data=='robot_management':
        Text_1='به مدیریت ربات خوش امدید '
        bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.management_menu_in_admin_side(user_id = call.from_user.id))
    
    
    if call.data=='back_from_management':
        
        bot.edit_message_text(welcome_msg , call.message.chat.id ,call.message.message_id , reply_markup=BotKb.main_menu_in_user_side(call.from_user.id))






# ---------------------------------------------------------------------------------------------------------------------------------#
# -------------------------PANEL MANAGEMENT----------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------------------#



#> ./Management > Panels 
@bot.callback_query_handler(func=lambda call:call.data=='panels_management' or call.data=='back_from_panel_manageing' or call.data=='add_panel' or call.data=='remove_panel' or call.data=='manageing_panels')
def handle_panel(call):

    Text_0='هیچ پنلی برای حذف کردن پیدا نشد \n\n برای اضافه کردن اولین پنل به ربات /add_panel رو بزنید'


    if call.data=='panels_management' :
        admins_ = admins.objects.get(user_id = int(call.from_user.id))
        if (admins_.acc_panels == 1 and admins_.acc_panels ==1) or admins_.is_owner ==1:
            Text_1='شما در حال مدیریت کردن بخش پنل ها هستید'
            bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.panel_management_menu_in_admin_side())
        else :
            bot.send_message(call.message.chat.id , 'شما اجازه دسترسی به این قسمت را ندارید')


    if call.data=='back_from_panel_manageing':
        Text_back='به مدیریت ربات خوش امدید '
        bot.edit_message_text(Text_back , call.message.chat.id , call.message.message_id , reply_markup=BotKb.management_menu_in_admin_side(user_id = call.from_user.id))



    #- Adding Panels
    if call.data=='add_panel':
        PANEL_RECEIVING_STATE['Enable_Panel_Adding']=True
        PANEL_RECEIVING_STATE.update({key : False for key in PANEL_RECEIVING_STATE if  key != 'Enable_Panel_Adding'})
        Text_2='یک اسم برای پنل خود انتخاب کنید؟\n⚠️.دقت کنید که این اسم مستقیما در قسمت خرید سرویس ها نمایش داده میشود\n\nمثال ها : \n سرویس هوشمند ، سرور مولتی لوکیشن \n\nTO CANCEL : /CANCEL'
        bot.edit_message_text(Text_2 , call.message.chat.id , call.message.message_id)



    #- Removing Panels
    if call.data=='remove_panel':
        no_panel = BotKb.panel_management_remove_panel()
        Text_3 = '🚦برای حذف کردن پنلی که میخواهید بر روی اون کلیک کنید'
        if no_panel=='no_panel_to_remove':
            bot.send_message(call.message.chat.id , Text_0)
        else :
            bot.edit_message_text(Text_3 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.panel_management_remove_panel())



    #- Manging Panels
    if call.data == 'manageing_panels':
        Text_4='شما در حال مدیریت کردن پنل ها هستید \n\n برای وارد شدن به پنل مدیریت :⚙️ '
        if BotKb.panel_management_manageing_panels() == 'no_panel_to_manage' :
            bot.send_message(call.message.chat.id , Text_0)
        else :
            bot.edit_message_text(Text_4 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.panel_management_manageing_panels())





#-------------ADD_panel-SECTION
PANEL_RECEIVING_STATE = {'Enable_Panel_Adding':False , 'Panel_Name_Receiving':False ,
                        'Panel_Url_Receiving':False , 'Panel_Username_Receiving':False ,
                        'Panel_Password_Receiving':False}


PANEL_INFORMATION = {'Panel_Name':'' , 'Panel_Url':'' ,
                     'Panel_Username':'' ,'Panel_Password':''}



#> ./Management > Panels > Add_panel - Panel_Name(step-1)
@bot.message_handler(func=lambda message: message.text =='/add_panel' or PANEL_RECEIVING_STATE['Enable_Panel_Adding']==True and PANEL_RECEIVING_STATE['Panel_Name_Receiving']==False)
def handle_incoming_panelName(message):

    if message.text =='/add_panel' :
        admins_ = admins.objects.get(user_id = int(message.from_user.id))
        if  admins_.is_owner == 1 or (admins_.is_admin == 1 and admins_.acc_panels ==1):
            PANEL_RECEIVING_STATE['Enable_Panel_Adding']=True
            Text_0='یک اسم برای پنل خود انتخاب کنید؟\n⚠️.دقت کنید که این اسم مستقیما در قسمت خرید سرویس ها نمایش داده میشود\n\nمثال ها : \n سرویس هوشمند ، سرور مولتی لوکیشن \n\nTO CANCEL : /CANCEL'
            bot.send_message(message.chat.id , Text_0)
        else:
            bot.send_message(message.chat.id , 'شما نمتوانید پنلی را اضافه کنید')
        return
    
    if PANEL_RECEIVING_STATE['Panel_Name_Receiving']==False and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        PANEL_RECEIVING_STATE.update({key:False for key in PANEL_RECEIVING_STATE})
        Text_1='✍🏻 .اضافه کردن پنل لغو شد!!'
        bot.send_message(message.chat.id , Text_1 , reply_markup=BotKb.panel_management_menu_in_admin_side())      
    else :
        if len(message.text) <= 124 :
            PANEL_INFORMATION['Panel_Name']=message.text
            PANEL_RECEIVING_STATE['Panel_Name_Receiving']=True
            Text_2='✅.اسم پنل دریافت شد\n\n .ادرس پنل را ارسال کنید \n فرمت های صحیح :\nhttp://panelurl.com:port\nhttps://panelurl.com:port\nhttp://ip:port\nhttps://ip:port\n\nTO CANCEL : /CANCEL'
            bot.send_message(message.chat.id , Text_2)            
        else:
            Text_3='❌.اسم پنل نباید بیشتر از 124 حروف باشد\n\nTO CANCEL : /CANCEL'
            bot.send_message(message.chat.id , Text_3)



#> ./Management > Panel > Add_panel - Panel_Url(step-2)
@bot.message_handler(func=lambda message:PANEL_RECEIVING_STATE['Enable_Panel_Adding']==True and PANEL_RECEIVING_STATE['Panel_Url_Receiving']==False)
def handle_incoming_panelUrl(message):
    if PANEL_RECEIVING_STATE['Panel_Url_Receiving']==False and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        PANEL_RECEIVING_STATE.update({key:False for key in PANEL_RECEIVING_STATE})
        Text_1='✍🏻 .اضافه کردن پنل لغو شد!!'
        bot.send_message(message.chat.id , Text_1 , reply_markup=BotKb.panel_management_menu_in_admin_side())      
    else:
        pattern=(
                    r'^(http|https):\/\/' 
                    r'('
                        r'[\w.-]+'
                        r'|'
                        r'(\d{1,3}\.){3}\d{1,3}'
                    r')'
                    r'(:\d{1,5})?$'
                )
        http_or_https_chekcer=re.search(pattern , message.text)
        if http_or_https_chekcer: 
            PANEL_INFORMATION['Panel_Url']=http_or_https_chekcer.group(0)
            PANEL_RECEIVING_STATE['Panel_Url_Receiving']=True
            Text_2='✅.آدرس پنل دریافت شد \n\n حالا یوزرنیم پنل رو برای ورود به پنل وارد کنید \n\nTO CANCEL : /CANCEL'
            bot.send_message(message.chat.id , Text_2)
        else: 
            Text_3='فرمت ادرس پنل اشتباه است.❌ \n\n فرمت درست به شکل زیر میباشد.\n\n http://panelurl.com:port \n https://panelurl.com:port \n http://ip:port \n https://ip:port '
            bot.send_message(message.chat.id ,Text_3) 





#> ./Management > Panel > Add_panel - Panel_Username(step-3)
@bot.message_handler(func=lambda message:PANEL_RECEIVING_STATE['Enable_Panel_Adding']==True and PANEL_RECEIVING_STATE['Panel_Username_Receiving']==False)
def handle_incoming_panelUsername(message):
    if PANEL_RECEIVING_STATE['Panel_Username_Receiving'] == False and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        PANEL_RECEIVING_STATE.update({key:False for key in PANEL_RECEIVING_STATE})
        Text_1='✍🏻 .اضافه کردن پنل لغو شد!!'
        bot.send_message(message.chat.id , Text_1 , reply_markup=BotKb.panel_management_menu_in_admin_side() )       
    else:
        PANEL_INFORMATION['Panel_Username'] = message.text
        PANEL_RECEIVING_STATE['Panel_Username_Receiving']=True
        Text_2='✅یوزرنیم پنل دریافت شد.\n\n حالا پسورد پنل رو برای ورود به پنل وارد کنید.\n\nTO CANCEL : /CANCEL'
        bot.send_message(message.chat.id , Text_2)




#> ./Management > Panel > Add_panel - Panel_Password(step-4)
@bot.message_handler(func=lambda message:PANEL_RECEIVING_STATE['Enable_Panel_Adding']==True and PANEL_RECEIVING_STATE['Panel_Password_Receiving']==False)
def handle_incoming_panelPassword(message):
    if PANEL_RECEIVING_STATE['Panel_Password_Receiving']==False and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        PANEL_RECEIVING_STATE.update({key:False for key in PANEL_RECEIVING_STATE})
        Text_1='✍🏻 .اضافه کردن پنل لغو شد!!'
        bot.send_message(message.chat.id , Text_1 ,reply_markup=BotKb.panel_management_menu_in_admin_side() )   
    else :
        PANEL_INFORMATION['Panel_Password']=message.text
        PANEL_RECEIVING_STATE['Panel_Password_Receiving']=True
        add_panel_database(PANEL_INFORMATION['Panel_Name'] , PANEL_INFORMATION['Panel_Url'] , PANEL_INFORMATION['Panel_Username'] , PANEL_INFORMATION['Panel_Password'] , PANEL_INFORMATION , message , bot)











#-------------REMOVE_panel-SECTION
#> ./Management > Panel > Remove_Panel (step-1)
@bot.callback_query_handler(func=lambda call:call.data.startswith(('remove_products_panel_' , 'remove_only_panel_' , 'panel_remove_')) or call.data in ['back_to_manage_panel' , 'back_to_remove_panel_section'] )
def handle_removing_panels(call): 
    if call.data.startswith('panel_remove_'):
        panel_id= call.data.split('_')
        Text_1 ='عمل ترجیحی را انتخاب نمایید'
        bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.panel_management_remove_panel(panel_id[2],kind=True))


    if call.data.startswith('remove_products_panel_'):
        panel_id = call.data.split("_")
        remove_panel_database(panel_id[3] , bot , call , product=True)


    if call.data.startswith('remove_only_panel_'):
        panel_id = call.data.split("_")
        remove_panel_database(panel_id[3] , bot , call , panel=True)


    #- Back-button
    if call.data=='back_to_manage_panel':
        Text_back_1='شما در حال مدیریت کردن بخش پنل ها هستید'
        bot.edit_message_text(Text_back_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.panel_management_menu_in_admin_side())
    
    #- Back-button
    if call.data=='back_to_remove_panel_section':
        Text_back_2 = '🚦برای حذف کردن پنلی که میخواهید بر روی اون کلیک کنید'    
        bot.edit_message_text(Text_back_2 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.panel_management_remove_panel())







#-------------MANAGING_panel-SECTION
CHANGING_PANEL_DETAILS={'Panel_Name':False , 'Panel_Url':False ,
                        'Panel_Username':False , 'Panel_Password':False ,
                        'All_Capcity' : False}

PANEL_ID={'panel_id': int}

#> ./Management > Panel > Manageing_Panels(step-1)
@bot.callback_query_handler(func=lambda call:call.data.startswith(('manageing_panel_' , 'panel_status_' , 'panel_name_' , 'panel_url_' , 'panel_username_' , 'panel_password_' , 'view_password_' , 'view_username_' , 'reality_flow_' , 'panel_capacity_','panel_statics_')) or call.data in ['back_to_manageing_panels'] )
def handle_panel_management(call) :
    call_data=call.data.split('_')
    PANEL_ID['panel_id']=call_data[2]
    

    if call.data.startswith(('manageing_panel_')):
        Text_1='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید'
        bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_selected_panel(panel_pk=call_data[2]))

    #- Back butotn 
    if call.data=='back_to_manageing_panels':
        Text_back='شما در حال مدیریت کردن بخش پنل ها هستید'
        bot.edit_message_text(Text_back , call.message.chat.id , call.message.message_id , reply_markup=BotKb.panel_management_manageing_panels())
    
    
    #- Change-Status
    if call.data.startswith('panel_status_'):
        change_panel_status(call_data[2] , bot , call)


    #- Change-Name
    if call.data.startswith('panel_name_'):
        CHANGING_PANEL_DETAILS['Panel_Name']=True
        Text_2=f'یک نام جدید برای پنل وارد کنید \n\nنام فعلی : {call_data[3]}\n\nTO CANCEL : /CANCEL'
        bot.edit_message_text(Text_2 , call.message.chat.id , call.message.message_id )
        

    #- Change-Url
    if call.data.startswith('panel_url_'):
        CHANGING_PANEL_DETAILS['Panel_Url'] = True
        Text_3=f'ادرس جدید پنل را وارد کنید \n\n ادرس فعلی :{call_data[3]}\n\nTO CANCEL : /CANCEL'
        bot.edit_message_text(Text_3 , call.message.chat.id , call.message.message_id)


    #- Change-Username
    if call.data.startswith('panel_username_'):
        CHANGING_PANEL_DETAILS['Panel_Username'] = True
        Text_4=f'یوزر نیم جدید پنل را وارد کنید \n\nTO CANCEL : /CANCEL'
        bot.edit_message_text(Text_4 , call.message.chat.id , call.message.message_id)

    #- Show-Username
    if  call.data.startswith('view_username_'):
        BotKb.manage_selected_panel(panel_pk=call_data[2] , username=True)
        Text_5='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید'
        bot.edit_message_text(Text_5 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_selected_panel(panel_pk=call_data[2] , username=True))
            

    #- Change-Password
    if call.data.startswith('panel_password_'):
        CHANGING_PANEL_DETAILS['Panel_Password'] = True
        Text_6=f' پسورد جدید پنل را وارد کنید \n\nTO CANCEL : /CANCEL'
        bot.edit_message_text(Text_6 , call.message.chat.id , call.message.message_id)
        

    #- Show-Password
    if  call.data.startswith('view_password_'):
        BotKb.manage_selected_panel(panel_pk=call_data[2] , passwd=True)
        Text_7='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید'
        bot.edit_message_text(Text_7 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_selected_panel(panel_pk=call_data[2] , passwd=True))
            

    #- Change-RealityFLow
    if call.data.startswith('reality_flow_'):
        Text_8='حالت ریلیتی - فلو برای کل اشتراک ها رواین پنل انتخاب کنید'
        bot.edit_message_text(Text_8 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.changin_reality_flow() )


    #- Change-Capcity 
    if call.data.startswith('panel_capacity_'):
        Text_9='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید'
        bot.edit_message_text(Text_9 , call.message.chat.id , call.message.message_id , reply_markup = BotKb.changin_panel_capcity(panel_pk=call_data[2]))



    if call.data.startswith('panel_statics_'):
        bot.edit_message_text(panel_state(int(call_data[-1])) , call.message.chat.id , call.message.message_id , reply_markup=BotKb.updating_panel(int(call_data[-1])))









#> ./Management > Panel > Manageing_Panels - Change (Panel_Name , Panel_Url , Panel_Username , Panel_Password)(step-2)
@bot.message_handler(func=lambda message:CHANGING_PANEL_DETAILS['Panel_Name']==True or CHANGING_PANEL_DETAILS['Panel_Url']==True or CHANGING_PANEL_DETAILS['Panel_Username']==True or CHANGING_PANEL_DETAILS['Panel_Password']==True or CHANGING_PANEL_DETAILS['All_Capcity']==True)
def get_CHANGING_PANEL_DETAILS_name(message):

    #- Change-Name
    if CHANGING_PANEL_DETAILS['Panel_Name']==True:
        change_panel_name(PANEL_ID['panel_id'], bot , message , CHANGING_PANEL_DETAILS)

    #- Change-Url
    if CHANGING_PANEL_DETAILS['Panel_Url']==True:
        change_panel_url(PANEL_ID['panel_id'] , bot , message , CHANGING_PANEL_DETAILS)

    #- Change-Username
    if CHANGING_PANEL_DETAILS['Panel_Username']==True:
        change_panel_username(PANEL_ID['panel_id'] , bot , message , CHANGING_PANEL_DETAILS)

    #- Change-Password
    if CHANGING_PANEL_DETAILS['Panel_Password']==True:
        change_panel_password(PANEL_ID['panel_id'] , bot , message , CHANGING_PANEL_DETAILS)

    #- Change-Allcapcity
    if CHANGING_PANEL_DETAILS['All_Capcity']==True:
        change_panel_allcapcity(PANEL_ID['panel_id'] , bot , message , CHANGING_PANEL_DETAILS)



#> ./Managemetn > Panel > Manageing_Panels - Change Reality-Flow(step-3)
@bot.callback_query_handler(func=lambda call:call.data in ['None_realityFlow' , 'xtls-rprx-vision'])
def reality_flow(call):

    #- Reality - flow 
    if call.data=='xtls-rprx-vision':
        change_panel_realityflow(PANEL_ID['panel_id'] , bot , call , reality=True)
        
    #-none Reality - flow 
    if call.data=='None_realityFlow':
        change_panel_realityflow(PANEL_ID['panel_id'] , bot , call , none_reality=True)




#> ./Management > Panel > Manageing_Panels - Change (Capcity-Mode , Sale-Mode)(step-4)
@bot.callback_query_handler(func=lambda call:call.data.startswith('all_capcity_') or call.data in [ 'capcity_mode' , 'sale_mode'  , 'back_from_panel_capcity_list'])
def CHANGING_PANEL_DETAILS_capicty(call) :
    #- Capcity-mode
    if call.data=='capcity_mode':
        change_panel_capcitymode(PANEL_ID['panel_id'] , bot , call)

    #- Sale-mode
    if call.data=='sale_mode':
        change_panel_salemode(PANEL_ID['panel_id'] , bot , call)

    #- All-Capcity
    if call.data.startswith('all_capcity_') :
        CHANGING_PANEL_DETAILS['All_Capcity'] = True
        call_data = call.data.split("_")[2]
        Text_1=f'مقدار عددی ظرفیت کلی پنل را ارسال کنید \n ظرفیت فعلی :{call_data}\n\nTO CANCEL : /CANCEL'
        bot.send_message(call.message.chat.id , Text_1)


    if call.data == 'back_from_panel_capcity_list' :
        Text_back='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید'
        bot.edit_message_text(Text_back , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_selected_panel(panel_pk=PANEL_ID['panel_id']))




#> ./Management > Panel > Manageing_Panels - Change (How-To-Send , Qrcode-Mode , Config-Mode) (step-7-4)
@bot.callback_query_handler(func=lambda call:call.data.startswith('send_config_') or call.data in ['qrcode_sending' , 'link_sending' , 'back_from_panel_howtosend_list'])
def CHANGING_PANEL_DETAILS_capicty(call) :
    
    if call.data.startswith('send_config_'):
        Text_1='تعیین کنید هنگام خرید موفق اشتراک  لینک ها چگونه ارسال شوند ⁉️'
        bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.how_to_send_links(PANEL_ID['panel_id']))

    #- QRcode
    if call.data =='qrcode_sending':
        change_panel_qrcode(PANEL_ID['panel_id'] , bot , call)

    #- Config
    if call.data =='link_sending':
        change_panel_config(PANEL_ID['panel_id'] , bot , call)

    #- Back button
    if call.data=='back_from_panel_howtosend_list': 
            Text_back='🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید'
            bot.edit_message_text(Text_back , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_selected_panel(panel_pk=PANEL_ID['panel_id']))
    






@bot.callback_query_handler(func= lambda call : call.data.startswith(('updating_panel_')) or call.data in ['back_from_panel_static'])
def handle_panel_static(call):
    #- panel-statics


    if call.data.startswith('updating_panel_'):
        bot.edit_message_text(panel_state(int(PANEL_ID['panel_id'])) , call.message.chat.id , call.message.message_id , reply_markup=BotKb.updating_panel(panel_id= int(PANEL_ID['panel_id']) )  )
    

    if call.data =='back_from_panel_static':
        Text_back_2 = '🔗برای تغییر تنظیمات  بر روی دکمه ها کلیک کنید'
        bot.edit_message_text(Text_back_2 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_selected_panel(panel_pk=int(PANEL_ID['panel_id'])))









#---------------------------------------------------------------------------------------------------------------------------------#
# -------------------------PRODUCTS-MANAGEMENT------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------------------#


#> ./Management > Product 
@bot.callback_query_handler(func=lambda call:call.data in [ 'products_management' , 'add_product' , 'remove_product' , 'manage_products' , 'back_from_products_manageing'])
def handle_products(call) :

    panel_=v2panel.objects.all()
    Text_0='هیچ پنلی برای لود کردن وجود ندارد \n\n اولین پنل خود را اضافه کنید :/add_panel'


    if call.data=='products_management':
        admins_ = admins.objects.get(user_id = int(call.from_user.id))
        if (admins_.acc_panels == 1 and admins_.acc_products ==1) or admins_.is_owner ==1:
            Text_1='✏️شما در حال مدیریت کردن بخش محصولات میباشید'
            bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.product_management_menu_in_admin_side())
        else :
            bot.send_message(call.message.chat.id , 'شما اجازه دسترسی به این قسمت را ندارید')



    if call.data=='back_from_products_manageing':
        Text_2='به مدیریت ربات خوش امدید'
        bot.edit_message_text(Text_2 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.management_menu_in_admin_side(user_id = call.from_user.id))


    #- Adding products 
    if call.data=='add_product':
        no_panel=BotKb.load_panel_add_product()
        if no_panel=='no_panel_to_load':
            bot.send_message(call.message.chat.id , Text_2)
        else:
            Text_3='📌یک پنل را برای اضافه کردن محصول به آن انتخاب کنید \n\n⚠️محصول زیر مجموعه پنل خواهد بود '
            bot.edit_message_text(Text_3 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.load_panel_add_product(add_product=True))
            


    #- Removing products
    if call.data == 'remove_product' :
        no_panel=BotKb.load_panel_add_product(remove_product=True)
        if no_panel=='no_panel_to_load':
            bot.send_message(call.message.chat.id , Text_0)
        else:
            Text_4='📌پنلی که میخواهید محصولات آن را حذف کنید را انتخاب نمایید'
            bot.edit_message_text(Text_4, call.message.chat.id , call.message.message_id , reply_markup=BotKb.load_panel_add_product(remove_product=True))
        

    
    #- Managing products
    if call.data=='manage_products':
        keyboard_manage=InlineKeyboardMarkup()
        no_panel=BotKb.load_panel_add_product(manage_product=True)
        if no_panel=='no_panel_to_load':
            bot.send_message(call.message.chat.id , Text_0)
        else:
            Text_5='📌پنلی را که میخواهید محصولات آن را مدیریت کنید انتخاب نمایید'
            bot.edit_message_text(Text_5 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.load_panel_add_product(manage_product=True))
                            




#-------------ADD_products-SECTION
PRODUCT_RECEIVING_STATE={'Enable_Product_Adding' : False , 'Product_Name_Receiving' : False , 
                          'Data_Limit_Receiving' : False , 'Expire_Date_Receiving' : False ,
                          'Product_Cost_Receiving' : False ,}


PRODUCT_INFORMATION={'Panel_Id' : '', 
                    'Product_Name' : '' ,'Data_Limit' : '' ,
                    'Expire_Date' : '' , 'Product_Cost' : '' , }

INBOUND_SELECTOR={'Inbounds':None}

#> ./Management > Product > Add_Product - Select_PanelId(step-1)
@bot.callback_query_handler(func=lambda call:call.data.startswith('panel_product_'))
def handle_incoming_product_panelId(call):
    if call.data.startswith('panel_product_'): 
        
        PRODUCT_RECEIVING_STATE['Enable_Product_Adding']=True
        PRODUCT_RECEIVING_STATE.update({key:False for key in PRODUCT_RECEIVING_STATE if key!='Enable_Product_Adding'})
        INBOUND_SELECTOR['Inbounds']=''
        call_data=call.data.split("_")
        PRODUCT_INFORMATION['Panel_Id']=call_data[2]
        call_panel_api = panelsapi.marzban(panel_id=call_data[2])
        inbounds = call_panel_api.get_inbounds()
        INBOUND_SELECTOR['Inbounds'] = [f" {tag['protocol']} : {tag['tag']} " for outer in inbounds for tag in inbounds[outer]]
        Text_1='📌یک نام برای محصول خود انتخاب نمایید \n\nTO CANCEL : /CANCEL'
        bot.send_message(call.message.chat.id , Text_1)
        



#> ./Management > Product > Add_Product - Product_Name(step2)
@bot.message_handler(func=lambda message :PRODUCT_RECEIVING_STATE['Enable_Product_Adding']==True and PRODUCT_RECEIVING_STATE['Product_Name_Receiving']==False)
def handle_incoming_product_name(message):
    if PRODUCT_RECEIVING_STATE['Product_Name_Receiving']==False and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        PRODUCT_RECEIVING_STATE.update({key:False for key in PRODUCT_RECEIVING_STATE})
        Text_1='✍🏻 .اضافه کردن محصول لغو شد!!'
        bot.send_message(message.chat.id , Text_1 , reply_markup=BotKb.product_management_menu_in_admin_side())
    else :
        if len(message.text)<=128:  
            PRODUCT_INFORMATION['Product_Name']=message.text
            PRODUCT_RECEIVING_STATE['Product_Name_Receiving'] = True
            Text_2='🔋مقدار حجم محصول را ارسال کنید \n ⚠️ دقت کنید حجم محصول باید برحسب گیگابایت باشد \n\nTO CANCEL : /CANCEL'
            bot.send_message(message.chat.id , Text_2)
        else:
            Text_3='❌نام محصول نباید بیشتر از 64 حرف/کرکتر باشد \n\nTO CANCEL : /CANCEL'
            bot.send_message(message.chat.id , Text_3)



#> ./Managemet > Product > Add_Product - Data_Limit(step-3)
@bot.message_handler(func=lambda message:PRODUCT_RECEIVING_STATE['Enable_Product_Adding']==True and PRODUCT_RECEIVING_STATE['Data_Limit_Receiving']==False )
def handle_incoming_data_limit(message) :
    if PRODUCT_RECEIVING_STATE['Data_Limit_Receiving']==False and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        PRODUCT_RECEIVING_STATE.update({key:False for key in PRODUCT_RECEIVING_STATE})
        Text_1='✍🏻 .اضافه کردن محصول لغو شد!!'
        bot.send_message(message.chat.id , Text_1 , reply_markup=BotKb.product_management_menu_in_admin_side())
    else :
        if message.text.isdigit():
            data_limit_checker=re.search(r'([0-9]{1,9}|[0-9]{1,9}\.[0-9]{0,3})' , message.text)
            if data_limit_checker:
                PRODUCT_INFORMATION['Data_Limit']=data_limit_checker.group(0)
                PRODUCT_RECEIVING_STATE['Data_Limit_Receiving']=True
                Text_2='⌛️مقدار دوره محصول را ارسال کنید \n\n مثال :30,60 \n⚠️ این عدد در هنگام خرید محصول به عنوان روز در نظر گرفته میشود : مثلا 30 روز\n\nTO CANCEL : /CANCEL'
                bot.send_message(message.chat.id , Text_2)
            else:
                Text_3='❌فرمت حجم محصول اشتباه است\n\nفرمت صحیح میتواند با اعشار تمام شود \nمثلا:20,30 \n\nTO CANCEL : /CANCEL'
                bot.send_message(message.chat.id , Text_3)
        else:
            Text_4='❌متن ارسالی باید شامل عدد باشد نه حروف \n\nTO CANCEL : /CANCEL'
            bot.send_message(message.chat.id , Text_4)
            



#> ./Management > Product >  Add_Product - Expire_Date(step-4)
@bot.message_handler(func=lambda message:PRODUCT_RECEIVING_STATE['Enable_Product_Adding']==True and PRODUCT_RECEIVING_STATE['Expire_Date_Receiving']==False)
def handle_incoming_expire_date(message):
    if PRODUCT_RECEIVING_STATE['Expire_Date_Receiving']==False and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        PRODUCT_RECEIVING_STATE.update({key:False for key in PRODUCT_RECEIVING_STATE})
        Text_1='✍🏻 .اضافه کردن محصول لغو شد!!'
        bot.send_message(message.chat.id , Text_1 , reply_markup=BotKb.product_management_menu_in_admin_side())
    else:
        if message.text.isdigit():
            PRODUCT_INFORMATION['Expire_Date']=message.text
            PRODUCT_RECEIVING_STATE['Expire_Date_Receiving']=True
            Text_2='💵قیمت محصول را ارسال کنید \n⚠️قیمت محصول باید به تومان باشد\n\nTO CANCEL : /CANCEL'
            bot.send_message(message.chat.id , Text_2)
        else : 
            Text_3='❌متن ارسالی باید شامل عدد باشد نه حروف \n\nTO CANCEL : /CANCEL'
            bot.send_message(message.chat.id , Text_3)
            


#> ./Management > Product > Add_Product - Pro_Cost(step-5)
@bot.message_handler(func=lambda message:PRODUCT_RECEIVING_STATE['Enable_Product_Adding']==True and PRODUCT_RECEIVING_STATE['Product_Cost_Receiving']==False)
def handle_incoming_expire_date(message):
    if PRODUCT_RECEIVING_STATE['Product_Cost_Receiving']==False and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        PRODUCT_RECEIVING_STATE.update({key:False for key in PRODUCT_RECEIVING_STATE})
        Text_1='✍🏻 .اضافه کردن محصول لغو شد!!'
        bot.send_message(message.chat.id , Text_1 , reply_markup=BotKb.product_management_menu_in_admin_side())
    else :
        if not message.text.isdigit():
            Text_2='❌متن ارسالی باید شامل عدد باشد نه حروف \n\nTO CANCEL : /CANCEL'
            bot.send_message(message.chat.id , Text_2 )
        else:
            PRODUCT_INFORMATION['Product_Cost']=message.text
            PRODUCT_RECEIVING_STATE['Product_Cost_Receiving']=True
            Text_3=f'اینباند های محصول را انتخاب کنید\n این اینباند هنگام ساخت محصول داخل اشتراک قرار خواهد گرفت\nلیست اینباند های انتخابی :\n []'
            bot.send_message(message.chat.id , Text_3 , reply_markup=BotKb.select_inbounds(INBOUND_SELECTOR['Inbounds']))
            
            

#> ./Management > Product > Add_Product - Pro_Inbounds(step-6)
@bot.callback_query_handler(func=lambda call:(INBOUND_SELECTOR['Inbounds'] is not None and call.data in INBOUND_SELECTOR['Inbounds']) or call.data in ['done_inbounds' , 'back_from_inbounds_selecting'])
def select_inbounds(call):
    if  (INBOUND_SELECTOR['Inbounds'] is not None and call.data in INBOUND_SELECTOR['Inbounds']):
        inbounds_list=INBOUND_SELECTOR['Inbounds']
        for i in inbounds_list:
            if call.data==i:
                index_inboundlist=inbounds_list.index(call.data)
                if '✅' in i:
                    new_values=i.replace('✅', '❌')
                    inbounds_list[index_inboundlist]=new_values  
                elif '❌' in i:
                    new_values=i.replace('❌', '✅')
                    inbounds_list[index_inboundlist]=new_values  
                else:
                    values=i + '✅'
                    inbounds_list[index_inboundlist]=values  

        inbounds_checkmark=[]
        for i in INBOUND_SELECTOR['Inbounds']:
            if  '✅' in i:
                inbounds_checkmark.append(i.strip('✅'))
            Text_1=f"لیست اینباند های انتخابی:\n\n {inbounds_checkmark}"
        keyboard = BotKb.select_inbounds(inbounds_list) 
        bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=keyboard)


    if call.data=='done_inbounds':
        grouped_inbounds = {}
        for items in INBOUND_SELECTOR['Inbounds']:
            key , value = items.split(':' , 1)
            if '✅' in value:

                if key not in grouped_inbounds :
                    grouped_inbounds[key]=[]
                grouped_inbounds[key].append(value.strip('✅'))
        if len(grouped_inbounds) > 0:
            add_product_database(call , bot , PRODUCT_INFORMATION , grouped_inbounds)
        else:
            bot.answer_callback_query(call.id , 'اینباند محصول نمیتواند خالی باشد')



    if call.data=='back_from_inbounds_selecting':
        Text_2='✏️شما در حال مدیریت کردن بخش محصولات میباشید'
        bot.edit_message_text(Text_2 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.product_management_menu_in_admin_side())
        bot.answer_callback_query(call.id , 'اضافه کردن محصول لغو شد')






#-------------REMOVE_products-SECTION
PRODUCT_REMOVE_PANELID = {'Panel_Id' : int}
#> ./Management > Product > Remove-Product (step-1)
@bot.callback_query_handler(func=lambda call:call.data.startswith(('remove_panel_product_' , 'delete_prodcut_' , 'remove_prev_page_products_' , 'remove_next_page_products_')) or call.data in ['back_remove_panel_product_', 'back_panel_product_' , 'back_managing_panel_product_' , 'back_from_remove_products'])
def handle_removing_products(call):

    #-load panels 
    if call.data.startswith('remove_panel_product_'):
        call_data=call.data.split('_')
        if BotKb.product_managemet_remove_products(panel_pk=call_data[3])=='no_products_to_remove':
            Text_1='هیچ محصولی وجود ندارد \n محصولی اضافه  کنید\n\n /add_product'
            bot.send_message(call.message.chat.id , Text_1)
        else:
            Text_2='محصولی را که میخواهید حذف کنید را انتخاب کنید\n برای حذف کافیست بر روی آن کلیک کنید'
            PRODUCT_REMOVE_PANELID['Panel_Id']=call_data[3]

            bot.edit_message_text(Text_2 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.product_managemet_remove_products(panel_pk=call_data[3]))
            

    #- delete product
    if call.data.startswith('delete_prodcut_'):
        print(PRODUCT_REMOVE_PANELID)
        call_data=call.data.split('_')
        remove_product_database(call , bot , call_data[2] , PRODUCT_REMOVE_PANELID)



    #- next page
    if call.data.startswith('remove_next_page_products_'):
        page_number=int(call.data.split('_')[-1])
        Text_3=f'محصولی را که میخواهید حذف کنید را انتخاب کنید\n برای حذف کافیست بر روی آن کلیک کنید \n صفحه :‌ {page_number}'
        bot.edit_message_text(Text_3 , call.message.chat.id ,call.message.message_id ,reply_markup= BotKb.product_managemet_remove_products(panel_pk=PRODUCT_REMOVE_PANELID['Panel_Id'] , page=page_number))
        

    #- prev page
    if call.data.startswith('remove_prev_page_products_') :
        page_number=int(call.data.split('_')[-1])
        Text_4=f'محصولی را که میخواهید حذف کنید را انتخاب کنید\n برای حذف کافیست بر روی آن کلیک کنید \n صفحه :‌ {page_number}'
        bot.edit_message_text(Text_4 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.product_managemet_remove_products(panel_pk=PRODUCT_REMOVE_PANELID['Panel_Id'] , page=page_number))



    #- back - button
    if call.data=='back_remove_panel_product_' or call.data=='back_panel_product_' or call.data=='back_managing_panel_product_':
        Text_back_1='✏️شما در حال مدیریت کردن بخش محصولات میباشید'
        bot.edit_message_text(Text_back_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.product_management_menu_in_admin_side())


    if call.data=='back_from_remove_products':
        Text_back_2='پنلی که میخواهید محصولات آن را حذف کنید را انتخاب نمایید'
        bot.edit_message_text(Text_back_2 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.load_panel_add_product(remove_product=True) )

    





#-------------MANAGING_products-SECTION

PANEL_PK={'PanelPK' : ''}
PRODUCT_PAGE={'Page' : 1}

#> ./Management > Products > Manage-Product(step-1)
@bot.callback_query_handler(func=lambda call:call.data.startswith(('managing_panel_product_' , 'down_' , 'up_' , 'product_next_page_products_' , 'product_prev_page_products_')) or call.data in ['back_from_manage_products_list_updown'])
def manage_product_choose_panel(call): 
    #- Listing product
    if call.data.startswith('managing_panel_product_'):
        if BotKb.products_list(call.data.split('_')[3])=='no_product_to_manage':
            Text_1='هیچ محصولی وجود ندارد ❌\n محصولی اضافه  کنید\n\n /add_product'
            bot.send_message(call.message.chat.id , Text_1)
        else:
            call_data=call.data.split('_')[-1]
            PANEL_PK['PanelPK']=call_data
            panel_=v2panel.objects.get(id=call_data)
            Text_2=f'📝لیست تمام محصولات پنل <b>({panel_.panel_name})</b> به صورت زیر میباشد'
            bot.edit_message_text(Text_2 , call.message.chat.id ,call.message.message_id ,reply_markup= BotKb.products_list(panel_pk=call_data) , parse_mode='HTML')
        

    #- down button
    if call.data.startswith('down_'):
        call_data=call.data.split('_')[-1]
        BotKb.products_list(panel_pk=PANEL_PK['PanelPK'] , down=int(call_data))
        Text_3='جایگاه محصول به پایین🔻 جابه جا شد \n ⚪️این جابه جایی در نحوه نمایش محصول هنگام خرید تاثیر خواهد گزاشت'
        bot.edit_message_text(Text_3 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.products_list(panel_pk=PANEL_PK['PanelPK'] , page=PRODUCT_PAGE['Page']))

    #- up button
    if call.data.startswith('up_'):
        call_data=call.data.split('_')[-1]
        Text_3='جایگاه محصول به بالا🔺 جابه جا شد \n ⚪️این جابه جایی در نحوه نمایش محصول هنگام خرید تاثیر خواهد گزاشت'
        BotKb.products_list(panel_pk=PANEL_PK['PanelPK'] , up=int(call_data))
        bot.edit_message_text(Text_3 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.products_list(panel_pk=PANEL_PK['PanelPK'], page=PRODUCT_PAGE['Page']))
    

    #- Next button
    if call.data.startswith('product_next_page_products_'):
        call_data=call.data.split('_')[-1]
        PRODUCT_PAGE['Page'] = int(call_data)
        Text_4=f'بروی محصولی که میخواهید مدیریت کنید کلیک کنید\n 📂صفحه محصول بارگزاری شده :{int(call_data)}'
        bot.edit_message_text(Text_4 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.products_list(panel_pk=PANEL_PK['PanelPK']  ,  page=int(call_data)))
           


    #- Prev button
    if call.data.startswith('product_prev_page_products_') :
        call_data=call.data.split('_')[-1]
        PRODUCT_PAGE['Page'] = int(call_data)
        Text_5=f'بروی محصولی که میخواهید مدیریت کنید کلیک کنید\n 📂صفحه محصول بارگزاری شده :{int(call_data)}'
        bot.edit_message_text(Text_5 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.products_list(panel_pk=PANEL_PK['PanelPK'] ,  page=int(call_data)))
        

    #- Back button 
    if call.data=='back_from_manage_products_list_updown':
        Text_back='📌پنلی را که میخواهید محصولات آن را مدیریت کنید انتخاب نمایید'
        bot.edit_message_text(Text_back , call.message.chat.id , call.message.message_id , reply_markup=BotKb.load_panel_add_product(manage_product=True))






PRODUCT_ID={'Product_Id' : int }
CHNAGING_PRODUCT_DETAILS = {'Enable_Changing_Product_Deatails' : False ,'Product_Name' : False ,
                            'Data_Limit' : False , 'Expire_Date' : False ,
                            'Product_Cost' : False}
CHANGED_INBOUND = {'inbounds' : None , 'product_id' : int}

#> ./Management > Products > Manage-Product(step-1)
@bot.callback_query_handler(func=lambda call:call.data.startswith(('detaling_product_' , '_pr_status_' , '_product_name_' , '_data_limit_', 'ـexpire_date_' , '_pro_cost_', '_inbounds_product_')) or call.data in ['back_from_manage_products_changing_limit' , 'change_inbound_done' , 'back_from_inbounds_chaging'] or (CHANGED_INBOUND['inbounds']  is not None and call.data in CHANGED_INBOUND['inbounds']))
def manage_products_base_id (call) : 
    #-start changing
    if call.data.startswith('detaling_product_') : 
        CHNAGING_PRODUCT_DETAILS['Enable_Changing_Product_Deatails']=True
        call_data =call.data.split('_')
        PRODUCT_ID['Product_Id']=0
        PRODUCT_ID['Product_Id']=int(call_data[-1])
        Text_1='🖋برای تغییر تنظیمات هر محصول بر روی آن کلیک کنید'
        bot.edit_message_text(Text_1,call.message.chat.id ,call.message.message_id , reply_markup=BotKb.product_changing_details(product_id=int(call_data[-1])))


    #-product status
    if call.data.startswith('_pr_status_'):
        call_data = call.data.split('_')
        change_product_status(call , bot , call_data[-1] )


    #-product name
    if call.data.startswith('_product_name_')  :
        if CHNAGING_PRODUCT_DETAILS['Enable_Changing_Product_Deatails']==True :      
            CHNAGING_PRODUCT_DETAILS['Product_Name'] = True
            Text_2=f'🔗نام جدید محصول را وارد نمایید\n\nTO CANCEL : /CANCEL'
            bot.send_message(call.message.chat.id , Text_2)
                

    #- product data-limit
    if call.data.startswith('_data_limit_') :
        if CHNAGING_PRODUCT_DETAILS['Enable_Changing_Product_Deatails'] == True :
            CHNAGING_PRODUCT_DETAILS['Data_Limit'] = True
            Text_3='🔗حجم جدید محصول را وارد نمایید\n\nTO CANCEL : /CANCEL'
            bot.send_message(call.message.chat.id , Text_3)


    #- product expire-date
    if call.data.startswith('ـexpire_date_') :
        if CHNAGING_PRODUCT_DETAILS['Enable_Changing_Product_Deatails'] == True :
            CHNAGING_PRODUCT_DETAILS['Expire_Date'] = True
            Text_4='🔗دوره جدید محصول را وارد نمایید \n\nTO CANCEL : /CANCEL'
            bot.send_message(call.message.chat.id , Text_4)


    #- product cost            
    if call.data.startswith('_pro_cost_') :
         if CHNAGING_PRODUCT_DETAILS['Enable_Changing_Product_Deatails'] == True :
            CHNAGING_PRODUCT_DETAILS['Product_Cost'] = True
            Text_5='🔗قیمت جدید محصول را وارد نمایید \n\nTO CANCEL : /CANCEL'
            bot.send_message(call.message.chat.id , Text_5)



    #- product - inbounds
    if call.data.startswith('_inbounds_product_'):
        call_data = call.data.split('_')
        panel_id = products.objects.get(id = call_data[-1])
        get_inbounds = panelsapi.marzban(panel_id.panel_id).get_inbounds()
        inbound_list = [f" {tag['protocol']} : {tag['tag']} "  for outer in get_inbounds for tag in get_inbounds[outer]]
        CHANGED_INBOUND['inbounds'] = inbound_list
        CHANGED_INBOUND['product_id'] = call_data[-1]
        Text_6=f'📥اینباند محصول را انتخاب نمایید و سپس گزینه اتمام را بزنید'
        bot.edit_message_text(Text_6 , call.message.chat.id , call.message.message_id , reply_markup= BotKb.change_inbounds(CHANGED_INBOUND['inbounds'] ))

    


    if CHANGED_INBOUND['inbounds'] is not None and call.data in CHANGED_INBOUND['inbounds'] :
        change_product_inbound(call , bot , CHANGED_INBOUND)


    if call.data =='change_inbound_done':
        grouped_inbounds = {}
        for items in CHANGED_INBOUND['inbounds']:
            key , value = items.split(':' , 1)
            if '✅' in value:
                if key not in grouped_inbounds :
                    grouped_inbounds[key]=[]
                grouped_inbounds[key].append(value.strip('✅'))
        product_= products.objects.get(id = CHANGED_INBOUND['product_id'])
        product_.inbounds_selected = json.dumps(grouped_inbounds , indent=1)
        product_.save()
        Text_2='🖋برای تغییر تنظیمات هر محصول بر روی آن کلیک کنید'
        bot.edit_message_text(Text_2 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.product_changing_details(CHANGED_INBOUND['product_id']))
    

    #-back buttons
    if call.data=='back_from_inbounds_chaging':
        Text_back_1='🖋برای تغییر تنظیمات هر محصول بر روی آن کلیک کنید'
        bot.edit_message_text(Text_back_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.product_changing_details(CHANGED_INBOUND['product_id']))



    if call.data=='back_from_manage_products_changing_limit':
            panel_=v2panel.objects.get(id=PANEL_PK['PanelPK'])
            Text_back_2=f'📝لیست تمام محصولات پنل <b>({panel_.panel_name})</b> به صورت زیر میباشد'
            bot.edit_message_text(Text_back_2 , call.message.chat.id ,call.message.message_id ,reply_markup= BotKb.products_list(panel_pk=PANEL_PK['PanelPK']) , parse_mode='HTML')
               








#> ./Management > Products > Manage-Product - Changeing (Product-Name , Data-limit , Expire-date , Proudct-cost)
@bot.message_handler(func= lambda message : CHNAGING_PRODUCT_DETAILS['Product_Name']==True or CHNAGING_PRODUCT_DETAILS['Data_Limit']==True or CHNAGING_PRODUCT_DETAILS['Expire_Date'] or CHNAGING_PRODUCT_DETAILS['Product_Cost'])
def get_changing_product_details_name(message):

    #- product name
    if CHNAGING_PRODUCT_DETAILS['Product_Name']==True :
        change_product_name(message , bot , CHNAGING_PRODUCT_DETAILS , PRODUCT_ID)

    #- product data-limit
    if CHNAGING_PRODUCT_DETAILS['Data_Limit'] == True:
        change_product_datalimt(message , bot , CHNAGING_PRODUCT_DETAILS , PRODUCT_ID)


    #- product expire-date
    if CHNAGING_PRODUCT_DETAILS['Expire_Date'] == True:
        change_prdocut_expiredate(message , bot , CHNAGING_PRODUCT_DETAILS , PRODUCT_ID)

    #- product cost
    if CHNAGING_PRODUCT_DETAILS['Product_Cost'] == True:
        change_product_cost(message , bot , CHNAGING_PRODUCT_DETAILS , PRODUCT_ID)



#---------------------------------------------------------------------------------------------------------------------------------#
# -------------------------admins_management------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------------------#

#//TODO make it better if you could
#//TODO add feature to access bot static or disabling it

USER_ADMIN_INFO = {'user_id':None , 'page_item':1 ,
                   'add_admin':False ,'add_admin_id':int ,
                    'admin_name' : False}

@bot.callback_query_handler(func= lambda call  : call.data in ['admins_management', 'add_new_admin', 'back_from_admin_menu' , 'back_from_admin_access'] or call.data.startswith(('Anext_','Abefore_' ,'load_' , 'adminremove_' , 'adminaccess_', 'accpanels_','accproducts_' ,'accpbotseeting_' , 'accadmins_' , 'accusermanagment_' , 'accbotstaticts_')))
def admins_management(call):

    if call.data == 'admins_management':
        admins_ = admins.objects.get(user_id = int(call.from_user.id))
        if (admins_.acc_panels == 1 and admins_.acc_admins ==1) or admins_.is_owner ==1:
            bot.edit_message_text('برای مدیریت  ادمین ها بروی انها کلیک کیند ', call.message.chat.id , call.message.message_id , reply_markup=BotKb.show_admins())
        else :
            bot.send_message(call.message.chat.id , 'شما اجازه دسترسی به این قسمت را ندارید')



    if call.data.startswith('Anext_'):
        user_id = USER_ADMIN_INFO['user_id'] if USER_ADMIN_INFO['user_id'] is not None else None
        USER_ADMIN_INFO['page_item'] = int(call.data.split('_')[-1])
        bot.edit_message_text('برای مدیریت  ادمین ها بروی انها کلیک کیند ' , call.message.chat.id, call.message.message_id,  reply_markup= BotKb.show_admins(who= user_id,page_items=int(call.data.split('_')[-1])))
    

    if call.data.startswith('Abefore_'):
        user_id = USER_ADMIN_INFO['user_id'] if USER_ADMIN_INFO['user_id'] is not None else None
        USER_ADMIN_INFO['page_item'] = int(call.data.split('_')[-1])
        bot.edit_message_text('برای مدیریت  ادمین ها بروی انها کلیک کیند ' , call.message.chat.id, call.message.message_id,  reply_markup= BotKb.show_admins(who= user_id , page_items=int(call.data.split('_')[-1])))
    

    if call.data.startswith('load_'):
        USER_ADMIN_INFO['user_id'] = int(call.data.split('_')[-1])
        bot.edit_message_text('برای مدیریت  ادمین ها بروی انها کلیک کیند ' , call.message.chat.id, call.message.message_id,  reply_markup= BotKb.show_admins(who=int(call.data.split('_')[-1]) , page_items= USER_ADMIN_INFO['page_item']))


    if call.data == 'add_new_admin':
        USER_ADMIN_INFO['add_admin'] = True
        bot.edit_message_text('ایدی عددی ادمین را وارد کنید' , call.message.chat.id , call.message.message_id)


    if call.data.startswith('adminremove_'):
        call_data = call.data.split('_')
        try:
            admins_ = admins.objects.get(user_id = call_data[-1])
            if admins_.is_owner == 1 :
                bot.answer_callback_query(call.id , 'شما نمیتوانید اونر بات را حذف کنید')
            else:
                admins_.delete()
                USER_ADMIN_INFO['user_id'] = None
                bot.edit_message_text('✅یوزر با موفقیت از دیتابیس پاک  شد ' , call.message.chat.id , call.message.message_id , reply_markup= BotKb.show_admins())

        except Exception as delete_admin_error:
            print(f'error while deleteing admin from db // error msg : {delete_admin_error}')



    if call.data.startswith('adminaccess_'):
        call_data = call.data.split('_')
        admins_ = admins.objects.get(user_id = call.from_user.id).is_owner 
        admins_2 = admins.objects.get(user_id= int(call_data[-1])).is_owner
        if admins_ == 1 :
            if admins_2 == 1 :
                bot.send_message(call.message.chat.id , 'مدیریت کردن دسترسی های اونر مجاز نمیباشد')
            else: 
                Text_1= f'به قسمت مدیریت دسترسی های ادمین خوش امدید'
                bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_admin_acc(user_id= int(call_data[-1])))
        else:
            bot.send_message(call.message.chat.id ,'شما اجازه مدیریت کردن دسترسی ها را ندارید' )


    if call.data.startswith('accpanels_'):
        call_data = call.data.split('_')
        admins_ = admins.objects.get(user_id = int(call_data[-1]))
        new_acc_panels = 1 if admins_.acc_panels == 0 else  0 
        admins_.acc_panels = new_acc_panels
        admins_.save()
        Text_2= f'به قسمت مدیریت دسترسی های ادمین خوش امدید'
        bot.edit_message_text(Text_2 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_admin_acc(user_id= int(call_data[-1])))


    if call.data.startswith('accproducts_'):
        call_data = call.data.split('_')
        admins_ = admins.objects.get(user_id = int(call_data[-1]))
        new_acc_products = 1 if admins_.acc_products == 0 else  0 
        admins_.acc_products = new_acc_products
        admins_.save()
        Text_3= f'به قسمت مدیریت دسترسی های ادمین خوش امدید'
        bot.edit_message_text(Text_3 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_admin_acc(user_id= int(call_data[-1])))



    if call.data.startswith('accpbotseeting_'):
        call_data = call.data.split('_')
        admins_ = admins.objects.get(user_id = int(call_data[-1]))
        new_acc_botmanagment = 1 if admins_.acc_botmanagment == 0 else  0 
        admins_.acc_botmanagment = new_acc_botmanagment
        admins_.save()
        Text_4= f'به قسمت مدیریت دسترسی های ادمین خوش امدید'
        bot.edit_message_text(Text_4 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_admin_acc(user_id= int(call_data[-1])))




    if call.data.startswith('accadmins_'):
        call_data = call.data.split('_')
        admins_ = admins.objects.get(user_id = int(call_data[-1]))
        new_acc_admins = 1 if admins_.acc_admins == 0 else  0 
        admins_.acc_admins = new_acc_admins
        admins_.save()
        Text_5= f'به قسمت مدیریت دسترسی های ادمین خوش امدید'
        bot.edit_message_text(Text_5 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_admin_acc(user_id= int(call_data[-1])))



    if call.data.startswith('accusermanagment_'):
        call_data = call.data.split('_')
        admins_ = admins.objects.get(user_id = int(call_data[-1]))
        new_acc_users = 1 if admins_.acc_users == 0 else  0 
        admins_.acc_users = new_acc_users
        admins_.save()
        Text_5= f'به قسمت مدیریت دسترسی های ادمین خوش امدید'
        bot.edit_message_text(Text_5 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_admin_acc(user_id= int(call_data[-1])))



    if call.data.startswith('accbotstaticts_'):
        call_data = call.data.split("_")
        admins_ = admins.objects.get(user_id = int(call_data[-1]))
        new_acc_staticts = 1 if admins_.acc_staticts == 0 else 0
        admins_.acc_staticts = new_acc_staticts
        admins_.save()
        Text_6 = f'به قسمت مدیریت دسترسی های ادمین خوش امدید'
        bot.edit_message_text(Text_6 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_admin_acc(user_id= int(call_data[-1])))



    if call.data =='back_from_admin_access':
        Text_back = 'برای مدیریت  ادمین ها بروی انها کلیک کنید'
        bot.edit_message_text(Text_back , call.message.chat.id , call.message.message_id , reply_markup= BotKb.show_admins())


    if call.data =='back_from_admin_menu':
            USER_ADMIN_INFO['admin_name'] = False
            USER_ADMIN_INFO['add_admin'] = False
            bot.edit_message_text('به مدیریت ربات خوش امدید' , call.message.chat.id , call.message.message_id , reply_markup= BotKb.management_menu_in_admin_side(user_id = call.from_user.id))






@bot.message_handler(func= lambda message : (USER_ADMIN_INFO['admin_name'] == False and USER_ADMIN_INFO['add_admin'] == True) or (USER_ADMIN_INFO['admin_name'] == True and USER_ADMIN_INFO['add_admin'] == False))
def add_new_admin(message):
    if USER_ADMIN_INFO['add_admin'] == True and USER_ADMIN_INFO['admin_name'] == False:
        if message.text.isdigit():
            bot.send_message(message.chat.id, 'ایدی عددی ادمین جدید دریافت شد \n یک نام برای ادمین انتخاب کنید')
            USER_ADMIN_INFO['add_admin'] = False
            USER_ADMIN_INFO['admin_name'] = True
            USER_ADMIN_INFO['add_admin_id'] = message.text
        else:
            bot.send_message(message.chat.id, 'ایدی باید به صورت عدد باشد نه حروف')
        return  


    if USER_ADMIN_INFO['admin_name'] == True and USER_ADMIN_INFO['add_admin'] == False:
        try:
            admins_ = admins.objects.create(admin_name=message.text, user_id=USER_ADMIN_INFO['add_admin_id'], is_admin=1, is_owner=0, acc_botmanagment=0, acc_panels=0, acc_products=0, acc_admins=0)
        except Exception as error_admin_adding:
            print(f'Error while adding admin to db: {error_admin_adding}')
            bot.send_message(message.chat.id, 'خطایی در افزودن ادمین به دیتابیس رخ داد')
            return
        
        bot.send_message(message.chat.id, 'ادمین با موفقیت به دیتابیس اضافه شد ✅', reply_markup=BotKb.show_admins())
        USER_ADMIN_INFO['admin_name'] = False
        USER_ADMIN_INFO['add_admin'] = False
        return  




#---------------------------------------------------------------------------------------------------------------------------------#
# -------------------------bot_statics------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------------------#



#//TODO add inline keyboard to this section > for example : which user buy the most , which product have been sold a lot , which panel has a lot user and other things in another versions

@bot.callback_query_handler(func= lambda call: call.data in ['bot_statics', 'back_from_bot_statics', 'users_static', 'products_static', 'panels_static', 'inovices_static', 'payments_static'])
def bot_statics(call):
    if call.data =='bot_statics':
        admins_ = admins.objects.get(user_id = int(call.from_user.id))
        if (admins_.acc_staticts == 1 and admins_.acc_staticts ==1) or admins_.is_owner ==1:
            user_ = users.objects.all().count()
            inovices_ = inovices.objects.all().count()
            payment_ = payments.objects.filter(payment_status = 'accepted').all().count()
            v2panel_ = v2panel.objects.all().count()
            product_ = products.objects.all().count()
            Text_1 = f"""

        آمار ربات به صورت زیر میباشد
👤 تعداد کل یوزر های ربات: {user_}
🎛 تعداد کل پنل های متصل به ربات: {v2panel_}
🔖تعداد کل محصولات ربات : {product_}
🛍 تعداد کل پرداختی ها : {payment_}
📃 تعداد کل فاکتور های صادر شده : {inovices_}
        """
        
            bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.bot_static())
        else :
            bot.send_message(call.message.chat.id , 'شما اجازه دسترسی به این قسمت را ندارید')






    #- bot static - USERS
    if call.data == 'users_static':
        users_ = users.objects
        if users_.all().exists():
            
            Text_users = f"""
📊- آمار کاربران 

── تعداد کل کاربران : {users_.all().count()} نفر
── تعداد کاربران بلاک شده : {users_.filter(block_status =1).count()} نفر 
── کل موجودی کیف پول کاربران : {format(int(users_.all().aggregate(Sum('user_wallet'))['user_wallet__sum']) , ',')} تومان
── بیشترین موجودی کیف پول کاربران : {format(int(users_.all().aggregate(Max('user_wallet'))['user_wallet__max']) ,',')} تومان

╣ - کاربران دارای بیشترین موجودی -
"""
            more_money = [i for i in users_.filter(user_wallet__gt = 25000).order_by('user_wallet').reverse()[:4]]

            users_static_list = []
            users_static_list.append(Text_users)
            for num , i in enumerate(more_money , 1):
                user_money = f'\n {num} - 👤 : <code>{str(i.user_id)}</code> : {format(int(i.user_wallet), ",")} تومان'
                users_static_list.append(user_money)
            users_static_list.append('\n.')
            users_static_text = ''.join(users_static_list)
        else :
            users_static_text = 'هنوز آماری برای ارائه وجود ندارد'
        bot.edit_message_text(users_static_text ,  call.message.chat.id , call.message.message_id , reply_markup=BotKb.bot_static(users=True))




    #- bot static - PRODUCTS
    if call.data =='products_static':
        products_ = products.objects
        if products_.all().exists():
            Text_products = f"""
📊- آمار محصولات

── تعداد کل محصولات : {products_.all().count()} عدد
── کمترین قیمت محصول : {format(products_.all().aggregate(Min('pro_cost'))['pro_cost__min'],',')} تومن
── بیشترین قیمت محصول : {format(products_.all().aggregate(Max('pro_cost'))['pro_cost__max'], ',')} تومن
── کمترین حجم محصول : {int(products_.all().aggregate(Min('data_limit'))['data_limit__min'])} گیگ
── بیشترین حجم محصول : {int(products_.all().aggregate(Max('data_limit'))['data_limit__max'])} گیگ

╣ - بیشترین محصولات فروش رفته - 
"""
            product_static_list = []
            product_static_list.append(Text_products)
            
            payments_accpeted_id = [i.inovice_id_id for i in  payments.objects.filter(payment_status= 'accepted' , inovice_id__isnull=False)]
            product_count_name = inovices.objects.filter(id__in = payments_accpeted_id).values('product_name').annotate(Count('product_name'))[:5]
            
            for num,i in enumerate(product_count_name ,1):
                product_sold = f'\n {num}- 🛍 - <code>{i["product_name"]}</code>'
                product_static_list.append(product_sold)
            product_static_list.append('\n.')
            product_static_text = ''.join(product_static_list)
        else:
            product_static_text = 'هنوز اطلاعاتی برای ارائه وجود ندارد'
        bot.edit_message_text(product_static_text , call.message.chat.id , call.message.message_id, reply_markup=BotKb.bot_static(products=True))







    #- bot static - PANELS
    if call.data =='panels_static':
        panels_ = v2panel.objects
        if panels_.all().exists():
            Text_panels = f"""
📊- آمار پنل ها 

── تعداد کل پنل ها :‌ {panels_.all().count()}
── تعداد اشتراک های هر پنل: 
"""
            panel_id = [i.id for i in  v2panel.objects.all()]
            subs_count = subscriptions.objects.filter(panel_id__in = panel_id).values('panel_id').annotate(Count('panel_id'))
            panels_static_list = []
            panels_static_list.append(Text_panels)
            for num ,i in enumerate(subs_count ,1):
                panel_name = v2panel.objects.get(id = i["panel_id"]).panel_name
                panel_sub = f'\n {num}- 🎛 {panel_name} :  {i["panel_id__count"]} عدد'
                panels_static_list.append(panel_sub)
            panels_static_list.append('\n.')
            panels_static_text = ''.join(panels_static_list)
        else:
            panels_static_text = 'هنوز اماری برای ارائه وجود ندارید'
        bot.edit_message_text(panels_static_text , call.message.chat.id , call.message.message_id , reply_markup=BotKb.bot_static(panels=True))





    #- bot static - INOVICES
    if call.data =='inovices_static':
        inovices_ = inovices.objects
        if inovices_.all().exists():
            Text_inovices = f"""
📊- آمار فاکتورها

── تعداد کل فاکتورها صادر شده : {inovices_.aggregate(Count('id'))['id__count']} عدد
── تعداد فاکتورها تمدید شده : {inovices_.filter(kind_pay ='Tamdid').aggregate(Count('id'))['id__count']} عدد
── تعداد فاکتورها اولین خرید  : {inovices_.filter(kind_pay = 'Buy').aggregate(Count('id'))['id__count']} عدد
── کل قیمت فاکتورها صادر شده : {format(int(inovices_.aggregate(Sum('pro_cost'))['pro_cost__sum']) ,',')} تومان
── کل حجم فاکتورها صادر شده : {inovices_.aggregate(Sum('data_limit'))['data_limit__sum']} Gb

╣ - بیشترین محصولات فاکتور شده - 
"""
            inovices_static_list = []
            inovices_static_list.append(Text_inovices)

            most_bought_product = inovices_.values('product_name').annotate(Count('product_name'))
            for num,i in enumerate(most_bought_product , 1):
                prod = f'\n {num}- 🔖 : <code>{i["product_name"]}</code> - {i["product_name__count"]} عدد'
                inovices_static_list.append(prod)

            inovices_static_list.append('\n.')
            invoices_static_text = ''.join(inovices_static_list)
        else :
            invoices_static_text = 'هنوز آماری برای ارائه وجود ندارد '
        bot.edit_message_text(invoices_static_text, call.message.chat.id, call.message.message_id, reply_markup=BotKb.bot_static(inovices=True))



    #- bot static - INOVICES
    if call.data =='payments_static':
        payments_ =payments.objects
        if payments_.all().exists():
            Text_payments = f"""
📊- آمار پرداخت‌ها 

── تعداد کل پرداختی ها  : {payments_.aggregate(Count('id'))['id__count']} عدد
── تعداد کل پرداختی های موفق : {payments_.filter(payment_status ='accepted').aggregate(Count('id'))['id__count']} عدد
── تعداد کل پرداختی های ناموفق  : {payments_.filter(payment_status ='declined').aggregate(Count('id'))['id__count']} عدد
── کل پرداختی های موفق  : {format(int(payments_.filter(payment_status ='accepted').aggregate(Sum('amount'))['amount__sum']), ',')} تومان

.
"""
        else:
            Text_payments = 'هنوز آماری برای ارائه وجود ندارید'
            
            bot.edit_message_text(Text_payments, call.message.chat.id, call.message.message_id , reply_markup=BotKb.bot_static(payments=True))

    if call.data == 'back_from_bot_statics':
        bot.edit_message_text('به مدیریت ربات خوش امدید', call.message.chat.id , call.message.message_id , reply_markup= BotKb.management_menu_in_admin_side(user_id = call.from_user.id))






#---------------------------------------------------------------------------------------------------------------------------------#
# -------------------------bot_management------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------------------#



ADD_BANK_KARD = {'bank_name_stat' : False , 'bank_name' : str ,
                'bank_kart_stat': False , 'bank_kart' : str ,
                'bank_ownername_stat' : False , 'bank_ownername': str}


@bot.callback_query_handler(func= lambda call: call.data in ['bot_managment', 'manage_bank_cards' ,'walletpay_status', 'kartbkart_status','manage_shomare_kart', 'back_to_management_menu', 'back_from_mange_howtopay', 'back_from_manage_shomare_kart', 'back_from_manage_shomare_karts' , 'add_new_kart_number', 'moneyusrtousr_status'] or call.data.startswith(('mkart_' , 'rmkart_', 'chstatus_shomarekart_' , 'userin_pays_')))
def bot_managment_payment(call):
    status_txt = lambda botstatus : '❌غیر فعال' if botstatus == 0 else  '✅فعال'
    
    if call.data == 'bot_managment':
        admins_ = admins.objects.get(user_id = int(call.from_user.id))
        if (admins_.acc_panels == 1 and admins_.acc_botmanagment ==1)or admins_.is_owner ==1:
            bot.edit_message_text('به قسمت تنظیمات ربات خوش امدید ' , call.message.chat.id , call.message.message_id , reply_markup=BotKb.bot_management())
        else :
            bot.send_message(call.message.chat.id , 'شما اجازه دسترسی به این قسمت را ندارید')


    if call.data =='manage_bank_cards':
        Text_2 = 'برای مدیریت کردن نحوه پرداخت از گزینه های زیر استفاده نمایید'
        bot.edit_message_text(Text_2 , call.message.chat.id , call.message.message_id, reply_markup=BotKb.manage_howtopay())


    if call.data =='back_to_management_menu':
        bot.edit_message_text('به مدیریت ربات خوش امدید', call.message.chat.id , call.message.message_id , reply_markup= BotKb.management_menu_in_admin_side(user_id = call.from_user.id))        

    if call.data =='back_from_mange_howtopay':
        bot.edit_message_text('به قسمت تنظیمات ربات خوش امدید' , call.message.chat.id , call.message.message_id , reply_markup=BotKb.bot_management())
    


    if call.data =='walletpay_status':
        botsettings_ = botsettings.objects.all()
        for i in botsettings_:
            new_wallet_pay = 1 if i.wallet_pay == 0 else 0
            i.wallet_pay = new_wallet_pay
            i.save()
        Text_3 = f'برای مدیریت کردن نحوه پرداخت از گزینه های زیر استفاده نمایید \n وضعیت پرداخت با کیف پول تغییر کرد \n وضعیت فعلی : {status_txt(i.wallet_pay)}'
        bot.edit_message_text(Text_3, call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_howtopay())


    if call.data =='kartbkart_status':
        botsettings_ = botsettings.objects.all()
        for i in botsettings_:
            new_kartbkart_pay = 1 if i.kartbkart_pay == 0 else 0
            i.kartbkart_pay = new_kartbkart_pay
            i.save()
        Text_3 = f'برای مدیریت کردن نحوه پرداخت از گزینه های زیر استفاده نمایید \n وضعیت پرداخت با کارت به کارت تغییر کرد \n وضعیت فعلی : {status_txt(i.kartbkart_pay)}'
        bot.edit_message_text(Text_3, call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_howtopay())


    if call.data == 'moneyusrtousr_status':
        botsettings_ = botsettings.objects.all()
        for i in botsettings_:
            new_kartbkart_pay = 1 if i.moneyusrtousr == 0 else 0
            i.moneyusrtousr = new_kartbkart_pay
            i.save()
        Text_3 = f'برای مدیریت کردن نحوه پرداخت از گزینه های زیر استفاده نمایید \n وضعیت انتقال وجه یوزر به یوزر تغییر کرد \n وضعیت فعلی : {status_txt(i.moneyusrtousr)}'
        bot.edit_message_text(Text_3, call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_howtopay())




    if call.data =='manage_shomare_kart':
        Text_4='به قسمت مدیریت کردن شماره کارت ها خوش امدید'
        bot.edit_message_text(Text_4 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_shomarekart())



    if call.data.startswith('mkart_'):
        call_data = call.data.split('_')
        shomarekart_ = shomarekart.objects.get(bank_card= call_data[-1])
        use_status = 'عدم استفاده' if shomarekart_.bank_inmsg == 0 else 'در حال استفاده'
        Text_5 = f"""
┐ - وضعیت کارت :‌ {status_txt(shomarekart_.bank_status)}

 ┊─ نام صاحب کارت : {shomarekart_.ownername}
 ┊─  نام بانک کارت : {shomarekart_.bank_name}
 ┊─ شماره کارت : {shomarekart_.bank_card}

┘ - وضعیت استفاده : {use_status}
.
"""
        bot.edit_message_text(Text_5 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_kart(call_data[-1]))



    if call.data.startswith('userin_pays_'):
        call_data = call.data.split('_')
        shomarekart_bank_inuse_false = shomarekart.objects.filter(bank_inmsg = 1).exclude(bank_card = call_data[-1]).all()
        for i in shomarekart_bank_inuse_false:
            i.bank_inmsg = 0
            i.save()
        shomarekart_ = shomarekart.objects.get(bank_card= call_data[-1])
        new_use_status = 1 if shomarekart_.bank_inmsg == 0 else 0
        shomarekart_.bank_inmsg = new_use_status
        shomarekart_.save()

        use_status = 'عدم استفاده' if shomarekart_.bank_inmsg == 0 else 'در حال استفاده'
        Text_5 = f"""
┐ - وضعیت کارت :‌ {status_txt(shomarekart_.bank_status)}

 ┊─ نام صاحب کارت : {shomarekart_.ownername}
 ┊─  نام بانک کارت : {shomarekart_.bank_name}
 ┊─ شماره کارت : {shomarekart_.bank_card}

┘ - وضعیت استفاده : {use_status}
.
"""
        bot.edit_message_text(Text_5 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_kart(call_data[-1]))




    if call.data.startswith('rmkart_'):
        call_data = call.data.split('_')
        shomarekart_ = shomarekart.objects.get(bank_card= call_data[-1]).delete()
        Text_5='به قسمت مدیریت کردن شماره کارت ها خوش امدید'
        bot.edit_message_text(Text_5 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_shomarekart())




    if call.data.startswith('chstatus_shomarekart_'):
        call_data = call.data.split("_")
        shomarekart_ = shomarekart.objects.get(bank_card= call_data[-1])
        new_shomarekart_status = 1 if shomarekart_.bank_status == 0 else 0
        shomarekart_.bank_status = new_shomarekart_status
        shomarekart_.save()
        use_status = 'عدم استفاده' if shomarekart_.bank_inmsg == 0 else 'در حال استفاده'
        Text_6 = f"""
┐ - وضعیت کارت :‌ {status_txt(shomarekart_.bank_status)}

 ┊─ نام صاحب کارت : {shomarekart_.ownername}
 ┊─  نام بانک کارت : {shomarekart_.bank_name}
 ┊─ شماره کارت : {shomarekart_.bank_card}

┘ - وضعیت استفاده : {use_status}
.
"""
        bot.edit_message_text(Text_6 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_kart(call_data[-1]))




    if call.data == 'back_from_manage_shomare_kart':
        Text_back_1='به قسمت مدیریت کردن شماره کارت ها خوش امدید'
        bot.edit_message_text(Text_back_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_shomarekart())


    if call.data =='back_from_manage_shomare_karts':
        Text_back_2= 'برای مدیریت کردن نحوه پرداخت از گزینه های زیر استفاده نمایید'
        bot.edit_message_text(Text_back_2 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_howtopay())



    if call.data =='add_new_kart_number':
        ADD_BANK_KARD['bank_name_stat'] = True
        bot.send_message(call.message.chat.id, 'نام بانک را ارسال نمایید')
        






@bot.message_handler(func= lambda message : ADD_BANK_KARD['bank_name_stat']== True or ADD_BANK_KARD['bank_kart_stat']==True or ADD_BANK_KARD['bank_ownername_stat']==True)
def handle_newbank_kard(message):
    if ADD_BANK_KARD['bank_name_stat']== True:
        ADD_BANK_KARD['bank_name'] = message.text
        ADD_BANK_KARD['bank_name_stat'] = False
        ADD_BANK_KARD['bank_kart_stat']=True
        bot.send_message(message.chat.id , 'شماره کارت بانک را ارسال نمایید')
        return


    if ADD_BANK_KARD['bank_kart_stat']== True:
        ADD_BANK_KARD['bank_kart'] = message.text
        ADD_BANK_KARD['bank_kart_stat'] = False
        ADD_BANK_KARD['bank_ownername_stat']= True
        bot.send_message(message.chat.id , 'نام دارنده حساب را ارسال نمایید')
        return



    if ADD_BANK_KARD['bank_ownername_stat']== True:
        ADD_BANK_KARD['bank_ownername'] = message.text
        ADD_BANK_KARD['bank_ownername_stat'] = False
        shomarekart.objects.create(bank_name=ADD_BANK_KARD['bank_name'], bank_card=ADD_BANK_KARD['bank_kart'] , ownername=ADD_BANK_KARD['bank_ownername'] , bank_status=0 , bank_inmsg=0)
        bot.send_message(message.chat.id , 'شماره کارت با موفقیت اضافه شد' , reply_markup=BotKb.manage_shomarekart())
        return








#----------------------------------------------------------------------------------------------------------------------------#
# -------------------------channel management--------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------------#





ADD_NEW_CHANNEL = {'ch_name_stat' : False , 'ch_name' : str ,
                'ch_id_stat': False , 'ch_id' : str ,}


# force join channel 
@bot.callback_query_handler(func= lambda call : call.data in ['manage_force_channel_join' , 'forcechjoin' ,'manage_forcejoin', 'back_from_manage_force_ch' , 'back_from_managing_force_ch' , 'back_from_manage_channel' , 'add_new_force_channel'] or call.data.startswith(('mfch_' , 'status_chf_' , 'rm_chf_')))
def manage_bot_join_ch(call):
    status_txt = lambda botstatus : '❌غیر فعال' if botstatus == 0 else  '✅فعال'

    if call.data == 'manage_force_channel_join':
        Text_1 = f'به قسمت مدیریت جوین اجباری خوش امدید'
        bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_joinch())


    if call.data == 'forcechjoin':
        botsettings_ = botsettings.objects.all()
        for i in botsettings_:
            new_status = 1 if i.forcechjoin == 0 else 0 
            i.forcechjoin = new_status
            i.save()
        Text_2 = f'به قسمت مدیریت جوین اجباری خوش امدید \n\n وضعیت جوین اجباری :‌{status_txt(i.forcechjoin)}'
        bot.edit_message_text(Text_2 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_joinch())



    if call.data =='back_from_manage_force_ch':
        Text_back_1 = 'به قسمت تنظیمات ربات خوش امدید' 
        bot.edit_message_text(Text_back_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.bot_management())




    if call.data =='back_from_managing_force_ch':
        Text_back_2 = f'به قسمت مدیریت جوین اجباری خوش امدید'
        bot.edit_message_text(Text_back_2 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_joinch())



    if call.data == 'manage_forcejoin':
        Text_3 = f'به مدیریت چنل ها خوش امدید \n چنلی را که میخواهید مدیریت کنید را انتخاب نمایید'
        bot.edit_message_text(Text_3 , call.message.chat.id , call.message.message_id , reply_markup=botkb.manage_channels())




    if call.data.startswith('mfch_'):
        call_data = call.data.split('_')
        channels_ = channels.objects.get(id = int(call_data[-1]))
        Text_4 = f"""
┐ - وضعیت چنل :‌ {status_txt(channels_.ch_status)}

 ┊─ نام چنل : {channels_.channel_name}
 ┊─   ادرس چنل : {channels_.channel_url or channels_.channel_id}

.
"""
        bot.edit_message_text(Text_4 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_ch(channel_id= int(call_data[-1])))




    if call.data.startswith('status_chf_'):
        call_data = call.data.split("_")
        channels_ = channels.objects.get(id = int(call_data[-1]))
        new_status = 1 if channels_.ch_status == 0 else 0 
        channels_.ch_status = new_status
        channels_.save()
        Text_4 = f"""
┐ - وضعیت چنل :‌ {status_txt(channels_.ch_status)}

 ┊─ نام چنل : {channels_.channel_name}
 ┊─   ادرس چنل : {channels_.channel_url or channels_.channel_id}

.
"""
        bot.edit_message_text(Text_4 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_ch(channel_id= int(call_data[-1])))

 


    if call.data.startswith('rm_chf_'):
        call_data = call.data.split('_')
        try :
            channels_ = channels.objects.get(id = int(call_data[-1])).delete()
        except Exception as rm_ch_error:
            print(f'error during remove channel \n error msg : {rm_ch_error}')
        Text_5 = f'به مدیریت چنل ها خوش امدید \n چنلی را که میخواهید مدیریت کنید را انتخاب نمایید'
        bot.edit_message_text(Text_5 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_channels())



    if call.data =='back_from_manage_channel':
        Text_back_3 = f'به مدیریت چنل ها خوش امدید \n چنلی را که میخواهید مدیریت کنید را انتخاب نمایید'
        bot.edit_message_text(Text_back_3 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_channels())


    if call.data =='add_new_force_channel':
        ADD_NEW_CHANNEL['ch_name_stat'] = True
        bot.send_message(call.message.chat.id , 'یک نام دلخواه برای چنل انتخاب کنید')


@bot.message_handler(func= lambda message : ADD_NEW_CHANNEL['ch_name_stat']==True or ADD_NEW_CHANNEL['ch_id_stat']==True)
def handle_add_ch(message):
    if ADD_NEW_CHANNEL['ch_name_stat']==True:
        ADD_NEW_CHANNEL['ch_name_stat'] = False
        ADD_NEW_CHANNEL['ch_id_stat'] = True
        ADD_NEW_CHANNEL['ch_name'] = message.text
        bot.send_message(message.chat.id , ' ایدی یا یوزر نیم کانال را بدون @ ارسال نمایید')
        return 
    

    if ADD_NEW_CHANNEL['ch_id_stat']==True :
        ADD_NEW_CHANNEL['ch_id_stat'] = False 
        if message.text.isdigit() or message.text.startswith('-'):
            try :
                channels_ = channels.objects.create(channel_name = ADD_NEW_CHANNEL['ch_name'] , channel_id = message.text , ch_status =0)
            except Exception as error_adding_chid :
                print(f'error during adding new ch \n error msg : {error_adding_chid}')
            bot.send_message(message.chat.id , 'چنل جدید با موفقیت اضافه شد' , reply_markup=botkb.manage_channels())
        else:
            try :
                channels_ = channels.objects.create(channel_name = ADD_NEW_CHANNEL['ch_name'] , channel_url = f"@{message.text}" , ch_status =0)
            except Exception as error_adding_churl :
                print(f'error during adding new ch \n error msg : {error_adding_churl}')
            bot.send_message(message.chat.id , 'چنل جدید با موفقیت اضافه شد' , reply_markup=botkb.manage_channels())
        return





#----------------------------------------------------------------------------------------------------------------------------#
# -------------------------user-increase-decrease-cash management------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------------#





USER_INCREASE_DECREASE_CASH = {}

def operating():
    OPERATION_INCREASE_DECREASE  = {'get_username' : False, 'operator': None , 'amount' : None , 'current_cash': None ,
                                    'verfiy_message': None , 'amount_wish': False ,
                                    'operating': False, 'user_id' : int  }
    return OPERATION_INCREASE_DECREASE


@bot.callback_query_handler(func= lambda call : call.data in ['users_management', 'back_from_user_management', 'increase_decrease_cash', 'back_from_increase_decrease_cash', 'ir_number'])
def manage_users(call):

    if call.data =='users_management':
        admins_ = admins.objects.get(user_id = int(call.from_user.id))
        if (admins_.acc_panels == 1 and admins_.acc_users == 1) or admins_.is_owner ==1:
            Text_1 = 'به قسمت مدیریت یوزر ها خوش امدید'
            bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_users())
        else :
            bot.send_message(call.message.chat.id , 'شما اجازه دسترسی به این قسمت را ندارید')



    if call.data =='back_from_user_management':
        Text_back = 'به مدیریت ربات خوش امدید'
        bot.edit_message_text(Text_back , call.message.chat.id , call.message.message_id , reply_markup=BotKb.management_menu_in_admin_side(call.from_user.id))



    if call.data == 'increase_decrease_cash':
        USER_INCREASE_DECREASE_CASH[call.from_user.id] = operating()
        USER_INCREASE_DECREASE_CASH[call.from_user.id]['get_username'] = True
        bot.edit_message_text('ایدی عددی یوزر مورد نظر را وارد کنید\n\n TO CANCEL : /cancel', call.message.chat.id , call.message.message_id)



    if call.data == 'back_from_increase_decrease_cash':
        clear_dict(USER_INCREASE_DECREASE_CASH , call.from_user.id)
        bot.edit_message_text('به قسمت مدیریت یوزر ها خوش امدید' , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_users())


    if call.data == 'ir_number':
        botsettings_ = botsettings.objects.all()
        for irnumber in botsettings_:
            new_irnumber = 1 if  irnumber.irnumber == 0 else 0
            irnumber.irnumber = new_irnumber
            irnumber.save()
        bot.edit_message_text('به قسمت مدیریت یوزر ها خوش امدید' , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_users())








@bot.message_handler(func= lambda message : message.from_user.id in USER_INCREASE_DECREASE_CASH and USER_INCREASE_DECREASE_CASH[message.from_user.id]['get_username'] == True or  message.from_user.id in USER_INCREASE_DECREASE_CASH and USER_INCREASE_DECREASE_CASH[message.from_user.id]['amount_wish'] == True)
def handle_user_increase_decrease_cash(message):

    if USER_INCREASE_DECREASE_CASH[message.from_user.id]['get_username'] == True:
        if message.text == '/cancel' or message.text == '/cancel'.upper():
            clear_dict(USER_INCREASE_DECREASE_CASH , message.from_user.id)
            bot.send_message(message.chat.id , 'عملیات لغو شد' , reply_markup=BotKb.manage_users())
        else:
            if message.text.isdigit():
                try : 
                    users_ = users.objects.get(user_id = int(message.text))
                    if users_:
                        USER_INCREASE_DECREASE_CASH[message.from_user.id]['get_username'] = False
                        USER_INCREASE_DECREASE_CASH[message.from_user.id]['user_id'] = int(message.text)
                        USER_INCREASE_DECREASE_CASH[message.from_user.id]['operating'] = True
                        Text_1 = f'''
عمل انتخابی خود را انتخاب نمایید 

👤: <code> {str(users_.user_id)} </code>
 ┊─  نام کاربری :‌{str(users_.first_name) } {str(users_.last_name)}
 ┊─  یوزر نیم : @{str(users_.username)}
 ┊─ موجودی کیف پول : {str(format(int(users_.user_wallet) , ','))}

.
'''
                        bot.send_message( message.chat.id , Text_1 , reply_markup=BotKb.increase_or_decrease(user_id=int(message.from_user.id)))
                except users.DoesNotExist:
                    USER_INCREASE_DECREASE_CASH[message.from_user.id]['get_username'] = False
                    bot.send_message(message.chat.id , 'یوزری با این ایدی یافت نشد')
            else:
                bot.send_message(message.chat.id , 'ایدی وارد شده باید به صورت عدد باشد')
        return




    if USER_INCREASE_DECREASE_CASH[message.from_user.id]['amount_wish'] ==True:
        if message.text.isdigit():
            USER_INCREASE_DECREASE_CASH[message.from_user.id]['amount_wish'] = False
            USER_INCREASE_DECREASE_CASH[message.from_user.id]['current_cash'] = int(message.text)
            users_ = users.objects.get(user_id = USER_INCREASE_DECREASE_CASH[message.from_user.id]['user_id'])
            Text_2 = f'''
عمل انتخابی خود را انتخاب نمایید 

👤: <code> {str(users_.user_id)} </code>
 ┊─  نام کاربری :‌{str(users_.first_name) } {str(users_.last_name)}
 ┊─  یوزر نیم : @{str(users_.username)}
 ┊─ موجودی کیف پول : {str(format(int(users_.user_wallet) , ','))}

.
'''
            op = "➕" if USER_INCREASE_DECREASE_CASH[message.from_user.id]['operator'] =='➕'  else '➖' if USER_INCREASE_DECREASE_CASH[message.from_user.id]['operator']=='➖' else None
            
            current_cash = USER_INCREASE_DECREASE_CASH[message.from_user.id]['current_cash']  if USER_INCREASE_DECREASE_CASH[message.from_user.id]['current_cash'] is not None else '5000'

            bot.send_message(message.chat.id , Text_2 , reply_markup=BotKb.increase_or_decrease(user_id= users_.user_id, current_cash= int(current_cash), operator=op , amount_add= 1))
        else:
            bot.send_message(message.chat.id , 'ایدی وارد شده باید به صورت عدد باشد')
        return













@bot.callback_query_handler(func= lambda call : call.data in ['operator_mines' , 'operator_plus' , 'decrease_cash_to','increase_cash_to' , 'back_from_step_increase_decrease' , 'wish_amount'] or call.data.startswith(('amount_decrease' , 'amount_increase','verify_inde_')))
def increase_decrease_cahs(call):
    if call.from_user.id in USER_INCREASE_DECREASE_CASH :
        User_id = USER_INCREASE_DECREASE_CASH[call.from_user.id]['user_id'] 
        users_ = users.objects.get(user_id = int(User_id))
        Text_00 = f'''
عمل انتخابی خود را انتخاب نمایید 

👤: <code> {str(users_.user_id)} </code>
 ┊─  نام کاربری :‌{str(users_.first_name) + str(users_.last_name)}
 ┊─  یوزر نیم : @{str(users_.username)}
 ┊─ موجودی کیف پول : {str(format(int(users_.user_wallet) , ','))}

.
 '''


    if call.data =='operator_mines':
        if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operating'] == True and call.from_user.id in USER_INCREASE_DECREASE_CASH:

            USER_INCREASE_DECREASE_CASH[call.from_user.id]['operator'] = '➖'

            op = "➕" if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operator'] =='➕'  else '➖' if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operator']=='➖' else None
            
            amount = USER_INCREASE_DECREASE_CASH[call.from_user.id]['amount'] if USER_INCREASE_DECREASE_CASH[call.from_user.id] is not None else  int(1)

            current_cash = USER_INCREASE_DECREASE_CASH[call.from_user.id]['current_cash'] if USER_INCREASE_DECREASE_CASH[call.from_user.id]['current_cash'] is not None else '5000'
            
            bot.edit_message_text(Text_00 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.increase_or_decrease(user_id=int(User_id), amount_add= amount, operator=op , current_cash = int(current_cash)))
        else:
            bot.send_message(call.message.chat.id , 'انجام این عملیات برای این یوزر امکان پذیر نمیباشد')





    if call.data =='operator_plus':
        if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operating'] == True  and call.from_user.id in USER_INCREASE_DECREASE_CASH:

            USER_INCREASE_DECREASE_CASH[call.from_user.id]['operator'] = "➕"

            op = "➕" if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operator'] =='➕'  else '➖' if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operator']=='➖' else None
            
            amount = USER_INCREASE_DECREASE_CASH[call.from_user.id]['amount'] if USER_INCREASE_DECREASE_CASH[call.from_user.id] is not None else  int(1)

            current_cash = USER_INCREASE_DECREASE_CASH[call.from_user.id]['current_cash'] if USER_INCREASE_DECREASE_CASH[call.from_user.id]['current_cash'] is not None else '5000'
            
            bot.edit_message_text(Text_00 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.increase_or_decrease(user_id=int(User_id),amount_add= amount, operator=op, current_cash = int(current_cash)))
        
        else:
            bot.send_message(call.message.chat.id , 'انجام این عملیات برای این یوزر امکان پذیر نمیباشد')





    if call.data.startswith('amount_decrease'):
        if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operating'] == True  and call.from_user.id in USER_INCREASE_DECREASE_CASH:

            call_data = call.data.split("_")
            
            USER_INCREASE_DECREASE_CASH[call.from_user.id]['amount'] = int(call_data[-1])
            
            op = "➕" if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operator'] =='➕'  else '➖' if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operator']=='➖' else None
            
            amount = USER_INCREASE_DECREASE_CASH[call.from_user.id]['amount'] if USER_INCREASE_DECREASE_CASH[call.from_user.id]['amount'] is not None else int(call_data[-1])
            
            current_cash = USER_INCREASE_DECREASE_CASH[call.from_user.id]['current_cash'] if USER_INCREASE_DECREASE_CASH[call.from_user.id]['current_cash'] is not None else '5000'
            
            bot.edit_message_text(Text_00 , call.message.chat.id , call.message.message_id , reply_markup= BotKb.increase_or_decrease(user_id=int(User_id), amount_add=amount, operator=op, current_cash=int(current_cash)))
        
        else:
            bot.send_message(call.message.chat.id , 'انجام این عملیات برای این یوزر امکان پذیر نمیباشد')





    if call.data.startswith('amount_increase'):
        if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operating'] == True  and call.from_user.id in USER_INCREASE_DECREASE_CASH:

            call_data = call.data.split("_")

            USER_INCREASE_DECREASE_CASH[call.from_user.id]['amount'] = int(call_data[-1])
            
            op = "➕" if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operator'] =='➕'  else '➖' if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operator']=='➖' else None
            
            amount = USER_INCREASE_DECREASE_CASH[call.from_user.id]['amount'] if USER_INCREASE_DECREASE_CASH[call.from_user.id]['amount'] is not None else int(call_data[-1])
            
            current_cash = USER_INCREASE_DECREASE_CASH[call.from_user.id]['current_cash'] if USER_INCREASE_DECREASE_CASH[call.from_user.id]['current_cash'] is not None else '5000'
            
            bot.edit_message_text(Text_00 , call.message.chat.id , call.message.message_id , reply_markup= BotKb.increase_or_decrease(user_id=int(User_id), amount_add=amount, operator=op, current_cash=int(current_cash)))
        
        else:
            bot.send_message(call.message.chat.id , 'انجام این عملیات برای این یوزر امکان پذیر نمیباشد')








    if call.data.startswith('verify_inde_') :
        if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operating'] == True  and call.from_user.id in USER_INCREASE_DECREASE_CASH :  
            call_data = call.data.split('_')
            USER_INCREASE_DECREASE_CASH[call.from_user.id]['verfiy_message'] = call.data
            amount = format(int(call_data[2]), ',')
            Text_0_2 = f"""
    ┊─ مبلغ : {str(amount)} تومان
به کیف پول شما اضافه شد 
.
"""
            Text_0_3 = f"""
    ┊─ مبلغ : {str(amount)} تومان
به کیف پول شما کسر شد 
.
"""
            if call_data[3] == 'None':
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton(text='اضافه کردن وجه', callback_data='increase_cash_to') , InlineKeyboardButton(text='کم کردن وجه' , callback_data='decrease_cash_to') , InlineKeyboardButton(text='بازگشت', callback_data='back_from_step_increase_decrease') ,row_width=1)
                bot.edit_message_text('عملیات را انتخاب نمایید', call.message.chat.id , call.message.message_id , reply_markup=keyboard)
            

            if call_data[3] =='plus':
                USER_INCREASE_DECREASE_CASH[call.from_user.id]['operating'] = False
                try :
                    user_ = users.objects.get(user_id = int(call_data[4]))
                    new_wallet = user_.user_wallet + decimal.Decimal(call_data[2])
                    user_.user_wallet = new_wallet
                    user_.save()
                    bot.send_message(call.message.chat.id , 'مبلغ به کیف پول یوزر اضافه شد')
                    bot.send_message(int(call_data[-1]) , Text_0_2)
                    clear_dict(USER_INCREASE_DECREASE_CASH ,call.from_user.id)
                except Exception as error_increase_cash :
                    print(f'error : {error_increase_cash}')


            if call_data[3] == 'mines':
                USER_INCREASE_DECREASE_CASH[call.from_user.id]['operating'] = False
                try :
                    user_ = users.objects.get(user_id = int(call_data[4]))
                    if user_.user_wallet < 0 :
                        bot.send_message(call.message.chat.id , 'موجودی کیف پول مقصد صفر تومان است')
                    elif user_.user_wallet <= int(call_data[2]):
                        user_.user_wallet = 0 
                        user_.save()
                        bot.send_message(call.message.chat.id , 'موجودی کیف پول مقصد صفر خواهد شد')
                    else:
                        new_wallet = user_.user_wallet - decimal.Decimal(call_data[2])
                        user_.user_wallet = new_wallet
                        user_.save()
                        bot.send_message(call.message.chat.id , 'مبلغ از کیف پول یوزر کسر شد')
                    bot.send_message(int(call_data[-1]) , Text_0_3)
                    clear_dict(USER_INCREASE_DECREASE_CASH , call.from_user.id)
                except Exception as error_decrease_cash :
                    print(f'error : {error_decrease_cash}')
        else:
            bot.send_message(call.message.chat.id , 'انجام این عملیات برای این یوزر امکان پذیر نمیباشد')



    if call.data =='increase_cash_to':
        if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operating'] == True  and call.from_user.id in USER_INCREASE_DECREASE_CASH :  
            call_data = USER_INCREASE_DECREASE_CASH[call.from_user.id]['verfiy_message'].split("_")
            amount = format(int(call_data[2]) , ',')
            Text_0_4 = f"""
    ┊─ مبلغ : {str(amount)} تومان
به کیف پول شما اضافه شد 
    .
    """
            USER_INCREASE_DECREASE_CASH[call.from_user.id]['operating'] = False
            try :
                users_ = users.objects.get(user_id = int(call_data[4]))
                new_wallet = users_.user_wallet + decimal.Decimal(call_data[2])
                users_.user_wallet = new_wallet
                users_.save()
                bot.send_message(call.message.chat.id , 'مبلغ به کیف پول یوزر اضافه شد')
                bot.send_message(int(call_data[-1]) , Text_0_4)
                clear_dict(USER_INCREASE_DECREASE_CASH , call.from_user)
            except Exception as error_next_increase:
                print(f'error : {error_next_increase}')
        else:
            bot.send_message(call.message.chat.id , 'انجام این عملیات برای این یوزر امکان پذیر نمیباشد')



    if call.data =='decrease_cash_to':
        if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operating'] == True  and call.from_user.id in USER_INCREASE_DECREASE_CASH :  
            call_data = USER_INCREASE_DECREASE_CASH[call.from_user.id]['verfiy_message'].split("_")
            amount = format(int(call_data[2]) , ',')
            Text_0_5 = f"""
    ┊─ مبلغ : {str(amount)} تومان
به کیف پول شما کسر شد 
    .
    """
            USER_INCREASE_DECREASE_CASH[call.from_user.id]['operating'] = False
            try :
                user_ = users.objects.get(user_id = int(call_data[4]))
                if user_.user_wallet < 0 :
                    bot.send_message(call.message.chat.id , 'موجودی کیف پول مقصد صفر تومان است')
                elif user_.user_wallet <= int(call_data[2]):
                    user_.user_wallet = 0 
                    user_.save()
                    bot.send_message(call.message.chat.id , 'موجودی کیف پول مقصد صفر خواهد شد')
                else:
                    new_wallet = user_.user_wallet - decimal.Decimal(call_data[2])
                    user_.user_wallet = new_wallet
                    user_.save()
                    bot.send_message(call.message.chat.id , 'مبلغ از کیف پول یوزر کسر شد')
                bot.send_message(int(call_data[-1]) , Text_0_5)
                clear_dict(USER_INCREASE_DECREASE_CASH , call.from_user.id)
            except Exception as error_decrease_cash :
                    print(f'error : {error_decrease_cash}')
        else:
            bot.send_message(call.message.chat.id , 'انجام این عملیات برای این یوزر امکان پذیر نمیباشد')




    if call.data =='back_from_step_increase_decrease':
        clear_dict(USER_INCREASE_DECREASE_CASH , call.from_user.id)
        bot.edit_message_text('به قسمت مدیریت یوزر ها خوش امدید' , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_users())





    if call.data=='wish_amount':
        if USER_INCREASE_DECREASE_CASH[call.from_user.id]['operating'] == True  and call.from_user.id in USER_INCREASE_DECREASE_CASH :  
            
            USER_INCREASE_DECREASE_CASH[call.from_user.id]['amount_wish'] = True
            
            bot.send_message(call.message.chat.id , 'مقدار دل خواه را وارد نمایید')
        
        else:
           
            bot.send_message(call.message.chat.id , 'انجام این عملیات برای این یوزر امکان پذیر نمیباشد')













#----------------------------------------------------------------------------------------------------------------------------#
# -------------------------user-blcok-unblcok-user management----------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------------#

BLOCK_UNBLOCK_USER = {}

def block_unblock_user():
    block_unblock_user_dict = {'get_userid':None, 'user_id':None,'block_unblock':None, 'get_reason':None, 'reason_msg':None }
    return block_unblock_user_dict


@bot.callback_query_handler(func= lambda call: call.data in ['block_unblock_user','back_from_block_unblock'] or call.data.startswith(('block_user_', 'unblock_user_', 'verify_sendmsg_')))
def handle_block_unblock(call):

    if call.data == 'block_unblock_user':
        if call.from_user.id in BLOCK_UNBLOCK_USER :
            clear_dict(BLOCK_UNBLOCK_USER , call.from_user.id)
        BLOCK_UNBLOCK_USER[call.from_user.id] = block_unblock_user()
        BLOCK_UNBLOCK_USER[call.from_user.id]['get_userid'] = True
        Text_1 = 'ایدی عددی کاربری را که میخواهید مسدود یا رفع مسدودی کنید را وارد نمایید\n TO CANCEL : /cancel'
        bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id)

    if call.data == 'back_from_block_unblock':
        clear_dict(BLOCK_OR_UNBLOCK , call.from_user.id)
        Text_0 = 'به قسمت مدیریت یوزر ها خوش امدید'
        bot.edit_message_text(Text_0 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_users())


    if call.data.startswith('block_user_'):
        users_ =users.objects.get(user_id = BLOCK_UNBLOCK_USER[call.from_user.id]['user_id'])
        if users_.block_status == 1 :
            Text_2 = 'یوزر از قبل مسدود میباشد'
            bot.send_message(call.message.chat.id , Text_2 )
        else:
            BLOCK_UNBLOCK_USER[call.from_user.id]['get_reason'] = True
            Text_3 = 'علت مسدودی یوزر را وارد کنید\n TO CANCEL : /cancel'
            bot.edit_message_text(Text_3, call.message.chat.id , call.message.message_id )
            




    if call.data.startswith('unblock_user_'):
        users_ =users.objects.get(user_id = BLOCK_UNBLOCK_USER[call.from_user.id]['user_id'])
        if users_.block_status == 0 :
            Text_4 = 'یوزر از قبل مسدود نمیباشد'
            bot.send_message(call.message.chat.id , Text_4 )
        else:
            BLOCK_UNBLOCK_USER[call.from_user.id]['block_unblock'] = 0
            Text_5 = f"به قسمت مدیریت یوزر ها خوش امدید\n علت مسدودی یوزر دریافت شد\n ایدی یوزر : {BLOCK_UNBLOCK_USER[call.from_user.id]['user_id']}"
            bot.edit_message_text(Text_5 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.block_unblock(user_id=BLOCK_UNBLOCK_USER[call.from_user.id]['user_id'] , unblock=True))




    if call.data.startswith('verify_sendmsg_'):
        try :
            users_ = users.objects.get(user_id = BLOCK_UNBLOCK_USER[call.from_user.id]['user_id'])
            admins_ = admins.objects.filter(user_id = BLOCK_UNBLOCK_USER[call.from_user.id]['user_id'])
            if BLOCK_UNBLOCK_USER[call.from_user.id]['block_unblock'] == 1:
                if admins_.exists :
                    admins_.delete()
                users_.block_status = 1
                users_.block_reason = BLOCK_UNBLOCK_USER[call.from_user.id]['reason_msg']
                users_.save()
                Text_6 = f"شما در ربات مسدود شدید و امکان استفاده از امکانات ربات را نخواهید داشت\n علت مسدودی : {BLOCK_UNBLOCK_USER[call.from_user.id]['reason_msg']}"
                bot.send_message(BLOCK_UNBLOCK_USER[call.from_user.id]['user_id'] ,Text_6 )
            
            else:
                users_.block_status = 0 
                users_.block_reason = None
                users_.save()
                Text_7 = f"شما در ربات رفع انسداد شدید و امکان استفاده از امکانات ربات برای شما میسر شد"
                bot.send_message(BLOCK_UNBLOCK_USER[call.from_user.id]['user_id'] ,Text_7 )

        except Exception as block_unblock_status :
            print(f'error while changing user block_unblock status : error_msg : {block_unblock_status}')
        
        block_status_msg = 'مسدود' if users_.block_status == 1 else 'عدم انسداد'
        Text_8 = f'وضععیت انسداد یوزر تغییر پیدا کرد \n وضعیت فعلی :‌{block_status_msg} '
        bot.send_message(call.message.chat.id , Text_8)
        bot.edit_message_text('به قسمت مدیریت یوزر ها خوش امدید' , call.message.chat.id , call.message.message_id , reply_markup=BotKb.manage_users())
        
        




@bot.message_handler(func= lambda message: (message.from_user.id in BLOCK_UNBLOCK_USER and len(BLOCK_UNBLOCK_USER) >= 1 and (BLOCK_UNBLOCK_USER[message.from_user.id]['get_userid'] ==True or BLOCK_UNBLOCK_USER[message.from_user.id]['get_reason'] == True)))
def handle_block_unblock_userid(message):


    if (message.from_user.id in BLOCK_UNBLOCK_USER and len(BLOCK_UNBLOCK_USER) >= 1 and BLOCK_UNBLOCK_USER[message.from_user.id]['get_userid'] ==True):
        if message.text =='/cancel' or message.text == '/cancel'.upper():
            clear_dict(BLOCK_UNBLOCK_USER , message.from_user.id)
            Text_1 = 'به قسمت مدیریت یوزر ها خوش امدید'
            bot.send_message(message.chat.id , Text_1 , reply_markup=BotKb.manage_users())
        else:
            if message.text.isdigit():
                try :
                    users_ = users.objects.get(user_id = int(message.text))
                    BLOCK_UNBLOCK_USER[message.from_user.id]['get_userid'] = False
                    BLOCK_UNBLOCK_USER[message.from_user.id]['user_id'] = int(message.text)
                    Text_2 = f"برای اعمال محدودیت از منوی زیر اقدام نمایید\n ایدی یوزر : {BLOCK_UNBLOCK_USER[message.from_user.id]['user_id']}"
                    bot.send_message(message.chat.id , Text_2 , reply_markup=BotKb.block_unblock(user_id=BLOCK_UNBLOCK_USER[message.from_user.id]['user_id']))
                
                except users.DoesNotExist as user_doesnot_exist:
                    clear_dict(BLOCK_UNBLOCK_USER , message.from_user.id)
                    bot.send_message(message.chat.id , 'کاربری با این ایدی عددی یافت نشد')
            else:
                Text_3 = 'مقدار ارسالی باید به صورت عددی باشد'
                clear_dict(BLOCK_UNBLOCK_USER , message.from_user.id)
                bot.send_message(message.chat.id , Text_3)
        return



    if (message.from_user.id in BLOCK_UNBLOCK_USER and len(BLOCK_UNBLOCK_USER) >= 1 and BLOCK_UNBLOCK_USER[message.from_user.id]['get_reason'] ==True):
        if message.text =='/cancel' or message.text =='/cancel'.upper():
            clear_dict(BLOCK_UNBLOCK_USER , message.from_user.id)
            Text_4 = 'به قسمت مدیریت یوزر ها خوش امدید'
            bot.send_message(message.chat.id, Text_4, reply_markup=BotKb.manage_users())
        else:
            BLOCK_UNBLOCK_USER[message.from_user.id]['get_reason'] = False
            BLOCK_UNBLOCK_USER[message.from_user.id]['reason_msg'] = str(message.text)
            BLOCK_UNBLOCK_USER[message.from_user.id]['block_unblock'] = 1
            Text_5 = f"به قسمت مدیریت یوزر ها خوش امدید\n علت مسدودی یوزر دریافت شد\n ایدی یوزر : {BLOCK_UNBLOCK_USER[message.from_user.id]['user_id']}\n علت مسدودی : {BLOCK_UNBLOCK_USER[message.from_user.id]['reason_msg']}"
            bot.send_message(message.chat.id , Text_5, reply_markup=BotKb.block_unblock(user_id=BLOCK_UNBLOCK_USER[message.from_user.id]["user_id"] , block=True))
        return



#----------------------------------------------------------------------------------------------------------------------------#
# -------------------------Send-msg-to-users management----------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------------#

# //TODO add table boardcasting for sending boardcasting to all users 
# //TODO add feature to cancel sending boardcasting 
# //TODO add feature to get accept or reject keyboard for forwarding msgs
# //TODO add feature to send msg to users who  have not account or had accounts or having at least one account


SIND_SINGLE_MSG = {'get_userid':False ,'get_msg':False, 'user_id': False}

BOARDCATING = {'send_boardcating_state_one': False , 'send_boardcating_state_two':False , 'msg_to_store':None , 'admin_requested':None,
               'forward_boardcating_state_one': False , 'forward_boardcating_state_two':False}

@bot.callback_query_handler(func= lambda call: call.data in ['send_msgs_to_users', 'send_msg_single_user', 'send_msg_boardcasting','send_msg_forwarding', 'back_from_send_msg'])
def handle_sending_users_msg(call):
    if call.data =='send_msgs_to_users':
        Text_1 = 'برای ارسال پیام به کاربران از گزینه های زیر استفاده نمایید'
        bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id, reply_markup=BotKb.send_user_msg())


    if call.data =='send_msg_single_user':
        Text_2 = '🆔ایدی عددی شخصی را که میخواهید پیام بدهید را ارسال نمایید\n TO CANCEL : /CANCEL'
        SIND_SINGLE_MSG['get_userid']=True
        bot.edit_message_text(Text_2, call.message.chat.id , call.message.message_id)



    if call.data =='send_msg_boardcasting':
        BOARDCATING['send_boardcating_state_one'] = True
        Text_3 = 'متنی را که میخواهید برای تمام اعضای ربات بفرستید را ارسال نمیایید\n TO CANCEL : /CANCEL'
        bot.edit_message_text(Text_3, call.message.chat.id , call.message.message_id)

    if call.data =='send_msg_forwarding':
        BOARDCATING['forward_boardcating_state_one'] = True
        Text_4 = ' متنی را که میخواهید برای تمام اعضای ربات فوروارد نمیایید را ارسال نمایید \n ⚠️ با ارسال پیام عمل فوروارد کردن درجا آغاز میشود\n TO CANCEL : /CANCEL'
        bot.edit_message_text(Text_4, call.message.chat.id , call.message.message_id)


    if call.data =='back_from_send_msg':
        bot.edit_message_text('برای ارسال پیام به کاربران از گزینه های زیر استفاده نمایید', call.message.chat.id, call.message.message_id, reply_markup=BotKb.send_user_msg())





@bot.message_handler(func= lambda message: SIND_SINGLE_MSG['get_userid']==True or SIND_SINGLE_MSG['get_msg'] == True or BOARDCATING['send_boardcating_state_one'] == True or BOARDCATING['forward_boardcating_state_one'] == True , content_types=['text','photo','video'])
def handle_single_msg(message):

    if SIND_SINGLE_MSG['get_userid'] == True:
        if message.text == '/cancel' or message.text =='/cancel'.upper():
            SIND_SINGLE_MSG.update({key : False for key in SIND_SINGLE_MSG.keys()})
            bot.send_message(message.chat.id, 'برای ارسال پیام به کاربران از گزینه های زیر استفاده نمایید', reply_markup=BotKb.send_user_msg())
        else:
            if message.text.isdigit():
                    user_ = users.objects.get(user_id = int(message.text))
                    if  user_:
                        SIND_SINGLE_MSG['get_userid'] = False
                        SIND_SINGLE_MSG['get_msg'] = True
                        SIND_SINGLE_MSG['user_id'] = message.text
                        bot.send_message(message.chat.id, '📝متن پیام خود را برای ارسال به کاربر مورد نظر ارسال فرمایید\n TO CANCEL : /CANCEL')
                    else:
                        bot.send_message(message.chat.id , 'کاربری با این نام کاربری پیدا نشد')
            else:
                bot.send_message(message.chat.id , 'فقط ایدی عددی مجاز میباشد')
            return


    if SIND_SINGLE_MSG['get_msg'] == True:
        if message.text == '/cancel' or message.text =='/cancel'.upper():
            SIND_SINGLE_MSG.update({key : False for key in SIND_SINGLE_MSG.keys()})
            bot.send_message(message.chat.id, 'برای ارسال پیام به کاربران از گزینه های زیر استفاده نمایید', reply_markup=BotKb.send_user_msg())
        else:
            admins_ = admins.objects
            admin_info = admins_.get(user_id = message.from_user.id)
            Text_1 = f'📧شما یک پیام دریافت کردید\nمتن پیام :\n {message.text}\n'
            Text_2 = '✅ پیام شما با موفقیت ارسال گردید'
            
            bot.send_message(SIND_SINGLE_MSG['user_id'] , Text_1)
            bot.send_message(message.chat.id , Text_2)

            if admin_info.is_admin:
                owner_id = admins_.filter(is_owner =1).values('user_id')[0]['user_id']
                owner_msg_single_user_msg = f'یک پیام برای کاربر : {SIND_SINGLE_MSG["user_id"]} \n از طرف ادمین : {admin_info.user_id} با نام {admin_info.admin_name} \nارسال شد'
                bot.send_message(owner_id , owner_msg_single_user_msg)
                
            bot.send_message(message.chat.id, 'برای ارسال پیام به کاربران از گزینه های زیر استفاده نمایید', reply_markup=BotKb.send_user_msg())

            SIND_SINGLE_MSG.update({key : False for key in SIND_SINGLE_MSG.keys()})
        return



    if BOARDCATING['send_boardcating_state_one'] == True :
        if message.text =='/cancel' or  message.text =='/cancel'.upper():
            BOARDCATING.update({key:False for key in BOARDCATING.keys() if key !='msg_to_store' and key !='admin_requested'})
            bot.send_message(message.chat.id, 'برای ارسال پیام به کاربران از گزینه های زیر استفاده نمایید', reply_markup=BotKb.send_user_msg())
        else:
            admins_ = admins.objects
            BOARDCATING['msg_to_store'] = message.text
            keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('تایید✅',callback_data='verify_send_msg_to_all'),InlineKeyboardButton('لغو و بازگشت ❌',callback_data='cancel_send_msg_to_all'))
            owner_msg = f'🔖درخواست ارسال یک پیام همگانی در ربات ثبت شده است \n متن پیام : {message.text} \n در صورت تایید گزینه ارسال را بزنید در غیر این صورت گزینه لغو را ارسال نمایید'
            request_admin = admins_.get(user_id = message.from_user.id)
            owner_id = admins_.filter(is_owner =1).values('user_id')[0]['user_id']
            if request_admin.is_admin and request_admin.user_id == message.from_user.id:
                bot.send_message(request_admin.user_id, 'درخواست شما ثبت شد پس از تایید به اطلاع شما خواهد رسید')
                bot.send_message(owner_id,owner_msg, reply_markup=keyboard)
                BOARDCATING['admin_requested'] = request_admin.user_id
            else:
                bot.send_message(owner_id ,owner_msg, reply_markup=keyboard)
            BOARDCATING['send_boardcating_state_one'] =False
        return




    if BOARDCATING['forward_boardcating_state_one'] == True :
        
        if message.text =='/cancel' or  message.text =='/cancel'.upper():
            BOARDCATING.update({key:False for key in BOARDCATING.keys() if key !='msg_to_store' and key !='admin_requested'})
            bot.send_message(message.chat.id, 'برای ارسال پیام به کاربران از گزینه های زیر استفاده نمایید', reply_markup=BotKb.send_user_msg())
        else:
            admins_ = admins.objects
            request_admin = admins_.get(user_id = message.from_user.id)
            owner_id = admins_.filter(is_owner =1).values('user_id')[0]['user_id']
            text_msg_status = f'یک پیام همگانی در حال فوروارد برای همه اعضای ربات میباشد '
            if owner_id == message.from_user.id:
                bot.send_message(owner_id ,text_msg_status)
                users_ = users.objects.all()       
                total_user = users_.count()
                i1 = 0
                i2 = 10
                while i1 <= total_user:
                    chunk_size = users_[i1: i1+i2]
                    for x in chunk_size:
                        if x.user_id != owner_id :
                            time.sleep(0.5)
                            bot.forward_message(x.user_id, message.chat.id , message.message_id)
                    i1 += i2
            else:
                bot.send_message(request_admin.user_id, 'شما امکان فوروارد کردن پیام همگانی را ندارید')
            BOARDCATING['forward_boardcating_state_one'] =False
        return



@bot.callback_query_handler(func= lambda call : call.data in ['verify_send_msg_to_all', 'cancel_send_msg_to_all'])
def handle_boradcating(call):
    if call.data == 'verify_send_msg_to_all':
        users_ = users.objects.all()
        owner_id = admins.objects.filter(is_owner =1).values('user_id')[0]['user_id']
        time_to_send = (users_.count() * 0.5) / 60
        text_msg_status = f'یک پیام همگانی در حال ارسال برای همه اعضای ربات میباشد \n متن پیام : \n {BOARDCATING["msg_to_store"]}\n زمان تقریبی برای ارسال : {round(time_to_send,3)} دقیقه'
        if BOARDCATING['admin_requested'] is not None :
            bot.send_message(BOARDCATING['admin_requested'] , ' درخواست شما توسط اونر ربات تایید شد و در حال ارسال برای تمام اعضا میباشد')
            bot.send_message(BOARDCATING['admin_requested'], text_msg_status)

        bot.edit_message_text(text_msg_status, owner_id , call.message.message_id)
        
        
        total_user = users_.count()
        i1 = 0
        i2 = 10
        while i1 <= total_user:
            chunk_size = users_[i1: i1+i2]
            for x in chunk_size:
                if x.user_id != owner_id or x.user_id != admins.objects.filter(is_admin =1).values('user_id')[0]['user_id']:
                    time.sleep(0.5)
                    bot.send_message(x.user_id , BOARDCATING['msg_to_store'])
            i1 += i2
    


    if call.data =='cancel_send_msg_to_all':
        if BOARDCATING['admin_requested'] is not None :
            bot.send_message(BOARDCATING['admin_requested'] ,'درخواست ارسال پیام همگانی شما رد شد', reply_markup=BotKb.send_user_msg())
        bot.send_message(call.message.chat.id ,'ارسال پیام همگانی لغو گردید' , reply_markup=BotKb.send_user_msg())
        BOARDCATING.update({key : False  for key in BOARDCATING.keys() if key !='msg_to_store' and key !='admin_requested' })
        print(BOARDCATING)























"""

# this used to import django in to the code / scripting runing
import django 
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'TeleBot.settings'
django.setup()
prrint('Configured')


"""
@bot.callback_query_handler(func= lambda call : call.data)
def check_call(call):
    print(call.data)



