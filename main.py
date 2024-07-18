import telebot
from telebot.types import InlineKeyboardMarkup , InlineKeyboardButton 
from mainrobot.models import users , admins , v2panel , products , inovices , payments , channels , subscriptions
from keybuttons import BotkeyBoard as BotKb
import string , random , re , decimal , json  
from functions.USERS_onstarts import *
from functions.PANEL_managing import *
from functions.PRODUCTS_managing import *
from functions.BUY_services import * 
from functions.check_fun import *
from BOTTOKEN import TOKEN
from tools import QRcode_maker
from bottext import *
import panelsapi

bot = telebot.TeleBot(token=TOKEN  , parse_mode="HTML" , colorful_logs= True)



#//TODO add feature of spliting text msg\'s 
#//TODO add /add_panel to the text if theres no plan for first time
#//TODO add charge wallet message in admin side section





#= Welcomer
@bot.message_handler(func=lambda message: '/start' in message.text)
def start_bot(message) :
    user_ = message.from_user 
    CHECKING_USER = CHECK_USER_EXITENCE(user_.id , user_.first_name , user_.last_name , user_.username , 0 )

    if FORCE_JOIN_CHANNEL(UserId=user_.id , Bot=bot) == True :
        #- Canceling operations : panels , product
        PANEL_RECEIVING_STATE['Enable_Panel_Adding'] = False
        PRODUCT_RECEIVING_STATE['enable_product_adding'] = False
        CHANGING_PANEL_DETAILS.update({key : False for key in CHANGING_PANEL_DETAILS})
        CHNAGING_PRODUCT_DETAILS['Enable_Changing_Product_Deatails'] = False

        if message.from_user.id in marzban_panel_api_user:
            marzban_panel_api_user.pop(message.from_user.id)
        """  
        This is temproraliy in here      
        if message.from_user.id in USERS_BASKET:
            USERS_BASKET.pop(message.from_user.id)

        """        
        bot.send_message(message.chat.id , welcome_msg , reply_markup= BotKb.main_menu_in_user_side(message.from_user.id))

    else :
        bot.send_message(message.chat.id , text=force_channel_join_msg, reply_markup=BotKb.load_channels(bot , user_.id))



#- handles all incoming channels_joined call.data 
@bot.callback_query_handler(func=lambda call : call.data=='channels_joined')
def channels_joined(call):
    if call.data=='channels_joined':
        if FORCE_JOIN_CHANNEL(call.from_user.id , bot) == True:
            bot.edit_message_text(welcome_msg , call.message.chat.id , call.message.message_id , reply_markup= BotKb.main_menu_in_user_side(call.message.from_user.id))
        else:
            Text_1='⚠️شما هنوز در چنل های ما جوین نشده اید⚠️'
            bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.load_channels(bot , call.from_user.id))






# -------------------------BUY SERVICES----------------------------------------------------------------------------------------
#//TODO edit all text in bot.send messsage
#> ./buy_services : selecting all plans if olny have on panel

def create_product_entry():
    return {
        'panel_number': '',
        'product_id': 0,
        'product_name': '',
        'data_limit': '',
        'expire_date': '',
        'pro_cost': '',
        'withcapcity': 0,
        'get_username': False,
        'usernameforacc': '',
        'statement': []}

USERS_BASKET = {}

NUMBER_OF_PANEL_LOADED={'one_panel':False , 'one_panel_id':int ,
                        'two_more_panels':False , 'two_panel_id':int}

@bot.callback_query_handler(func=lambda call:call.data in ['buy_service' , 'back_mainmenu_from_one_panels' ])
def handler_buy_service_one_panel(call):   
    panels_ = v2panel.objects.all()
    panel_id = [i.id for i in panels_]
    #check user is joined or not
    if FORCE_JOIN_CHANNEL(call.from_user.id , bot) == True :

        #check received call.data and panels count
        if  call.data == 'buy_service' and 0 < panels_.count() < 2  : 
            if plans_loading_for_one_panel() == 'panel_disable' :
                bot.send_message(call.message.chat.id , '⌛️پنل در حال بروزرسانی میباشد . لطفا بعدا مراجعه فرمایید')
            else : 
                if isinstance(plans_loading_for_one_panel() , InlineKeyboardMarkup):
                    bot.edit_message_text(buy_service_section_product_msg , call.message.chat.id , call.message.message_id , reply_markup = plans_loading_for_one_panel())      

                    NUMBER_OF_PANEL_LOADED['one_panel'] = True
                    NUMBER_OF_PANEL_LOADED['one_panel_id'] = panel_id[-1]

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
            keyboard = InlineKeyboardMarkup()
            for i in panels_ :
                button = InlineKeyboardButton(text=i.panel_name , callback_data=f'TBSpanel_pk_{str(i.id)}')
                keyboard.add(button)
            button_back_2more = InlineKeyboardButton(text='بازگشت به منو اصلی🔙' , callback_data='back_main_menu_from_2more_panels')
            keyboard.add(button_back_2more)
            bot.edit_message_text(buy_service_section_choosing_panel_msg , call.message.chat.id , call.message.message_id , reply_markup=keyboard)


    else :
        bot.send_message(call.message.chat.id , text=force_channel_join_msg, reply_markup=BotKb.load_channels(bot , call.from_user.id))


        #-back - buttons
    if call.data == 'back_mainmenu_from_one_panels' : 
         bot.edit_message_text( welcome_msg , call.message.chat.id , call.message.message_id , reply_markup = BotKb.main_menu_in_user_side(call.from_user.id))
        





#> ./buy service : two panels buying
@bot.callback_query_handler(func = lambda call : call.data.startswith('TBSpanel_pk_') or  call.data in ['back_main_menu_from_2more_panels' , 'back_to_main_menu_for_two_panels'])
def handle_buy_service_two_panel(call):


    #check user is joined or not
    if FORCE_JOIN_CHANNEL(call.from_user.id , bot) == True :

        if call.data.startswith('TBSpanel_pk_') :
            call_data = call.data.split('_')
            state_panel = plans_loading_for_two_more_panel(panel_pk= call_data[-1])
            if state_panel == 'panel_disable':
                bot.send_message(call.message.chat.id , '⌛️پنل در حال بروزرسانی میباشد . لطفا بعدا مراجعه فرمایید')
            
            else :
                if isinstance(state_panel , InlineKeyboardMarkup) :
                    bot.edit_message_text(buy_service_section_product_msg , call.message.chat.id , call.message.message_id , reply_markup = state_panel)
                    NUMBER_OF_PANEL_LOADED['two_more_panels'] = True
                    NUMBER_OF_PANEL_LOADED['two_panel_id'] = call.data.split('_')[-1]
                    if call.from_user.id not in USERS_BASKET:
                        USERS_BASKET[call.from_user.id] = create_product_entry()

                    USERS_BASKET[call.from_user.id]['panel_number'] =  call.data.split('_')[-1]


            if state_panel == 'sale_closed':
                bot.send_message(call.message.chat.id , '⛔️فروش سرویس بسته میباشد ، بعدا مراجعه فرمایید')

            if  state_panel == 'sale_open_no_capcity':
                bot.send_message(call.message.chat.id , '🪫ظرفیت فروش به اتمام رسیده است . بعدا مراجعه فرمایید')

            if state_panel == 'no_products':
                bot.send_message(call.message.chat.id , '‼️متاسفیم ، هنوز هیچ سرور یا محصولی برای ارائه وجود ندارد')
    else :
        bot.send_message(call.message.chat.id , text=force_channel_join_msg, reply_markup=BotKb.load_channels(bot , call.from_user.id))



    if call.data in  ['back_main_menu_from_2more_panels','back_to_main_menu_for_two_panels']:
        bot.edit_message_text(welcome_msg, call.message.chat.id , call.message.message_id , reply_markup = BotKb.main_menu_in_user_side(call.from_user.id))








#> ./buy_services > selecting products plans
@bot.callback_query_handler(func = lambda call : call.data.startswith('buyservice_'))
def handle_buyService_select_proplan(call) :
    
    if call.data.startswith('buyservice_') :
        USERS_BASKET[call.from_user.id]['get_username'] = True
        call_data = call.data.split("_")
        USERS_BASKET[call.from_user.id]['product_id'] = call_data[1]
        USERS_BASKET[call.from_user.id]['statement'] = [call_data[2] , call_data[3] , call_data[4]] 
        bot.edit_message_text(buy_service_section_choosing_username_msg , call.message.chat.id , call.message.message_id)







#> ./buy_services > get user username 
@bot.message_handler(func=lambda message:(message.from_user.id in USERS_BASKET and len(USERS_BASKET) != 0  and USERS_BASKET[message.from_user.id]['get_username']==True))
def get_username_for_config_name(message):
    
    if USERS_BASKET[message.from_user.id]['get_username']==True:

        pattern = re.fullmatch(r'(\w|\d|\_)+', message.text)
        if pattern:
            users_in_panel=panelsapi.marzban(USERS_BASKET[message.from_user.id]['panel_number']).get_all_users()
            
            if users_in_panel['total'] == 0:
                USERS_BASKET[message.from_user.id]['usernameforacc'] = f'1_{message.text}'


            elif users_in_panel['total'] ==1 :
                for i in users_in_panel['users']:
                    if '_' in i['username']:
                        new_number = i['username'].split("_")[0]
                        if new_number.isdigit() :
                            USERS_BASKET[message.from_user.id]['usernameforacc'] = f'{int(new_number) + 1}_{message.text}'


            elif users_in_panel['total'] >1:
                users_username=  [i['username'] for i in users_in_panel['users']]
                new_number = users_username[-1].split("_")[0]
                if new_number.isdigit() : 
                    USERS_BASKET[message.from_user.id]['usernameforacc'] = f'{int(new_number) + 1}_{message.text}'


            USERS_BASKET[message.from_user.id] ['get_username'] = False

            call_data = USERS_BASKET[message.from_user.id]['product_id']
            product_ = products.objects.get(id = call_data)
            USERS_BASKET[message.from_user.id] ['product_name'] = product_.product_name
            USERS_BASKET[message.from_user.id] ['data_limit'] = product_.data_limit
            USERS_BASKET[message.from_user.id] ['expire_date'] = product_.expire_date
            USERS_BASKET[message.from_user.id] ['pro_cost'] = product_.pro_cost

            keyboard = InlineKeyboardMarkup()
            button_1 = InlineKeyboardButton('✅ تایید محصول ' , callback_data= 'verify_product')
            button_2 = InlineKeyboardButton('↩️ بازگشت ' , callback_data = 'back_from_verfying')
 
            keyboard.add(button_1 , button_2 , row_width = 2)
            bot.send_message(message.chat.id , product_info_msg(USERS_BASKET[message.from_user.id]) , reply_markup=keyboard)
        else : 
            bot.send_message(message.chat.id , '⚠️نام کاربری انتخابی اشتباه است لطفامجدد امتحان فرمایید ')






#> ./buy_services > proccess selected product plan 
@bot.callback_query_handler(func = lambda call : call.data in ['verify_product' , 'pay_with_wallet' , 'pay_with_card' , 'back_from_verfying' , 'back_from_payment'] )
def handle_selected_products(call) : 

    if call.data == 'verify_product' :

        bot.edit_message_text('⚪️ یک روش پرداخت را انتخاب نمایید' , call.message.chat.id , call.message.message_id , reply_markup=BotKb.payby_in_user_side()) 



    #pay wallet
    if call.data == 'pay_with_wallet':
        req =pay_with_wallet(call , bot , USERS_BASKET , NUMBER_OF_PANEL_LOADED)

        if req =='requset_false'  :
            print(f'requset is failed related to the api')
        elif req is None:
            print('due to isuffinet')
        else :
            bot.edit_message_text(paied_msg , call.message.chat.id , call.message.message_id)
            how_to_send(req, int(USERS_BASKET[call.from_user.id]['panel_number']) , bot , call.from_user.id)
            users_ = users.objects.get(user_id = call.from_user.id)
            panels_= v2panel.objects.get(id = USERS_BASKET[call.from_user.id]['panel_number'])
            products_ = products.objects.get(id =USERS_BASKET[call.from_user.id]['product_id'] )
            subscriptions_ = subscriptions.objects.create(user_id = users_ , product_id = products_ , panel_id = panels_ , user_subscription = USERS_BASKET[call.from_user.id]['usernameforacc'])
            USERS_BASKET.pop(call.from_user.id)



    #pay card
    if call.data == 'pay_with_card':
        pay_with_card(call , bot , USERS_BASKET , USER_PAYCARD_FISH)


    #back - buttons
    if call.data == 'back_from_verfying':
        bot.edit_message_text(welcome_msg , call.message.chat.id , call.message.message_id , reply_markup = BotKb.main_menu_in_user_side(call.from_user.id))
        bot.answer_callback_query(call.id , 'ادامه خرید محصول لغو شد')
        USERS_BASKET.pop(call.from_user.id)



    if call.data == 'back_from_payment':
        bot.edit_message_text(welcome_msg , call.message.chat.id , call.message.message_id , reply_markup= BotKb.main_menu_in_user_side(call.from_user.id))
        bot.answer_callback_query(call.id , 'پرداخت لغو شد')
        USERS_BASKET.pop(call.from_user.id)







USER_PAYCARD_FISH = {}



# ./buy_service > seding fish section
@bot.message_handler(func = lambda message : (message.from_user.id in USER_PAYCARD_FISH and len(USER_PAYCARD_FISH) > 0  and USER_PAYCARD_FISH[message.from_user.id]['fish_send']) , content_types=['photo'])
def getting_fish_image(message):

    users_ = users.objects.get(user_id = message.from_user.id)
    admins_ = admins.objects.all()
    inovices_ = inovices.objects
    
    all_user_kbk_inovices = []

    if USER_PAYCARD_FISH[message.from_user.id]['fish_send'] == True :
        for i in inovices_.filter(user_id = users_ , paid_status=2 , paid_mode='kbk').order_by('created_date') : #paid_status =2  / waiting for paying

            all_user_kbk_inovices.append(i.id)


        
        if check_time_passed(all_user_kbk_inovices[-1]) == 'time_passed':
            update_inovice_status = inovices_.get(id = int(all_user_kbk_inovices[-1]))   
            update_inovice_status.paid_status = 0 # paid_status = 0 / unpaid due to passing time
            update_inovice_status.save()
            bot.send_message(message.chat.id , inovice_time_passed_msg)

        else :
            panel_id = NUMBER_OF_PANEL_LOADED['one_panel_id'] if NUMBER_OF_PANEL_LOADED['one_panel'] == True else NUMBER_OF_PANEL_LOADED['two_panel_id']
            panel_name = v2panel.objects.get(id = panel_id).panel_name
            user_info = users.objects.get(user_id = message.from_user.id)  
            for i in admins_:
                    bot.send_photo(i.user_id , message.photo[-1].file_id , caption = send_user_buy_request_to_admins(USERS_BASKET[message.from_user.id] ,user_info , panel_name ) , reply_markup= BotKb.agree_or_disagree(message.from_user.id))
            bot.send_message(message.chat.id ,send_success_msg_to_user)

        USER_PAYCARD_FISH[message.from_user.id]['accpet_or_reject'] = True










@bot.callback_query_handler(func = lambda call : call.data.startswith('agree_') or call.data.startswith('disagree_') )
def agree_or_disagree_kbk_payment(call):
    
    call_data = call.data.split('_')
    user_basket = USERS_BASKET[int(call_data[1])]
    if call.data.startswith('agree_')  and (int(call_data[1]) in USER_PAYCARD_FISH and len(USER_PAYCARD_FISH) >=1 and  USER_PAYCARD_FISH[int(call_data[1])]['accpet_or_reject']) == True:

                inovices_ = inovices.objects.all().filter(user_id=call_data[1]).order_by('created_date').last()
                inovices_.paid_status = 1
                inovices_.save()


                users_ = users.objects.get(user_id = call_data[1])
                inovivces2_ = inovices.objects.filter(user_id =users_).latest('created_date')
                payments_ = payments.objects.create(user_id = users_ , amount = user_basket['pro_cost']  ,payment_stauts = 'accepted' , inovice_id = inovivces2_)

                if NUMBER_OF_PANEL_LOADED['one_panel'] == True :
                        if  ('open' and 'withcapcity') or ('zarfit' and 'withcapcity') in user_basket['statement'] :
                            check_capcity(NUMBER_OF_PANEL_LOADED['one_panel_id'])
                else :
                    if NUMBER_OF_PANEL_LOADED['two_more_panels'] == True :
                        if  ('open' and 'withcapcity') or ('zarfit' and 'withcapcity') in user_basket['statement']:
                            check_capcity(NUMBER_OF_PANEL_LOADED['two_panel_id'])
                
                bot.send_message(call.message.chat.id , f'درخواست پرداخت یوزر : {call.message.chat.id} انجام شد')
                bot.send_message(call.data.split('_')[1] , paied_msg)
                send_request = panelsapi.marzban(user_basket['panel_number']).add_user(user_basket['usernameforacc'] , user_basket['product_id'] )
                how_to_send(send_request , user_basket['panel_number'] , bot , int(call_data[1]))

                users_ = users.objects.get(user_id = int(call_data[1]))
                panels_= v2panel.objects.get(id = USERS_BASKET[int(call_data[1])]['panel_number'])
                products_ = products.objects.get(id =USERS_BASKET[int(call_data[1])]['product_id'] )
                subscriptions_ = subscriptions.objects.create(user_id = users_ , product_id = products_ , panel_id = panels_ , user_subscription = USERS_BASKET[int(call_data[1])]['usernameforacc'])
                
                USERS_BASKET.pop(int(call_data[1]))
                USER_PAYCARD_FISH.pop(int(call_data[1]))




    if call.data.startswith('disagree_')  and (int(call_data[1]) in USER_PAYCARD_FISH and len(USER_PAYCARD_FISH) >=1 and  USER_PAYCARD_FISH[int(call_data[1])]['accpet_or_reject']) == True:
            users_ = users.objects.get(user_id = call_data[1])
            inovices_ = inovices.objects.all().filter(user_id=users_).order_by('created_date').last()
            inovices_.paid_status = 3
            inovices_.save()

            inovivces2_ = inovices.objects.filter(user_id =users_).latest('created_date')
            payments_ = payments.objects.create(user_id = users_ , amount = user_basket['pro_cost'] ,payment_stauts = 'declined' , inovice_id = inovivces2_)

            bot.send_message(call.message.chat.id , 'علت رد پرداخت را ارسال کنید')
            if int(call_data[1])  not in payment_decline_reason_2 :
                payment_decline_reason_2[int(call_data[1])] = payment_decline_reason_create()

            payment_decline_reason_2[int(call_data[1])]['reason'] = True
            payment_decline_reason_2[int(call_data[1])]['user_id'] = int(call_data[1])
            USER_PAYCARD_FISH[int(call_data[1])]['accpet_or_reject'] = False



def payment_decline_reason_create():
    payment_decline_reason_2 = {'reason' : False  , 'user_id' : int}
    
    return payment_decline_reason_2

payment_decline_reason_2={}



# ./buy services > disagree of fish : getting reason
@bot.message_handler(func= lambda message : (message.from_user.id in payment_decline_reason_2 and len(payment_decline_reason_2) >=1 and payment_decline_reason_2[message.from_user.id]['reason'] == True))
def get_decline_reason(message):
    
    user_id = payment_decline_reason_2[message.from_user.id]['user_id']
    if payment_decline_reason_2[message.from_user.id]['reason'] == True : 
        payments_ = payments.objects.filter(user_id = payment_decline_reason_2[message.from_user.id]['user_id']).latest('payment_time')
        payments_.decline_reason = message.text
        payments_.save()
        bot.send_message(user_id , f'درخواست شما رد شد \n\n علت :‌ {message.text}')
        bot.send_message(message.chat.id ,f'درخواست پرداخت یوزر :‌{payment_decline_reason_2[message.from_user.id]["user_id"]} رد شد')
        USERS_BASKET.pop(message.from_user.id)
        USER_PAYCARD_FISH.pop(message.from_user.id)
        payment_decline_reason_2.pop(message.from_user.id)

# ---------------------------- service_status ----------------------------------------------------------------------------------------

marzban_panel_api_user = {}

@bot.callback_query_handler(func= lambda call: call.data in ['service_status' ,  'get_config_link' , 'get_qrcode_link']  or call.data.startswith(('serviceshow_' , 'get_new_link')))
def show_services(call):
    Text_0 = 'برای نمایش وضعیت سرویس بر روی آن کلیک کنید'

    if call.data=='service_status':
        bot.edit_message_text(Text_0 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.show_service_status(call.from_user.id))

    if call.data.startswith('serviceshow_'):
        call_data = call.data.split('_')
        Text_1 = 'وضعیت فعلی سرویس شما'
        subscriptions_ = subscriptions.objects.get(user_subscription=  f'{call_data[2]}_{call_data[3]}')
        request = panelsapi.marzban(int(subscriptions_.panel_id.pk)).get_user( f'{call_data[2]}_{call_data[3]}')
        marzban_panel_api_user[call.from_user.id]=request
        bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.user_service_status(call_data[1] , request))


    if call.data == 'get_config_link':
        if call.from_user.id in marzban_panel_api_user:
            Text_2 =marzban_panel_api_user[call.from_user.id]['subscription_url']
            bot.send_message(call.message.chat.id , Text_2)
        else:
            bot.answer_callback_query(call.id , 'نمیتوانید از این پیام استفاده کنید')
            bot.send_message(call.message.chat.id , Text_0 , reply_markup=BotKb.show_service_status(call.from_user.id))            


    if call.data == 'get_qrcode_link':
        if call.from_user.id in marzban_panel_api_user:
            Text_4 =marzban_panel_api_user[call.from_user.id]['subscription_url']
            qr = QRcode_maker.make_qrcode(Text_4)
            bot.send_photo(call.message.chat.id , qr)
        else:
            bot.answer_callback_query(call.id , 'نمیتوانید از این پیام استفاده کنید')
            bot.send_message(call.message.chat.id , Text_0 , reply_markup=BotKb.show_service_status(call.from_user.id))            


    if call.data.startswith('get_new_link'):
        if call.from_user.id in marzban_panel_api_user:
            user_name = marzban_panel_api_user[call.from_user.id]['username']
            subscriptions_ = subscriptions.objects.get(user_subscription = user_name)
            req = panelsapi.marzban(subscriptions_.panel_id.pk).revoke_sub(user_name)
            bot.send_message(call.message.chat.id , req['subscription_url'])
        else :
            bot.answer_callback_query(call.id , 'نمیتوانید از این پیام استفاده کنید')
            bot.send_message(call.message.chat.id , Text_0 , reply_markup=BotKb.show_service_status(call.from_user.id))            







# ---------------------------- MANAGEMENT ----------------------------------------------------------------------------------------


#> ./management
@bot.callback_query_handler(func=lambda call:call.data in ['robot_management' , 'back_from_management'])
def bot_mangement(call) :
    if call.data=='robot_management':
        Text_1='به مدیریت ربات خوش امدید '
        bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.management_menu_in_admin_side())
    
    
    if call.data=='back_from_management':
        Text_back='/خوش آمدید /'
        bot.edit_message_text(Text_back , call.message.chat.id ,call.message.message_id , reply_markup=BotKb.main_menu_in_user_side(call.from_user.id))






# ---------------------------------------------------------------------------------------------------------------------------------#
# -------------------------PANEL MANAGEMENT----------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------------------#



#> ./Management > Panels 
@bot.callback_query_handler(func=lambda call:call.data=='panels_management' or call.data=='back_from_panel_manageing' or call.data=='add_panel' or call.data=='remove_panel' or call.data=='manageing_panels')
def handle_panel(call):

    Text_0='هیچ پنلی برای حذف کردن پیدا نشد \n\n برای اضافه کردن اولین پنل به ربات /add_panel رو بزنید'


    if call.data=='panels_management' :
        Text_1='شما در حال مدیریت کردن بخش پنل ها هستید'
        bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.panel_management_menu_in_admin_side())



    if call.data=='back_from_panel_manageing':
        Text_back='به مدیریت ربات خوش امدید '
        bot.edit_message_text(Text_back , call.message.chat.id , call.message.message_id , reply_markup=BotKb.management_menu_in_admin_side())



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
@bot.message_handler(func=lambda message:PANEL_RECEIVING_STATE['Enable_Panel_Adding']==True and PANEL_RECEIVING_STATE['Panel_Name_Receiving']==False)
def handle_incoming_panelName(message):
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
@bot.callback_query_handler(func=lambda call:call.data.startswith(('manageing_panel_' , 'panel_status_' , 'panel_name_' , 'panel_url_' , 'panel_username_' , 'panel_password_' , 'view_password_' , 'view_username_' , 'reality_flow_' , 'panel_capacity_')) or call.data in ['back_to_manageing_panels'] )
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
    



#---------------------------------------------------------------------------------------------------------------------------------#
# -------------------------PRODUCTS-MANAGEMENT------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------------------#


#> ./Management > Product 
@bot.callback_query_handler(func=lambda call:call.data in [ 'products_management' , 'add_product' , 'remove_product' , 'manage_products' , 'back_from_products_manageing'])
def handle_products(call) :

    panel_=v2panel.objects.all()
    Text_0='هیچ پنلی برای لود کردن وجود ندارد \n\n اولین پنل خود را اضافه کنید :/add_panel'

    if call.data=='products_management':
        Text_1='✏️شما در حال مدیریت کردن بخش محصولات میباشید'
        bot.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.product_management_menu_in_admin_side())


    if call.data=='back_from_products_manageing':
        Text_2='به مدیریت ربات خوش امدید'
        bot.edit_message_text(Text_2 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.management_menu_in_admin_side())


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
        print(INBOUND_SELECTOR)
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








# ---------------------------------------------------------------------------------------------------------------------------------#
# ------------------------- Wallet-Profile ----------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------------------#

wallet_profile_dict = {'charge_wallet': False ,'waiting_for_USER_FISH' : False ,
                       'tranfert_money_from_wallet' : False , 'get_amount_to_transefer' : False , 'user_id' : None}


# ./wallet-profile
@bot.callback_query_handler(func = lambda call : call.data =='wallet_profile' or call.data =='back_from_wallet_profile' or call.data =='user_id' or call.data =='username' or call.data =='tranfert_money_from_wallet' or call.data =='charge_wallet') 
def wallet_profile(call):

    if call.data == 'wallet_profile' :
        bot.edit_message_text('پروفایل من : ' , call.message.chat.id , call.message.message_id , reply_markup= BotKb.wallet_profile(call.from_user.id))




    if call.data=='back_from_wallet_profile':
        bot.edit_message_text('welcome', call.message.chat.id , call.message.message_id , reply_markup= BotKb.main_menu_in_user_side(call.from_user.id))



    if call.data=='user_id':
        info_list_def = BotKb.wallet_profile(call.from_user.id , True)
        bot.edit_message_text(f'پروفایل من :‌ \n\n ایدی عددی :  <code>{info_list_def[0]}</code> \n\n' , call.message.chat.id , call.message.message_id ,parse_mode="HTML" ,reply_markup= BotKb.wallet_profile(call.from_user.id))



    if call.data =='username':
        info_list_def = BotKb.wallet_profile(call.from_user.id , True)
        bot.edit_message_text(f'پروفایل من :‌ \n\n یوزرنیم :  <code>@{info_list_def[1]}</code> \n\n ' , call.message.chat.id , call.message.message_id ,parse_mode="HTML" ,reply_markup= BotKb.wallet_profile(call.from_user.id))
        


    if call.data=='tranfert_money_from_wallet':
        wallet_profile_dict['tranfert_money_from_wallet'] = True
        bot.send_message(call.message.chat.id , 'لطفا ایدی عددی کاربر مقصد را وارد نمایید \n\n برای کنسل کردن انتقال  : /CANCEL')




    if call.data=='charge_wallet':
        wallet_profile_dict['charge_wallet'] = True
        bot.send_message(call.message.chat.id ,'مبلغ مورد نظر را به تومان برای شارژ کیف پول خود را وارد نمایید \n\n برای کنسل کردن انتقال  : /CANCEL')





# ./wallet_profile > tranfert_money_from_wallet
@bot.message_handler(func= lambda message : wallet_profile_dict['tranfert_money_from_wallet'] == True)
def tranfert_money_from_wallet(message):

    if wallet_profile_dict['tranfert_money_from_wallet'] == True :
        user_id = message.text
        if message.text == '/CANCEL':
            
            wallet_profile_dict['tranfert_money_from_wallet'] = False
            wallet_profile_dict['get_amount_to_transefer'] = False
            wallet_profile_dict['user_id'] = None
            bot.send_message(message.chat.id , 'پروفایل من :' , reply_markup=BotKb.wallet_profile(message.from_user.id))
        else:
            if  not users.objects.filter(user_id = user_id).exists() :
                bot.send_message(message.chat.id , 'اکانتی با ایدی عددی ارسال شده وجود ندارد \n\n برای کنسل کردن انتقال  : /CANCEL')

            else :
                wallet_profile_dict['user_id'] = message.text
                wallet_profile_dict['get_amount_to_transefer'] = True
                wallet_profile_dict['tranfert_money_from_wallet'] = False    
                bot.send_message(message.chat.id , 'مبلغ مورنظر را وارد نمایید \n\n برای کنسل کردن انتقال  : /CANCEL')





# ./ wallet_profile > transfer_money_from_wallet : get amount
@bot.message_handler(func = lambda message: wallet_profile_dict['get_amount_to_transefer'] == True)
def tranfert_money_from_wallet_amount(message):

    
    if wallet_profile_dict['get_amount_to_transefer'] == True :
        if message.text == '/CANCEL' : 
            wallet_profile_dict['tranfert_money_from_wallet'] = False
            wallet_profile_dict['get_amount_to_transefer'] = False
            wallet_profile_dict['user_id'] = None
            bot.send_message(message.chat.id , 'پروفایل من :' , reply_markup=BotKb.wallet_profile(message.from_user.id))


        else :
           
            if  not message.text.isdigit():
                bot.send_message(message.chat.id , 'لطفا مقدار عددی وارد کنید \n\n برای کنسل کردن انتقال  : /CANCEL')

            else :

                users_2 = users.objects.get(user_id = message.from_user.id)
                if users_2.user_wallet  == 0 :
                    wallet_profile_dict['tranfert_money_from_wallet'] = False
                    wallet_profile_dict['get_amount_to_transefer'] = False
                    wallet_profile_dict['user_id'] = None
                    bot.send_message(message.chat.id , 'موجودی حساب شما برای انتقال کافی نمیباشد')

                else :
                        users_1 = users.objects.get(user_id = wallet_profile_dict['user_id'])
                        #update user destination wallet
                        new_wallet = users_1.user_wallet + int(message.text)
                        users_1.user_wallet = new_wallet
                        # update origin wallet 
                        new_wallet2 = users_2.user_wallet - int(message.text)
                        users_2.user_wallet = new_wallet2

                        users_2.save()
                        users_1.save()
                        bot.send_message(message.chat.id , 'مبلغ مورد نظر با موفقیت انتقال یافت')
                        bot.send_message(wallet_profile_dict['user_id'] , f'شما مبلغ {message.text} دریافت کردید')   


                        wallet_profile_dict['tranfert_money_from_wallet'] = False
                        wallet_profile_dict['get_amount_to_transefer'] = False
                        wallet_profile_dict['user_id'] = None





# ./wallet-profile > charge - wallet
@bot.message_handler(func= lambda message: wallet_profile_dict['charge_wallet'] == True)
def charge_wallet_profilewallet(message):

    if wallet_profile_dict['charge_wallet'] == True:
        if message.text =='/CANCEL':
            wallet_profile_dict['charge_wallet'] = False
            bot.send_message(message.chat.id, 'پروفایل من ' , reply_markup=BotKb.wallet_profile(message.chat.id))

        else:
            if message.text.isdigit():
                text_ = f"""
                برای تکمیل شارژ حساب کاربری خود

                مبلغ :  {format(int(message.text) , ',')} تومان 
                به این شماره کارت واریز کرده و سپس فیش واریزی را همین جا ارسال کنید

                *************************
                شماره کارت :‌
                به نام : 
                *************************
                ⚠️ لطفا از اسپم کردن پرهیز نمایید
                ⚠️ از ارسال رسید فیک اجتناب فرمایید 
                ⚠️ هرگونه واریزی اشتباه بر عهده شخص میباشد

                """        
                wallet_profile_dict['waiting_for_USER_FISH'] = True
                wallet_profile_dict['charge_wallet'] = False
                bot.send_message(message.chat.id , text_ )
                users_ = users.objects.get(user_id = message.chat.id )
                payments_ = payments.objects.create(user_id = users_ , amount = message.text , payment_stauts = 'waiting' )
            else:
                bot.send_message(message.chat.id , 'لطفا مقدار عددی  وارد کنید \n\n برای لغو کردن انتقال :  /CANCEL')


    




# ./wallet-profile > charge - wallet : fish section
@bot.message_handler(func= lambda message : wallet_profile_dict['waiting_for_USER_FISH'] == True , content_types=['photo'])
def charge_wallet_profilewallet_fish(message):
    
    if wallet_profile_dict['waiting_for_USER_FISH'] == True :
        bot.send_message(message.chat.id , 'درخواست شما ارسال شد')
        bot.send_photo((i.user_id for i in admins.objects.all()) , message.photo[-1].file_id , reply_markup=BotKb.wallet_accepts_or_decline(message.chat.id ))




payments_decline = {'reason' : False  , 'userid':int}
# ./wallet-profile > charge - wallet : accpeting fish
@bot.callback_query_handler(func= lambda call : call.data.startswith('wallet_accepts_') or call.data.startswith('wallet_decline_'))
def accepts_decline(call):
    print(call.data)

    userId = call.data.split('_')[2]

    if call.data.startswith('wallet_accepts_'):

        payments_ = payments.objects.filter(user_id = userId).latest('payment_time')
        payments_.payment_stauts = 'accepted'
        payments_.save()

        users_ = users.objects.get(user_id = userId )
        users_.user_wallet = users_.user_wallet + payments_.amount
        users_.save()
        keyboard = InlineKeyboardMarkup()
        button = keyboard.add(InlineKeyboardButton('مشاهده کیف پول' , callback_data='wallet_profile'))
        
        bot.send_message(call.message.chat.id , 'درخواست پرداخت قبول شد')
        bot.send_message(userId , 'درخواست شما با موفقیت انجام شد' , reply_markup=keyboard)


    if call.data.startswith('wallet_decline_'):
        payments_decline['reason'] = True
        payments_decline['userid'] = userId
        bot.send_message(call.message.chat.id , 'دلیل رد کردن درخواست را ثبت بفرمایید')



# ./wallet-profile > charge - wallet : getting decline reason
@bot.message_handler(func = lambda message : payments_decline['reason'] == True)
def get_decline_reason(message):
    if payments_decline['reason'] == True :
        payments_ = payments.objects.filter(user_id = payments_decline['userid']).latest('payment_time')
        payments_.payment_stauts = 'declined'
        payments_.decline_reason = message.text
        payments_.save()
        bot.send_message(message.chat.id , 'درخواست پرداخت رد شد')
        bot.send_message(payments_decline['userid'] , f'درخواست شما رد شد \n\n علت :‌ {message.text}')













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



