import telebot
from telebot.types import InlineKeyboardMarkup , InlineKeyboardButton
from mainrobot.models import users , admins , v2panel , products , inovices , payments , channels
from keybuttons import BotkeyBoard as BotKb
import string , random , re , decimal , json 
from functions.USERS_checker import *
from functions.PANEL_managing import *
from functions.BUY_services import * 
from functions.checker_ import *
from tools import QRcode_maker
import panelsapi
BOT_TOKEN = '6724521362:AAGKk0Fgvm1oP90e1XKZvjZ4thx6D_IZCtI'

bot = telebot.TeleBot(token=BOT_TOKEN , parse_mode= "HTML" , colorful_logs= True)

# IMPORTANT #// TODO changin behaivor of call.data's # IMPORTANT

#//TODO add feature of spliting text msg\'s 
#//TODO add  enable | disable , also for products
#//TODO avoid adding products when no panel exists
#//TODO add /add_panel to the text if theres no plan for first time
#//TODO add charge wallet message in admin side section
#//TODO add port section in v2panel , change format of re checker in v2panel




#= Welcomer
@bot.message_handler(func=lambda message: '/start' in message.text)
def start_bot(message) :
    user_ = message.from_user 
    CHECKING_USER = CHECK_USER_EXITENCE(user_.id , user_.first_name , user_.last_name , user_.username , 0 )

    if CHECK_USER_CHANNEL(UserId=user_.id , Bot=bot) == True :
        #- Canceling operations : panels , product
        panel_reciving_state['enable_panel_adding'] = False
        product_reciving_state['enable_product_adding'] = False
        changing_panel_details.update({key : False for key in changing_panel_details})
        changing_product_details['enable_changing_product_deatails'] = False

        bot.send_message(message.chat.id , ' \ خوش امدید \ ' , reply_markup= BotKb.main_menu_in_user_side(message.from_user.id))

    else :
        channel = channels.objects.all()
        for i in channel:
            channel_url = bot.get_chat(i.channel_id).username
        Text = f'لطفا در کانال ما جوین شوید \n\n channel : @{channel_url} \n\n و سپس /start را وارد کنید '
        bot.send_message(message.chat.id , text=Text )




# -------------------------BUY SERVICES----------------------------------------------------------------------------------------
#//TODO edit all text in bot.send messsage
#> ./buy_services : selecting all plans if olny have on panel

    


number_of_panel_loaded_data = {'one_panel' : False , 'one_panel_id' : int ,
                                'two_more_panels' : False , 'two_panel_id' : int}

@bot.callback_query_handler(func = lambda call : call.data == 'buy_service')
def handler_buy_service_one_panel(call) :   

    panels_ = v2panel.objects.all()
    count_panels = []
    panels_info_set = []

    for i in panels_ :
        count_panels.append(i.id)


    if  call.data == 'buy_service' and 0 < len(count_panels) < 2  : 
        
        if plans_loading_for_one_panel() == 'panel_disable' :
            bot.send_message(call.message.chat.id , 'پنل  در حال بروزرسانی میباشند لطفا بعدا مراجعه فرمایید')

        else : 

            if isinstance(plans_loading_for_one_panel() , InlineKeyboardMarkup):
                bot.edit_message_text('select you\'r wish plan?', call.message.chat.id , call.message.message_id , reply_markup = plans_loading_for_one_panel())      
                number_of_panel_loaded_data['one_panel'] = True
                number_of_panel_loaded_data['one_panel_id'] = max(count_panels)
                panel_product_selected['panel_number'] =  max(count_panels)


        if plans_loading_for_one_panel() == 'sale_closed' :
            bot.send_message(call.message.chat.id , 'فروش بسته میباشد بعدا مراجعه فرمایید')


        if plans_loading_for_one_panel() == 'sale_open_no_zarfit' or plans_loading_for_one_panel() ==  'sale_zrafit_no_zarfit' :
            bot.send_message(call.message.chat.id , 'ظرفیت فروش به اتمام رسیده است بعد مراجعه فرمایید')


        if plans_loading_for_one_panel() == 'no_panel_product' : 
            bot.send_message(call.message.chat.id , 'هیچ سروری یا محصولی برای ارائه وجود ندارد' )



        
    if call.data == 'buy_service' and len(count_panels) >= 2 :
            keyboard = InlineKeyboardMarkup()
            for i in panels_ :
                button = InlineKeyboardButton(text =  i.panel_name , callback_data = 'panel_pk_' + str(i.id) )
                keyboard.add(button)
            button_back_2more = InlineKeyboardButton(text = 'بازگشت🔙' , callback_data = 'back_to_main_menu_for_2more_panels')
            keyboard.add( button_back_2more)
            bot.edit_message_text('which panel do you want?' , call.message.chat.id ,call.message.message_id , reply_markup = keyboard)





#> ./buy service : two panels buying
@bot.callback_query_handler(func = lambda call : call.data.startswith('panel_pk_'))
def handle_buy_service_two_panel(call):

    state_panel = plans_loading_for_two_more_panel(panel_pk= call.data.split('_')[-1])


    if call.data.startswith('panel_pk_') :
        
        if state_panel == 'panel_disable':
            bot.send_message(call.message.chat.id , 'پنل  در حال بروزرسانی میباشند لطفا بعدا مراجعه فرمایید')
        
        else :

            if  isinstance(state_panel , InlineKeyboardMarkup) :
                bot.edit_message_text('which products do you want ?' , call.message.chat.id , call.message.message_id , reply_markup = state_panel)
                number_of_panel_loaded_data['two_more_panels'] = True
                number_of_panel_loaded_data['two_panel_id'] = call.data.split('_')[-1]
                panel_product_selected['panel_number'] = call.data.split('_')[-1]

        if state_panel == 'sale_closed':
            bot.send_message(call.message.chat.id , 'فروش بسته میباشد بعدا مراجعه فرمایید')


        if (state_panel =='sale_zarfit_no_capcity') or (state_panel == 'sale_open_no_capcity')  :
            bot.send_message(call.message.chat.id , 'ظرفیت فروش به اتمام رسیده است بعد مراجعه فرمایید')


        if state_panel == 'no_products':
            bot.send_message(call.message.chat.id , 'هیچ محصولی برای ارائه وجود ندارد' )










panel_product_selected = {'panel_number' : '' , 
                          'product_name' : '' ,
                          'data_limit' : '' , 
                          'expire_date' : '' , 
                          'pro_cost' : '' ,
                          'withcapcity' : int ,
                          'get_username' : False ,
                          'usernameforacc'  : str ,
                          'statement' : []
                        }

#> ./buy_services > selecting products plans
@bot.callback_query_handler(func = lambda call : call.data.startswith('buyservice_'))
def handle_buyService_select_proplan(call) :
    
    if call.data.startswith('buyservice_') :
        for i in products.objects.filter(id = call.data.split('_')[1]):
            panel_product_selected['product_name'] = i.product_name
            panel_product_selected['data_limit'] = i.data_limit
            panel_product_selected['expire_date'] = i.expire_date
            panel_product_selected['pro_cost'] = i.pro_cost

        panel_product_selected['statement'] = [call.data.split('_')[2] , call.data.split('_')[3] , call.data.split('_')[4]]
           
        text_ = f"""محصول شما انتخاب شد ✅ 
        نام محصول : {panel_product_selected['product_name']}
        حجم محصول : {panel_product_selected['data_limit']} گیگ
        زمان محصول : {panel_product_selected['expire_date']} روزه 
        قیمت محصول : {format(panel_product_selected['pro_cost'] , ',')} تومان
        در صورت تایید گزینه تایید را زده و در صورت عدم تایید گزینه بازگشت را بزنید
        """

        keyboard = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton('✅ تایید محصول ' , callback_data= 'verify_product')
        button_2 = InlineKeyboardButton('↩️ بازگشت ' , callback_data = 'back_from_verfying')
        keyboard.add(button_1 , button_2 , row_width = 2)
        bot.edit_message_text(text = text_  ,chat_id =  call.message.chat.id , message_id = call.message.message_id , reply_markup = keyboard)







#> ./buy_services > proccess selected product plan 
@bot.callback_query_handler(func = lambda call : call.data == 'verify_product' or call.data == 'pay_with_wallet' or call.data == 'pay_with_card')
def handle_selected_products(call) : 


    if call.data == 'verify_product' :
        panel_product_selected['get_username'] = True
        bot.edit_message_text('لطفا یک نام کاربری انتخاب نمایید' , call.message.chat.id , call.message.message_id )




    if call.data == 'pay_with_wallet':
        user_ = users.objects.get(user_id = call.from_user.id)
        product_price = panel_product_selected['pro_cost']

        if user_.user_wallet < product_price :
            bot.send_message(call.message.chat.id , 'not enough found ')

        elif user_.user_wallet >= product_price :
            new_wallet = (user_.user_wallet) - decimal.Decimal(product_price)
            
            try :
                user_.user_wallet = new_wallet
                user_.save()

                if number_of_panel_loaded_data['one_panel'] == True :
                    if  ('open' and 'withcapcity') or ('zarfit' and 'withcapcity') in panel_product_selected['statement'] :
                        check_capcity(number_of_panel_loaded_data['one_panel_id'])
                else :
                    if number_of_panel_loaded_data['two_more_panels'] == True :
                        if  ('open' and 'withcapcity') or ('zarfit' and 'withcapcity') in panel_product_selected['statement']:
                            check_capcity(number_of_panel_loaded_data['two_panel_id'])

            except Exception as error_1:
                print(f'an error eccured  when updating user wallet: \n\t {error_1}')
            

            
            panel_ = v2panel.objects.get(id = panel_product_selected['panel_number'] )

            users_ = users.objects.get(user_id = call.from_user.id)

            inovivces_ = create_inovices(user_id= users_ ,
                                        user_username=call.from_user.username ,
                                        panel_name = panel_.panel_name ,
                                        product_name= panel_product_selected['product_name'],
                                        data_limit= panel_product_selected['data_limit'],
                                        expire_date= panel_product_selected['expire_date'] ,
                                        pro_cost= panel_product_selected['pro_cost'], 
                                        config_name = panel_product_selected['usernameforacc'] ,
                                        paid_status = 1 , # 0 > unpaid , 1 > paid , 2 > waiting  , 3 > disagree 
                                        paid_mode= 'wlt')
            
            inovivces2_ = inovices.objects.filter(user_id =users_).latest('created_date')
            payments_ = payments.objects.create(user_id = users_ , amount = panel_product_selected['pro_cost'] ,payment_stauts = 'accepted' , inovice_id = inovivces2_)
            send_request = panelsapi.marzban(panel_product_selected['panel_number']).add_user(panel_product_selected['usernameforacc'] , float(panel_product_selected['data_limit']) ,panel_product_selected['expire_date'])
            bot.edit_message_text('paied successfully \n\t waiting ' , call.message.chat.id , call.message.message_id)
            how_to_send(send_request , panel_product_selected['panel_number'] , bot , call)
            
        



            
        






    if call.data == 'pay_with_card':
        #//TODO add a table for storing karts number (payment setting)
        text_ = f"""
        برای تکمیل خرید خود و دریافت لینک اشتراک 

        مبلغ : {format(panel_product_selected['pro_cost'], ',')} تومان 
        به این شماره کارت واریز کرده و سپس فیش واریزی را همین جا ارسال کنید

        *************************
        شماره کارت :‌
        به نام : 
        *************************
        ⚠️ لطفا از اسپم کردن پرهیز نمایید
        ⚠️ از ارسال رسید فیک اجتناب فرمایید 
        ⚠️ هرگونه واریزی اشتباه بر عهده شخص میباشد

        """ 

        panel_id = products.objects.get(product_name = panel_product_selected['product_name']).panel_id
        panel_name = v2panel.objects.get(id = panel_id ).panel_name
        users_ = users.objects.get(user_id = call.from_user.id  )
        inovivces_ = create_inovices(user_id= users_,
                                        user_username=call.from_user.username ,
                                        panel_name = panel_name ,
                                        product_name= panel_product_selected['product_name'],
                                        data_limit= panel_product_selected['data_limit'],
                                        expire_date= panel_product_selected['expire_date'] ,
                                        pro_cost= panel_product_selected['pro_cost'], 
                                        config_name = panel_product_selected['usernameforacc'] ,
                                        paid_status= 2 , # 0 > unpaid , 1 > paid , 2 > waiting  , 3 > disagree
                                        paid_mode= 'kbk')

        user_fish['user_id'] = call.from_user.id 
        user_fish['fish_send'] = True
        bot.send_message(chat_id = call.message.chat.id , text = text_ )









#> ./buy_services > get user username 
@bot.message_handler(func= lambda message : panel_product_selected['get_username'] == True)
def get_username_for_config_name(message):
    if panel_product_selected['get_username'] == True:
        panel_product_selected['usernameforacc'] = f'{panel_product_selected["panel_number"]}_' + message.text
        panel_product_selected['get_username'] = False
        bot.send_message(message.chat.id  ,'لطفا یک روش پرداخت را انتخاب کنید' , reply_markup= BotKb.payby_in_user_side())
        








user_fish = {'user_id' : int , 'fish_send' : False}
# ./buy_service > seding fish section
@bot.message_handler(func = lambda message :  user_fish['fish_send'] == True , content_types=['photo'] )
def getting_fish_image(message):

    users_ = users.objects.get(user_id = message.from_user.id)
    admins_ = admins.objects.all()
    inovices_ = inovices.objects
    
    all_user_kbk_inovices = []

    if user_fish['fish_send'] == True :
        for i in inovices_.filter(paid_status=2):
            if i.user_id == users_ and inovices_.filter(paid_status=2).order_by('created_date') and inovices_.filter(paid_mode = 'kbk').order_by('created_date'):
                all_user_kbk_inovices.append(i.id)


        
        if check_time_passed(all_user_kbk_inovices[-1]) == 'time_passed':
            update_inovice_status = inovices_.get(id = all_user_kbk_inovices[-1])
            update_inovice_status.paid_status = 0
            update_inovice_status.save()
            
            bot.send_message(message.chat.id , 'این صورت حساب باطل شده است مجدد صادر فرمایید')



        else :
            panel_name = v2panel.objects.get(id = number_of_panel_loaded_data['two_panel_id']).panel_name
            user_info = users.objects.get(user_id = message.from_user.id)
            
            caption_text = f"""
            درخواست خرید ✅:
 ---------------------------------------------------------------------------
┌─نام کاربر : {user_info.first_name } {'' if not user_info.last_name else user_info.last_name}
│ایدی عددی کاربر : {user_info.user_id}
│ایدی تلگرام : {user_info.username}
│موجودی کیف پول : {format(user_info.user_wallet, ",")} تومان
│میلغ خرید : {panel_product_selected['pro_cost']}
│نام محصول :‌ {panel_product_selected['product_name']}
└─نام سرور : {panel_name}
            """

            for i in admins_:
                    bot.send_photo( i.user_id , message.photo[-1].file_id , caption = caption_text , reply_markup= BotKb.agree_or_disagree(message.from_user.id) )
            
            bot.send_message(message.chat.id , 'درخواست شما برای ادمین صادر شد در صورت تایید به اطلاع شما خواهد رسید')
        user_fish.update({'user_id': int, 'fish_send': False})
        taaeed_ya_rad['status'] = True







taaeed_ya_rad = {'status':False }
@bot.callback_query_handler(func = lambda call : call.data.startswith('agree_') or call.data.startswith('disagree_') )
def agree_or_disagree_kbk_payment(call):
    
    call_data = call.data.split('_')
    print(call_data)

    
    if call.data.startswith('agree_')  and taaeed_ya_rad['status'] == True:

                inovices_ = inovices.objects.all().filter(user_id=call_data[1]).order_by('created_date').last()
                inovices_.paid_status = 1
                inovices_.save()
                # sending config from panel

                users_ = users.objects.get(user_id = call_data[1])
                inovivces2_ = inovices.objects.filter(user_id =users_).latest('created_date')
                payments_ = payments.objects.create(user_id = users_ , amount = panel_product_selected['pro_cost'] ,payment_stauts = 'accepted' , inovice_id = inovivces2_)


                if number_of_panel_loaded_data['one_panel'] == True :
                        if  ('open' and 'withcapcity') or ('zarfit' and 'withcapcity') in panel_product_selected['statement'] :
                            check_capcity(number_of_panel_loaded_data['one_panel_id'])
                else :
                    if number_of_panel_loaded_data['two_more_panels'] == True :
                        if  ('open' and 'withcapcity') or ('zarfit' and 'withcapcity') in panel_product_selected['statement']:
                            check_capcity(number_of_panel_loaded_data['two_panel_id'])
                

                bot.send_message(call.message.chat.id , 'پرداخت انجام شد')
                bot.send_message(call.data.split('_')[1] , 'پرداخت شما با موفقیت انجام شد \n YOUR CONFIG')
                send_request = panelsapi.marzban(panel_product_selected['panel_number']).add_user(panel_product_selected['usernameforacc'] , float(panel_product_selected['data_limit']) ,panel_product_selected['expire_date'])
                how_to_send(send_request , panel_product_selected['panel_number'] , bot , call)
                taaeed_ya_rad['status'] = False




    if call.data.startswith('disagree_')  and taaeed_ya_rad['status'] == True:
            users_ = users.objects.get(user_id = call_data[1])

            inovices_ = inovices.objects.all().filter(user_id=users_).order_by('created_date').last()
            inovices_.paid_status = 3
            inovices_.save()

            inovivces2_ = inovices.objects.filter(user_id =users_).latest('created_date')
            payments_ = payments.objects.create(user_id = users_ , amount = panel_product_selected['pro_cost'] ,payment_stauts = 'declined' , inovice_id = inovivces2_)

            bot.send_message(call.message.chat.id , 'علت رد پرداخت را ارسال کنید')
            payments_decline_1['userid'] = call_data[1]
            payments_decline_1['reason'] = True
            taaeed_ya_rad['status'] = False
            




payments_decline_1 = {'reason' : False  , 'userid' : int}
# ./buy services > disagree of fish : getting reason
@bot.message_handler(func= lambda message : payments_decline_1['reason'] == True)
def get_decline_reason(message):
    
    user_id = payments_decline_1['userid']
    if payments_decline_1['reason'] == True : 
        payments_ = payments.objects.filter(user_id = payments_decline_1['userid']).latest('payment_time')
        payments_.decline_reason = message.text
        payments_.save()
        bot.send_message(user_id , f'درخواست شما رد شد \n\n علت :‌ {message.text}')
        bot.send_message(message.chat.id , 'درخواست پرداخت رد شد')


























#> ./buy_services > handle all back buttons 
@bot.callback_query_handler(func = lambda call : call.data =='back_to_main_menu_for_two_panels' or call.data == 'back_to_main_menu_for_2more_panels' or call.data == 'back_to_main_menu_for_one_panels' or call.data == 'back_from_verfying' or call.data =='back_from_payment')
def handling_all_back_buttons(call) :

    if call.data == 'back_to_main_menu_for_one_panels' : 
        bot.edit_message_text( 'Welcome' , call.message.chat.id , call.message.message_id , reply_markup = BotKb.main_menu_in_user_side(call.from_user.id) )
    


    if call.data == 'back_from_verfying':
        bot.edit_message_text('canceled // welcome' , call.message.chat.id , call.message.message_id , reply_markup = BotKb.main_menu_in_user_side(call.from_user.id))
        bot.answer_callback_query(call.id , 'CANCELED')


    if call.data == 'back_from_payment':
        bot.edit_message_text('payment canceled' , call.message.chat.id , call.message.message_id , reply_markup= BotKb.main_menu_in_user_side(call.from_user.id))
        bot.answer_callback_query(call.id , 'CANCELED')


    if call.data == 'back_to_main_menu_for_2more_panels':
        bot.edit_message_text('welcome', call.message.chat.id , call.message.message_id , reply_markup = BotKb.main_menu_in_user_side(call.from_user.id))



    if call.data == 'back_to_main_menu_for_two_panels':
            keyboard = InlineKeyboardMarkup()
            for i in v2panel.objects.all() :
                button = InlineKeyboardButton(text =  i.panel_name , callback_data = 'panel_pk_' + str(i.id) )
                keyboard.add(button)
            button_back_2more = InlineKeyboardButton(text = 'back🔙' , callback_data = 'back_to_main_menu_for_2more_panels')
            keyboard.add( button_back_2more)
            bot.edit_message_text('which panel do you want?' , call.message.chat.id ,call.message.message_id , reply_markup = keyboard)








# ---------------------------- MANAGEMENT ----------------------------------------------------------------------------------------








#> ./management
@bot.callback_query_handler(func = lambda call: call.data == 'robot_management' or call.data == 'back_from_management')
def bot_mangement(call) :

    if call.data == 'robot_management' :
        bot.edit_message_text('Welcome to bot mangement !!' , 
                              call.message.chat.id , 
                              call.message.message_id , 
                              reply_markup=BotKb.management_menu_in_admin_side()
                              )
    
    
    if call.data == 'back_from_management' :
        bot.edit_message_text('Welcome' ,
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup = BotKb.main_menu_in_user_side(call.from_user.id)
                             )







# -------------------------PANEL MANAGEMENT----------------------------------------------------------------------------------------








#> ./management > panels 
@bot.callback_query_handler(func = lambda call : call.data == 'panels_management' or call.data == 'add_panel' or call.data == 'remove_panel' or call.data == 'manageing_panels')
def handle_panel(call) :

    if call.data == 'panels_management' :
        bot.send_message(call.message.chat.id ,
                         text = 'You\'r managing panels !!' ,
                         reply_markup = BotKb.panel_management_menu_in_admin_side()
                        )



    #- Adding Panels
    if call.data == 'add_panel' :
        panel_reciving_state['enable_panel_adding'] = True
        panel_reciving_state.update({key : False for key in panel_reciving_state if  key != 'enable_panel_adding'})
        bot.edit_message_text('Send me you\'r Panel-Name ? \n\n to cancel it : /cancel ' ,
                              call.message.chat.id ,
                              call.message.message_id 
                             )


    #- Removing panel
    if call.data == 'remove_panel' :
        if BotKb.panel_management_remove_panel() == 'no_panel_to_remove' :
            bot.send_message(call.message.chat.id , 'no panel to remove \n\n\t add your first')
        else :
            bot.edit_message_text('which panel do you want to remove? \n\n tap to remove panel' ,
                                call.message.chat.id ,
                                call.message.message_id ,
                                reply_markup = BotKb.panel_management_remove_panel()
                                )


    #- Manging panels
    if call.data == 'manageing_panels':
        if BotKb.panel_management_manageing_panels() == 'no_panel_to_manage' :
            bot.send_message(call.message.chat.id , 'no panel to manage \n\n\t add your first')
        else :
            bot.edit_message_text('Now you\'r managing your panels  \n\n TAP on to manage them : ⚙️' , 
                                call.message.chat.id , 
                                call.message.message_id , 
                                reply_markup=BotKb.panel_management_manageing_panels()
                                )






panel_reciving_state = {'enable_panel_adding' : False ,
                        'panel_name_receiving' : False ,
                        'panel_url_receiving' : False ,
                        'panel_username_receiving' : False ,
                        'panel_password_receiving' : False ,
                        }

panel_information = {'panel_name' : '', 
                     'panel_url' : '' ,
                     'panel_username' : '' ,
                     'panel_password' : '',
                    }


#> ./management > panel > add_panel - panel_name (step-1-1)
@bot.message_handler(func = lambda message : panel_reciving_state['panel_name_receiving'] == False and panel_reciving_state['enable_panel_adding'] == True )
def handle_incoming_panelName(message) :

    if panel_reciving_state['panel_name_receiving'] == False and message.text == '/cancel' :
        panel_reciving_state.update({key : False for key in panel_reciving_state})
        bot.send_message(message.chat.id ,
                         'adding panel / CANCELED / ' , 
                         reply_markup = BotKb.panel_management_menu_in_admin_side() 
                        )
            
    else :

        if len(message.text) <= 256 :
            panel_information['panel_name'] = message.text
            panel_reciving_state['panel_name_receiving'] = True
            bot.send_message(message.chat.id ,
                             'Now send me you\'r Panel-Url ? \n\n to cancel it : /cancel ' , 
                            )
                    
        else:
            bot.send_message(message.chat.id ,
                            'The name must not be above 256 characters \n TRY AGAIN' ,
                            )


#> ./management > panel > add_panel - panel_url (step-1-2)
@bot.message_handler(func= lambda message : panel_reciving_state['panel_url_receiving'] == False and panel_reciving_state['enable_panel_adding'] == True)
def handle_incoming_panelUrl(message) :

    if panel_reciving_state['panel_url_receiving'] == False and message.text == '/cancel' :
        panel_reciving_state.update({key : False for key in panel_reciving_state})
        bot.send_message(message.chat.id , 
                         'adding panel / CANCELED / ' ,
                         reply_markup = BotKb.panel_management_menu_in_admin_side() 
                        )
            
    else : 
        http_or_https_chekcer = re.search(r'(http|https)://[^: ]+' , message.text)

        if  http_or_https_chekcer : 
            panel_information['panel_url'] = http_or_https_chekcer.group(0)
            panel_reciving_state['panel_url_receiving'] = True
            bot.send_message(message.chat.id ,
                             'Now send me you\'r Panel-Username ? \n\n to cancel it : /cancel ' , 
                            )

        else : 
            bot.send_message(message.chat.id ,
                            'Please send me url in this format : \n\n http://panelurl.com:port  or  https://panelurl.com:port' , 
                            )
                


#> ./management > panel > add_panel - panel_username (step-1-3)
@bot.message_handler(func = lambda message : panel_reciving_state['panel_username_receiving'] == False and panel_reciving_state['enable_panel_adding'] == True )
def handle_incoming_panelUsername(message) :

    if panel_reciving_state['panel_username_receiving'] == False and message.text == '/cancel' :
        panel_reciving_state.update({key : False for key in panel_reciving_state})
        bot.send_message(message.chat.id , 'adding panel / CANCELED / ' ,
                         reply_markup = BotKb.panel_management_menu_in_admin_side() 
                        )
            
    else:
        panel_information['panel_username'] = message.text
        panel_reciving_state['panel_username_receiving'] = True
        bot.send_message(message.chat.id ,
                        'Now send me you\'r Panel_Password ? \n\n to cancel it : /cancel ' , 
                        )
            


#> ./management > panel > add_panel - panel_passwd (step-1-4)
@bot.message_handler(func= lambda message : panel_reciving_state['panel_password_receiving'] == False and panel_reciving_state['enable_panel_adding'] == True )
def handle_incoming_panelPassword(message) :

    if panel_reciving_state['panel_password_receiving'] == False and message.text == '/cancel' :
        panel_reciving_state.update({key : False for key in panel_reciving_state})
        bot.send_message(message.chat.id , 'adding panel / CANCELED / ' ,
                         reply_markup = BotKb.panel_management_menu_in_admin_side() 
                        )
            
    else :
        panel_information['panel_password'] = message.text
        panel_reciving_state['panel_password_receiving'] = True
        panel_id_STRgenerated = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4))

        try :
            panel_ = v2panel.objects.create(panel_name = panel_information['panel_name'] ,
                                            panel_url = panel_information['panel_url'] ,
                                            panel_username = panel_information['panel_username'] ,
                                            panel_password=panel_information['panel_password'],
                                            panel_id_str = panel_id_STRgenerated , 
                                            )

            panel_information.update({key: '' for key in panel_information })
            bot.send_message(message.chat.id ,
                             'Panel successfully added' , 
                             reply_markup = BotKb.panel_management_menu_in_admin_side()
                            )

        except Exception as panel_creation:
            print(f'Error during creating panel \n\t Error-msg : {panel_creation}')
            bot.send_message(message.chat.id , 
                            'something went wrong \n\n please try again' ,
                            )
            





#> ./management > panel > remove panel (step-1)
@bot.callback_query_handler(func = lambda call : call.data in [str(i.id) + 'a' for i in v2panel.objects.all()])
def handle_removing_panels(call) : 

    if call.data in [str(i.id) + 'a' for i in v2panel.objects.all()] :
        call_= call.data
        ob_ = re.sub(r'[A-Za-z]+' , '' , call_)


    try :  
        panel_to_Remove = v2panel.objects.get(id = ob_).delete()

    except Exception as panel_RE :
        print(f'Error !! during removing panel \n\t Error-msg : {panel_RE}')


    try : 
        products_to_remove = products.objects.filter(panel_id = ob_).delete()
        
    except Exception as products_RE:
        print(f'Error !! during removing panel\'s product \n\t Error-msg :  {products_RE}')
     
      
    bot.edit_message_text("Panel and its products Removed ;\n !Succesfully " , 
                          call.message.chat.id ,
                          call.message.message_id ,
                          reply_markup= BotKb.panel_management_remove_panel()
                         )


#> ./management > panel > remove panel - back button (step-1-2)
@bot.callback_query_handler(func = lambda call : call.data == 'back_to_manage_panel')
def back_from_remove_panel(call) :
    if call.data == 'back_to_manage_panel' :
        bot.edit_message_text('You\'r managing panels !!' , 
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup = BotKb.panel_management_menu_in_admin_side()
                            )
        





#> ./management > panel > manageing panels
selected_panel = {'panel_id' : 0}
@bot.callback_query_handler(func = lambda call : call.data in [str(i.id) + 'aa' for i in v2panel.objects.all()] or call.data == 'back_to_manageing_panels' or call.data == 'back_to_manage_panel' )
def handle_panel_management(call) :

    if call.data in [str(i.id) + 'aa' for i in v2panel.objects.all()] :
        selected_panel['panel_id'] = 0
        ob_ = re.sub(r'[a-zA-Z]+' , '' , call.data)
        selected_panel['panel_id'] = int(ob_)
        bot.edit_message_text('to change your setting tap on buttons',
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup = BotKb.manage_selected_panel(id_panel_pk = ob_)
                             )
        

    if call.data == 'back_to_manageing_panels' :
        selected_panel['panel_id'] = 0
        bot.edit_message_text('Now you\'r managing your panels  \n\n TAP on to manage them : ⚙️'  ,
                              call.message.chat.id , 
                              call.message.message_id ,
                              reply_markup = BotKb.panel_management_manageing_panels()
                             )


    if call.data == 'back_to_manage_panel' :
        bot.edit_message_text('Welcome to bot mangement !!' , 
                              call.message.chat.id , 
                              call.message.message_id ,
                              reply_markup = BotKb.panel_management_menu_in_admin_side()
                            )
        






#> ./management > panel > manage panels - Change status (step-1)
@bot.callback_query_handler(func = lambda call : call.data == 'panel_status_' + getting_panel_pk(selected_panel) )
def changing_panel_details_status(call):
    
    if call.data == 'panel_status_' + getting_panel_pk(selected_panel) :
        try :
            panel_ = v2panel.objects.get(id = int(getting_panel_pk(selected_panel)))
            panel_new_status = 0 if panel_.panel_status == 1 else 1
            panel_.panel_status = panel_new_status
            panel_.save()

        except Exception as changestatus_RE:
            print(f'Error during changing panel status \n\t Error-msg : {changestatus_RE}')
        
        bot.edit_message_text(f'to change your setting tap on buttons \n\n Panel status changed : {"enable" if panel_.panel_status == 1 else "disable"}' ,
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup = BotKb.manage_selected_panel(id_panel_pk = int(getting_panel_pk(selected_panel)))
                             )
        
        bot.answer_callback_query(call.id , 
                                  'enable' if panel_.panel_status == 1 else 'disable'
                                 )
        



changing_panel_details = {'panel_name' : False , 
                          'panel_url' : False ,
                          'panel_username' : False ,
                          'panel_password' : False , 
                        }


#> ./management > panel > manage panels - change panel_name -1 (step-2.1)
@bot.callback_query_handler(func = lambda call : call.data  == 'panel_name_' + getting_panel_pk(selected_panel))
def changing_panel_details_name(call):

    if call.data == 'panel_name_' + getting_panel_pk(selected_panel):
        changing_panel_details['panel_name'] = True
        bot.send_message(call.message.chat.id ,
                        'Send me your new panel name? \n\n to cancel it : /cancel'
                        )


#> ./management > panel > manage panels - change panel_name -2 (step-2.2)
@bot.message_handler(func = lambda message : changing_panel_details['panel_name'] == True)
def get_changing_panel_details_name(message):
    
    if changing_panel_details['panel_name'] == True and message.text == '/cancel':
        changing_panel_details['panel_name'] = False
        bot.send_message(message.chat.id , 
                         'to change your setting tap on buttons  \n\n changing panel name : / CANCELED / ' ,
                         reply_markup = BotKb.manage_selected_panel(id_panel_pk = int(getting_panel_pk(selected_panel)))
                        )
    
    else:

        try:
            panel_ = v2panel.objects.get(id = int(getting_panel_pk(selected_panel)))
            panel_new_name = message.text 
            panel_.panel_name = panel_new_name
            panel_.save()
            changing_panel_details['panel_name'] = False

        except Exception as changename_RE:
            print(f'Error during changing panel name \n\t  Error-msg : {changename_RE}')

        bot.send_message(message.chat.id ,
                        'to change your setting tap on buttons \n\n Panel name changed' ,
                        reply_markup=BotKb.manage_selected_panel(id_panel_pk = int(getting_panel_pk(selected_panel)))
                        )
        



#> ./management > panel > manage panels - change panel_url -1 (step-3-1)
@bot.callback_query_handler(func = lambda call: call.data  == 'panel_url_' + getting_panel_pk(selected_panel))
def changing_panel_details_name(call):

    if call.data == 'panel_url_' + getting_panel_pk(selected_panel):
        changing_panel_details['panel_url'] = True
        bot.send_message(call.message.chat.id , 
                         'send me your new panel url? \n\n to cancel it : /cancel'
                         )


#> ./management > panel > manage panels - change panel_url -2 (step-3-2)
@bot.message_handler(func = lambda message : changing_panel_details['panel_url'] == True)
def get_changing_panel_details_name(message):

    if changing_panel_details['panel_url'] == True and message.text == '/cancel' :
        changing_panel_details['panel_url'] = False
        bot.send_message(message.chat.id , 
                         'to change your setting tap on buttons  \n\n changing panel url / CANCELED / ' ,
                         reply_markup = BotKb.manage_selected_panel(id_panel_pk = int(getting_panel_pk(selected_panel)))
                        )
    else :   

        http_or_https_chekcer = re.search(r'(http|https)://[^: ]+' , message.text)
        
        if http_or_https_chekcer :

            try:

                panel_ = v2panel.objects.get(id = int(getting_panel_pk(selected_panel)))
                panel_new_name = http_or_https_chekcer.group(0)
                panel_.panel_url = panel_new_name
                panel_.save()
                changing_panel_details['panel_url'] = False

            except Exception as changeurl_RE:
                print(f'Error during changing panel url \n\t  Error-msg : {changeurl_RE}')

            bot.send_message(message.chat.id ,
                     'to change your setting tap on buttons \n\n Panel url changed' ,
                     reply_markup=BotKb.manage_selected_panel(id_panel_pk= int(getting_panel_pk(selected_panel)))
                    )
        else:
            bot.send_message(message.chat.id , 
                            'Please send me new url in this format \n\n http://test.com or https://test.com \n\n to cancel it : /cancel'
                            )






#> ./management > panel > manage panels - change panel_username -1 (step-4-1)
@bot.callback_query_handler(func = lambda call: call.data  == 'panel_username_' + getting_panel_pk(selected_panel))
def changing_panel_details_name(call):

    if call.data == 'panel_username_' + getting_panel_pk(selected_panel) :
        changing_panel_details['panel_username'] = True
        bot.send_message(call.message.chat.id , 
                        'send me your new panel username? \n\n to cancel it : /cancel'
                        )



#> ./management > panel > manage panels - change panel_username -2 (step-4-2)
@bot.message_handler(func = lambda message : changing_panel_details['panel_username'] == True)
def get_changing_panel_details_name(message):

    if changing_panel_details['panel_username'] == True and message.text == '/cancel' :
        changing_panel_details['panel_username'] = False
        bot.send_message(message.chat.id , 
                         'to change your setting tap on buttons  \n\n changing panel username / CANCELED / ' ,
                         reply_markup = BotKb.manage_selected_panel(id_panel_pk = int(getting_panel_pk(selected_panel)))
                        )
    else:

        try:
            panel_ = v2panel.objects.get(id = int(getting_panel_pk(selected_panel)))
            panel_new_name = message.text 
            panel_.panel_username = panel_new_name
            panel_.save()
            changing_panel_details['panel_username'] = False

        except Exception as changeusername_RE:
            print(f'Error during changing panel username \n\t  Error-msg : {changeusername_RE}')

        bot.send_message(message.chat.id ,
                    'to change your setting tap on buttons \n\n panel username changed' ,
                    reply_markup=BotKb.manage_selected_panel(id_panel_pk = int(getting_panel_pk(selected_panel)))
                    )
    





#> ./management > panel > manage panels - change panel_password -1 (step-5-1)
@bot.callback_query_handler(func = lambda call: call.data.startswith('panel_password_')  or call.data == 'panel_password')
def changing_panel_details_name(call):

    list_calls = call.data.split('_')
    
    if  call.data =='panel_password' :
        BotKb.manage_selected_panel(id_panel_pk = selected_panel['panel_id'] , passwd = True)
        bot.edit_message_text('to change your setting tap on buttons',
                                call.message.chat.id ,
                                call.message.message_id ,
                                reply_markup = BotKb.manage_selected_panel(id_panel_pk = selected_panel['panel_id'] , passwd = True)
                                )
            
    if call.data.startswith('panel_password_') :
        changing_panel_details['panel_password'] = True
        bot.send_message(call.message.chat.id , 
                            'send me your new panel password? \n\n to cancel it : /cancel'
                            )




#> ./management > panel > manage panels - change panel_password -2 (step-5-2)
@bot.message_handler(func = lambda message : changing_panel_details['panel_password'] == True)
def get_changing_panel_details_name(message):

    if changing_panel_details['panel_password'] == True and message.text == '/cancel' :
        changing_panel_details['panel_password'] == False
        bot.send_message(message.chat.id , 
                         'to change your setting tap on buttons  \n\n changing panel password / CANCELED / ' ,
                         reply_markup = BotKb.manage_selected_panel(id_panel_pk = int(getting_panel_pk(selected_panel)))
                        )
    else : 

        try:
            panel_ = v2panel.objects.get(id = int(getting_panel_pk(selected_panel)))
            panel_new_name = message.text 
            panel_.panel_password = panel_new_name
            panel_.save()
            changing_panel_details['panel_password'] = False

        except Exception as changepassword_RE:
            print(f'Error during changing panel username \n\t  Error-msg : {changepassword_RE}')

        bot.send_message(message.chat.id ,
                    'to change your setting tap on buttons \n\n panel password changed' ,
                    reply_markup=BotKb.manage_selected_panel(id_panel_pk= int(getting_panel_pk(selected_panel)))
                    )
        
#//TODO add security deatils for password button




#> ./management > panel > manage panels - change panel_reality -1 (step-6-1)
@bot.callback_query_handler(func = lambda call : call.data == 'reality_flow_'+ getting_panel_pk(selected_panel))
def changing_panel_details_reality(call):

    if call.data == 'reality_flow_'+ getting_panel_pk(selected_panel):
        bot.edit_message_text('Choose your prefer setting' , 
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup= BotKb.changin_reality_flow() 
                             )



#> ./management > panel > manage panels - change panel_reality -2 (step-6-2)
@bot.callback_query_handler(func = lambda call :  call.data == 'xtls-rprx-vision' or call.data == 'None')
def changing_panel_details_reality(call):

    if call.data == 'xtls-rprx-vision' :

        try : 
            panel_ = v2panel.objects.get(id = int(getting_panel_pk(selected_panel)))
            panel_new_reality = call.data 
            panel_.reality_flow = panel_new_reality
            panel_.save()

        except Exception as changereality_RE:
            print(f'Error during changing panel reality \n\t  Error-msg : {changereality_RE}')
        bot.edit_message_text('to change your setting tap on buttons \n\n Reality flow changed ' ,
                              call.message.chat.id , 
                              call.message.message_id ,
                              reply_markup = BotKb.manage_selected_panel(id_panel_pk= int(getting_panel_pk(selected_panel)))
                             )


    if call.data == 'None' :

        try : 
            panel_ = v2panel.objects.get(id = int(getting_panel_pk(selected_panel)))
            panel_new_reality = call.data 
            panel_.reality_flow = panel_new_reality
            panel_.save()

        except Exception as changereality_RE_2:
            print(f'Error during changing panel username \n\t  Error-msg : {changereality_RE_2}')

        bot.edit_message_text('to change your setting tap on buttons \n\n Reality flow changed ' , 
                              call.message.chat.id , 
                              call.message.message_id , 
                              reply_markup = BotKb.manage_selected_panel(id_panel_pk= int(getting_panel_pk(selected_panel)))
                              )
        





#> ./management > panel > manage panels - change panel_capcity -1 (step-7-1)
changing_panel_capicty = {'all_capcity' : False}

@bot.callback_query_handler(func = lambda call : call.data == 'panel_capacity_'+ getting_panel_pk(selected_panel) )
def changing_panel_details_capicty(call) :

    if call.data == 'panel_capacity_' + getting_panel_pk(selected_panel) :
        bot.edit_message_text('to change your setting tap on buttons' ,
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup = BotKb.changin_panel_capcity(id_panel_pk = int(getting_panel_pk(selected_panel)))
                             )



#> ./management > panel > manage panels - change panel_capcity -2 (step-7-2)
@bot.callback_query_handler(func = lambda call : call.data == 'capcity_mode' or call.data == 'sale_mode' or call.data == 'all_capcity' or call.data == 'sold_capcity' or call.data == 'remaining_capcity')
def changing_panel_details_capicty(call) :

    if call.data == 'capcity_mode' :

        panel_ = v2panel.objects.get(id = int(getting_panel_pk(selected_panel)))

        if panel_.capcity_mode == 0 :

            try :
                new_capcity = 1
                panel_.capcity_mode = new_capcity
                panel_.save()

            except Exception as capcity_mode_1 :
                print(f'Error during changing panel capcity mode \n\t  Error-msg : {capcity_mode_1}')


        elif panel_.capcity_mode == 1 :

            try :
                new_capcity = 2
                panel_.capcity_mode = new_capcity
                panel_.save()

            except Exception as capcity_mode_2 :
                print(f'Error during changing panel capcity mode \n\t  Error-msg : {capcity_mode_2}')

        else :
            try :
                new_capcity = 0
                panel_.capcity_mode = new_capcity
                panel_.save()

            except Exception as capcity_mode_3 :
                    print(f'Error during changing panel capcity mode \n\t  Error-msg : {capcity_mode_3}')

        bot.edit_message_text('to change your setting tap on buttons  \n\n capcity mode changed  ' ,
                              call.message.chat.id , 
                              call.message.message_id , 
                               reply_markup= BotKb.changin_panel_capcity(id_panel_pk= int(getting_panel_pk(selected_panel)))
                             )


    if call.data == 'sale_mode' :

        panel_ = v2panel.objects.get(id = int(getting_panel_pk(selected_panel)))

        if panel_.panel_sale_mode == 0 :

            try :
                new_panel_sale_mode = 1
                panel_.panel_sale_mode = new_panel_sale_mode
                panel_.save()

            except Exception as sale_mode_1 :
                print(f'Error during changing panel sale mode \n\t  Error-msg : {sale_mode_1}')


        elif panel_.panel_sale_mode == 1 :

            try :
                new_panel_sale_mode = 2
                panel_.panel_sale_mode = new_panel_sale_mode
                panel_.save()

            except Exception as sale_mode_2 :
                print(f'Error during changing panel sale mode \n\t  Error-msg : {sale_mode_2}')

        else : 

            try :
                new_panel_sale_mode = 0
                panel_.panel_sale_mode = new_panel_sale_mode
                panel_.save()

            except Exception as sale_mode_3 :
                print(f'Error during changing panel sale mode \n\t  Error-msg : {sale_mode_3}')

        bot.edit_message_text('to change your setting tap on buttons  \n\n  sale mode changed  ' ,
                               call.message.chat.id ,
                               call.message.message_id ,
                               reply_markup = BotKb.changin_panel_capcity(id_panel_pk = int(getting_panel_pk(selected_panel)))
                                )
        


    if call.data == 'all_capcity' :
        changing_panel_capicty['all_capcity'] = True
        bot.send_message(call.message.chat.id , 
                        'send me your all capcity nmuber ? \n\n to cancel it : /cancel'
                        )


#> ./management > panel > manage panels - change panel_capcity -3 (step-7-3)
@bot.message_handler(func = lambda messgae : changing_panel_capicty['all_capcity'] == True)
def getting_changing_panel_capcity(messgae) :
   
    if changing_panel_capicty['all_capcity'] == True and messgae.text =='/cancel' :
        changing_panel_capicty['all_capcity'] = False 
        bot.send_message(messgae.chat.id ,
                         'to change your setting tap on buttons  \n\n changing panle capcity /CANCELED/' ,
                         reply_markup = BotKb.changin_panel_capcity(id_panel_pk = int(getting_panel_pk(selected_panel)))
                           )
    else :
        if messgae.text.isdigits():
            try : 
                panel_ = v2panel.objects.get(id = int(getting_panel_pk(selected_panel)))
                panel_new_all_capcity = messgae.text
                panel_.all_capcity = panel_new_all_capcity
                panel_.save()

            except Exception as capcitychanging_RE :
                    print(f'Error during changing panel capcity changing \n\t  Error-msg : {capcitychanging_RE}')

            bot.send_message(messgae.chat.id , 
                            'to change your setting tap on buttons  \n\n panel all capcity changed ' ,
                            reply_markup = BotKb.changin_panel_capcity(id_panel_pk = int(getting_panel_pk(selected_panel)))
                            )
        else : 
            bot.send_message(messgae.chat.id  , 'please send integer not str ')  


#> ./management > panel > manage panels - change panel_capcity back_button -4 (step-7-4)
@bot.callback_query_handler(func = lambda call : call.data == 'back_from_panel_capcity_list' or call.data == 'back_from_panel_howtosend_list')
def changing_panel_details_capicty(call) :

    if call.data == 'back_from_panel_capcity_list' :
        bot.edit_message_text('to change your setting tap on buttons' ,
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup= BotKb.manage_selected_panel(id_panel_pk = int(getting_panel_pk(selected_panel)))
                            )
        

    if call.data == 'back_from_panel_howtosend_list' : 
            bot.edit_message_text('to change your setting tap on buttons' ,
                                 call.message.chat.id ,
                                 call.message.message_id ,
                                 reply_markup= BotKb.manage_selected_panel(id_panel_pk = int(getting_panel_pk(selected_panel)))
                                 )    



inbounds_selected = {'inbounds': None}
#> ./management > panel > manage panels - how-to-sending
@bot.callback_query_handler(func = lambda call : call.data == 'how_to_send' or call.data == 'qrcode_sending' or call.data == 'link_sending' or call.data=='inbounds_selector' or (inbounds_selected['inbounds'] is not None and call.data in inbounds_selected['inbounds']) or call.data =='done_inbounds' or call.data =='back_from_inbounds_selecting')
def how_to_get_config(call) :

    if call.data == 'how_to_send' :
        bot.edit_message_text('specifing how to send configs after success pay' ,
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup= BotKb.how_to_send_links(int(getting_panel_pk(selected_panel)))
                             )


    if call.data == 'qrcode_sending' :
        panel_ = v2panel.objects.get(id = int(getting_panel_pk(selected_panel)))

        if panel_.send_qrcode_mode == 0 :

            try :
                new_send_qrcode_moode = 1
                panel_.send_qrcode_mode = new_send_qrcode_moode 
                panel_.save()   

            except Exception as qrcodechaing_RE_1 :
                print(f'Error during changing panel Qrcode changing \n\t  Error-msg : {qrcodechaing_RE_1}')

        elif panel_.send_qrcode_mode == 1 :

            try :
                new_send_qrcode_moode = 2
                panel_.send_qrcode_mode = new_send_qrcode_moode 
                panel_.save()    

            except Exception as qrcodechaing_RE_2 :
                print(f'Error during changing panel Qrcode changing \n\t  Error-msg : {qrcodechaing_RE_2}')

        else:

            try :
                new_send_qrcode_moode = 0
                panel_.send_qrcode_mode = new_send_qrcode_moode 
                panel_.save()  

            except Exception as qrcodechaing_RE_3 :
                print(f'Error during changing panel Qrcode changing \n\t  Error-msg : {qrcodechaing_RE_3}')    

        bot.edit_message_text('to change your setting tap on buttons  \n\n  qrcode sending mode changed ',
                              call.message.chat.id , 
                              call.message.message_id , 
                              reply_markup= BotKb.how_to_send_links(int(getting_panel_pk(selected_panel)))
                              )




    if call.data =='link_sending' :

        panel_ = v2panel.objects.get(id = int(getting_panel_pk(selected_panel)))

        if panel_.send_links_mode == 0 :

            try :
                new_send_links_mode = 1
                panel_.send_links_mode = new_send_links_mode
                panel_.save()    

            except Exception as linkchanging_RE_1 :
                print(f'Error during changing panel link changing \n\t  Error-msg : {linkchanging_RE_1}')

        elif panel_.send_links_mode == 1 :

            try :
                new_send_links_mode = 2
                panel_.send_links_mode = new_send_links_mode
                panel_.save()    

            except Exception as linkchanging_RE_2 :
                print(f'Error during changing panel link changing \n\t  Error-msg : {linkchanging_RE_2}') 

        else :

            try :
                new_send_links_mode = 0
                panel_.send_links_mode = new_send_links_mode
                panel_.save()   

            except Exception as linkchanging_RE_3 :
                print(f'Error during changing panel link changing \n\t  Error-msg : {qrcodechaing_RE_3}')          

        bot.edit_message_text('to change your setting tap on buttons  \n\n  link sending mode changed ', 
                              call.message.chat.id , 
                              call.message.message_id ,
                              reply_markup = BotKb.how_to_send_links(int(getting_panel_pk(selected_panel)))
                              )
        




    if call.data == 'inbounds_selector' :
        inbounds = panelsapi.marzban(panel_id= int(getting_panel_pk(selected_panel))).get_inbounds()
        inbounds_selected['inbounds'] = [f"{tag['protocol']}:{tag['tag']}" for outer in inbounds for tag in inbounds[outer]]
        
        Text = f"لیست اینباند های انتخابی \n\n []"
        bot.edit_message_text(Text , call.message.chat.id ,call.message.message_id , reply_markup= BotKb.select_inbounds(inbounds_selected['inbounds']))
        


    if  (inbounds_selected['inbounds'] is not None and call.data in inbounds_selected['inbounds']):
        
        inbounds_list = inbounds_selected['inbounds']
        for i in inbounds_list:
            if call.data == i:
                index_inboundlist = inbounds_list.index(call.data)

                if '✅' in i:
                    new_values = i.replace('✅', '❌')
                    inbounds_list[index_inboundlist] = new_values  

                elif '❌' in i:
                    new_values = i.replace('❌', '✅')
                    inbounds_list[index_inboundlist] = new_values  

                else:
                    values = i + '✅'
                    inbounds_list[index_inboundlist] = values  

        inbounds_checkmark = []
        for i in inbounds_selected['inbounds']:
            if  '✅' in i :
                inbounds_checkmark.append(i.strip('✅'))
            
            Text = f"لیست اینباند های انتخابی \n\n {inbounds_checkmark}"

        keyboard = BotKb.select_inbounds(inbounds_list) 
        bot.edit_message_text(Text , call.message.chat.id , call.message.message_id , reply_markup=keyboard)




    if call.data =='done_inbounds':
        
        group_inbounds = {}
        for items in inbounds_selected['inbounds']:
            if '✅' in items :
                key , value = items.split(':' , 1)
                value = value.strip('✅')
                if key not in group_inbounds:
                    group_inbounds[key] = []
                group_inbounds[key].append(value)

        try :
            panels_ = v2panel.objects.get(id = int(getting_panel_pk(selected_panel)))
            panels_.inbounds_selected = json.dumps(group_inbounds , indent=1)
            panels_.save()
        except Exception as e :
            print(f'something went wrong when adding inbounds into database : {e}')
        
        bot.edit_message_text("to change your setting tap on buttons" , call.message.chat.id , call.message.message_id , reply_markup= BotKb.manage_selected_panel(id_panel_pk = int(getting_panel_pk(selected_panel))))

    if call.data == 'back_from_inbounds_selecting':
        bot.edit_message_text("to change your setting tap on buttons" , call.message.chat.id , call.message.message_id , reply_markup= BotKb.manage_selected_panel(id_panel_pk = int(getting_panel_pk(selected_panel))))








# -------------------------PRODUCTS MANAGEMENT----------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------






#> ./management > product 
@bot.callback_query_handler(func = lambda call : call.data == 'products_management' or call.data == 'add_product' or call.data == 'remove_product' or call.data == 'manage_products')
def handle_products(call) :

    panel_ =  v2panel.objects.all()
    if call.data == 'products_management' :
        bot.send_message(call.message.chat.id , 
                        text ='you \'re managing products !!' ,
                        reply_markup = BotKb.product_management_menu_in_admin_side()
                        )


    #- Adding products 
    if call.data == 'add_product' :
        keyboard_add = InlineKeyboardMarkup()
        if not panel_.exists() :

            bot.send_message(call.message.chat.id ,
                            'no panel exists to add'
                            )
        else :

            for i in panel_ :
                buttons = InlineKeyboardButton(text = i.panel_name , callback_data = 'add_product_' + str(i.id))
                keyboard_add.add(buttons)

            back_button_add = InlineKeyboardButton(text = 'بازگشت ↪️'  , callback_data = 'back_from_chooing_panel_to_add_product')
            keyboard_add.add(back_button_add)

            product_reciving_state.update({key : False for key in product_reciving_state if key  != 'enable_product_adding' })

            bot.send_message(call.message.chat.id ,
                            text='Select wich panel do you want to add product?' ,
                            reply_markup = keyboard_add
                            )
            


    #- Removing products
    if call.data == 'remove_product' :

        keyboard_remove = InlineKeyboardMarkup()
        if not panel_.exists() :
            bot.send_message(call.message.chat.id , 'no panel exists to remove')
        else :
            for i in  panel_:
                buttons = InlineKeyboardButton(text = i.panel_name , callback_data ='remove_product_' + str( i.id))
                keyboard_remove.add(buttons)

            back_button_remove = InlineKeyboardButton(text = 'بازگشت ↪️'  , callback_data = 'back_from_chooing_panel_to_remove_product')
            keyboard_remove.add(back_button_remove)

            bot.send_message(call.message.chat.id ,
                            text = 'which panel do you want  ? \n\n tap to choose' ,
                            reply_markup = keyboard_remove
                            )
        

    

    if call.data == 'manage_products' :
        keyboard_manage = InlineKeyboardMarkup()
        if not panel_.exists():
            bot.send_message(call.message.chat.id , 'no panel exists to manage')
        else :
            for i in panel_:
                buttons = InlineKeyboardButton(text= i.panel_name , callback_data = 'manage_product_' + str(i.id))
                keyboard_manage.add(buttons)

            back_button_manage = InlineKeyboardButton(text = 'بازگشت ↪️' , callback_data = 'back_from_chooing_panel_to_manage_product')
            keyboard_manage.add(back_button_manage)

            bot.send_message(call.message.chat.id , 
                            'which panel do you want  ? \n\n tap to choose' , 
                            reply_markup = keyboard_manage
                            )





product_reciving_state = {'enable_product_adding' : False ,
                          'pro_name_receiving' : False , 
                          'data_limit_receiving' : False ,
                          'expire_date_receiving' : False ,
                          'pro_cost_receiving' : False ,
                          }


product_information = {'product_name' : '' ,
                       'data_limit' : '' ,
                       'expire_date' : '' ,
                       'pro_cost' : '' , 
                       'panel_id' : ''
                      }

#> ./management > product > add_product - select_panelId (step-1-1)
@bot.callback_query_handler(func = lambda call : call.data.startswith('add_product_'))
def handle_incoming_product_panelId(call) :

    product_reciving_state.update({key : False for key in product_reciving_state if key  != 'enable_product_adding' })

    if call.data.startswith('add_product_') : 
        product_reciving_state['enable_product_adding'] = True
        product_information['panel_id'] = int(call.data.split('_')[-1])

        bot.send_message(call.message.chat.id ,
                         text = 'Now me send you\'r product name? \n\n to cancel it : /cancel'
                         )
        

#> ./management > product > add_product - product_name (step-1-2)
@bot.message_handler(func = lambda message : product_reciving_state['pro_name_receiving'] == False and product_reciving_state['enable_product_adding'] == True)
def handle_incoming_product_name(message) :

    if product_reciving_state['pro_name_receiving'] == False :

        if message.text == '/cancel' : 
            product_reciving_state.update({key : False for key in product_reciving_state})

            bot.send_message(message.chat.id ,
                            'adding product /CANCELED/' ,
                             reply_markup = BotKb.product_management_menu_in_admin_side()
                            )
        else :

            if len(message.text) <= 128 :  
                product_information['product_name'] = message.text
                product_reciving_state['pro_name_receiving'] = True

                bot.send_message(message.chat.id ,
                                text = 'Now send me you\'r product data limit? \n\n to cancel it : /cancel'
                                )
                
            else :
                bot.send_message(message.chat.id ,
                                 'Product name must be under 128 character \n\n Please try again !! \n\n to cancel it : /cancel'
                                )
                
                
#> ./managemet > product > add_product - data_limit (step-1-3)
@bot.message_handler(func = lambda message : product_reciving_state['data_limit_receiving'] == False and product_reciving_state['enable_product_adding'] == True)
def handle_incoming_data_limit(message) :

    if product_reciving_state['data_limit_receiving'] == False and message.text =='/cancel' :
        product_reciving_state.update({key : False for key in product_reciving_state})
        bot.send_message(message.chat.id ,
                         'adding product /CANCELED/ ' , 
                         reply_markup = BotKb.product_management_menu_in_admin_side()
                        )
        
    else :

        if message.text.isdigit() :
            data_limit_checker = re.search(r'([0-9]{1,9}|[0-9]{1,9}\.[0-9]{0,2})', message.text)

            if data_limit_checker :
                product_information['data_limit'] = data_limit_checker.group(0)
                product_reciving_state['data_limit_receiving'] = True
                bot.send_message(message.chat.id ,
                                text = 'Now send me you\'r product expire date? \n\n to cancel it : /cancel'
                                )
            
            else : 
                bot.send_message(message.chat.id ,
                                'Please send me in this format : amount.00 \n\n to cancel it : /cancel'
                                )
                
        else :
            bot.send_message(message.chat.id , 
                            'please send me digits not strings \n\n to cancel it : /cancel'
                            )
            

#> ./management > product >  add_product - expire_date (step-1-4)
@bot.message_handler(func = lambda message : product_reciving_state['expire_date_receiving'] == False and product_reciving_state['enable_product_adding'] == True)
def handle_incoming_expire_date(message) :

    if product_reciving_state['expire_date_receiving'] == False and message.text =='/cancel' :
        product_reciving_state.update({key : False for key in product_reciving_state})
        bot.send_message(message.chat.id , 'adding product /CANCELEC/' ,
                         reply_markup = BotKb.product_management_menu_in_admin_side()
                        )
        
    else :

        if message.text.isdigit():
            product_information['expire_date'] = message.text
            product_reciving_state['expire_date_receiving'] = True
            bot.send_message(message.chat.id ,
                            text = 'Send me the price of the product? \n\n to cancel it : /cancel'
                            )
            
        else : 
            bot.send_message(message.chat.id , 
                            'please send me digits not strings \n\n to cancel ir : /cancel'
                            )
            

#> ./management > product > add_product - pro_cost (step-1-5)
@bot.message_handler(func = lambda message : product_reciving_state['pro_cost_receiving'] == False and product_reciving_state['enable_product_adding'] == True)
def handle_incoming_expire_date(message) :

    if product_reciving_state['pro_cost_receiving'] == False and message.text == '/cancel' :
        product_reciving_state.update({key : False for key in product_reciving_state})
        bot.send_message(message.chat.id ,
                        'adding product /CANCELEC/' ,
                        reply_markup = BotKb.product_management_menu_in_admin_side()
                        )
        
    else :

        if message.text.isdigit() :
            product_information['pro_cost'] = message.text
            product_reciving_state['pro_cost_receiving'] = True
            product_id_STRgenerated = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4))
            products_obejcts = [i.id for i in products.objects.all()] 
            
            try:
                product_ = products.objects.create(product_name = product_information['product_name'],
                                                data_limit=product_information['data_limit'],
                                                expire_date=product_information['expire_date'],
                                                pro_cost=product_information['pro_cost'],
                                                panel_id=product_information['panel_id'],
                                                pro_id_str = product_id_STRgenerated ,
                                                sort_id = max(products_obejcts)+1 if products_obejcts  else 1
                                                )
                
            except Exception as product_creation:
                print(f'Error during creating product \n\t Error-msg : {product_creation}')
                bot.send_message(message.chat.id , 
                                'something went wrong \n\n please try again' ,
                                )
                
            product_information.update({key : '' for key in product_information})
            bot.send_message(message.chat.id ,
                            'Product successfully added' ,
                            reply_markup = BotKb.product_management_menu_in_admin_side()
                            )
                
        else :
            bot.send_message(message.chat.id , 
                             'please send me digits not strings \n\n to cancel ir : /cancel'
                            )
            







product_remove_panelpk = {'panel_pk' : ''}
#> ./management > product > remove-product (step-1-1)
@bot.callback_query_handler(func= lambda call : call.data in [str(i.id) +'b' for i in products.objects.all()] or call.data.startswith('remove_product_'))
def handle_removing_products (call) :
    
    if call.data.startswith('remove_product_'):
        if BotKb.product_managemet_remove_products(panel_pk = call.data.split('_')[-1]) == 'no_products_to_remove':
            bot.send_message(call.message.chat.id , 'no products \n\n\t add your first' )
        else :
            product_remove_panelpk['panel_pk'] = call.data.split('_')[-1]
            bot.edit_message_text('which products do you want to remove ? \n\n tap to remove product ' ,
                                call.message.chat.id ,
                                call.message.message_id ,
                                reply_markup = BotKb.product_managemet_remove_products(panel_pk = call.data.split('_')[-1]))
            



    if call.data in [str(i.id) + 'b' for i in products.objects.all()] :
        call_ = call.data
        ob_ = re.sub(r'[a-zA-z]+' ,'',call_)
        productname = products.objects.get(id = ob_)
        

        try :
            product_to_remove = products.objects.get(id = ob_).delete()


        except Exception as products_errorRiase :
            print(f'Error during removing product \n Error_msg : {products_errorRiase}')
            bot.send_message(call.message.chat.id , 
                            text = f'Error during removing product \n\n Error_msg : {products_errorRiase}' ,
                            reply_markup = BotKb.product_managemet_remove_products(panel_pk = product_remove_panelpk['panel_pk'])
                            )
        

        else:
            bot.edit_message_text(f'Product removed succesfully \n\n  product name : {productname.product_name}' ,
                                  call.message.chat.id ,
                                  call.message.message_id ,
                                  reply_markup = BotKb.product_managemet_remove_products(panel_pk = product_remove_panelpk['panel_pk'])
                                  )
            






#> ./management > product > remove-product - next-or-prev-buttons (step-1-2)
@bot.callback_query_handler(func = lambda call :  call.data.startswith('next_page_products_') or call.data.startswith('prev_page_products_'))
def handle_NextPrev_button_in_remove_product(call):

    page_number = int(call.data.split('_')[-1])

    if call.data.startswith('next_page_products'):
        bot.edit_message_text(f'which products do you want to remove ? \n tap to remove product \n\n page : {page_number}' , 
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup= BotKb.product_managemet_remove_products(panel_pk = product_remove_panelpk['panel_pk'] , page = page_number)
                             )
        

    if call.data.startswith('prev_page_products_') :
        bot.edit_message_text(f'which products do you want to remove ? \n tap to remove product \n\n page : {page_number}' , 
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup= BotKb.product_managemet_remove_products(panel_pk = product_remove_panelpk['panel_pk'] , page = page_number)
                             )











#> ./management > product >  - back-buttons (step-1)
@bot.callback_query_handler(func = lambda call : call.data =='back_from_chooing_panel_to_manage_product' or call.data == 'back_from_manage_products_changing_limit' or call.data == 'back_from_remove_products' or call.data == 'back_from_chooing_panel_to_remove_product' or call.data == 'back_from_chooing_panel_to_add_product' or call.data == 'back_from_manage_products_list_updown')
def back_button_in_remove_product(call):


    if call.data == 'back_from_remove_products' :
        product_remove_panelpk['panel_pk'] = ''

        keyboard_remove = InlineKeyboardMarkup()

        for i in v2panel.objects.all():
            buttons = InlineKeyboardButton(text = i.panel_name , callback_data ='remove_product_' + str( i.id))
            keyboard_remove.add(buttons)

        back_button_remove = InlineKeyboardButton(text = 'بازگشت ↪️'  , callback_data = 'back_from_chooing_panel_to_remove_product')
        keyboard_remove.add(back_button_remove)

        bot.edit_message_text('which panel do you want  ? \n\n tap to choose' ,
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup = keyboard_remove
                             )





    if call.data == 'back_from_chooing_panel_to_remove_product' or call.data == 'back_from_chooing_panel_to_add_product' :
        bot.edit_message_text('you\'re managing products !!',
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup = BotKb.product_management_menu_in_admin_side()
                             )




    if call.data == 'back_from_manage_products_list_updown':
        keyboard_manage = InlineKeyboardMarkup()

        for i in v2panel.objects.all():
            buttons = InlineKeyboardButton(text= i.panel_name , callback_data = 'manage_product_' + str(i.id))
            keyboard_manage.add(buttons)

        back_button_manage = InlineKeyboardButton(text = 'بازگشت ↪️' , callback_data = 'back_from_chooing_panel_to_manage_product')
        keyboard_manage.add(back_button_manage)

        bot.edit_message_text('which panel do you want  ? \n\n tap to choose or tap بازگشت' ,
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup = keyboard_manage)



    if call.data == 'back_from_manage_products_changing_limit' :
        bot.edit_message_text('all products listed here', 
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup = BotKb.products_list(panel_pk= panel['panelpk']))



    if call.data == 'back_from_chooing_panel_to_manage_product':
        bot.edit_message_text('you \re managing products !!' ,
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup = BotKb.product_management_menu_in_admin_side())











panel = {'panelpk' : ''}
#> ./management > products > manage-product (step-1)
@bot.callback_query_handler(func = lambda call : call.data.startswith('manage_product_'))
def manage_product_choose_panel(call) : 
    
    if call.data.startswith('manage_product_'):
        if BotKb.products_list(call.data.split('_')[-1]) == 'no_product_to_manage':
            bot.send_message(call.message.chat.id , 'no products to manage \n\n\t add your first')
        else :
            panel_pk = call.data.split('_')[-1]
            panel['panelpk'] = panel_pk

            bot.edit_message_text('all products listed here' , 
                                call.message.chat.id ,
                                call.message.message_id ,
                                reply_markup= BotKb.products_list(panel_pk = panel_pk)
                                )
        


prodcuts_page = {'page' : 1}
#> ./management > products > manage-product (step-1-2)
@bot.callback_query_handler( func = lambda  call : call.data.startswith('down_') or call.data.startswith('up_'))
def handle_sorts(call) :
    
    
    if call.data.startswith('down_'):
        BotKb.products_list(panel_pk=panel['panelpk'], down=int(call.data.split('_')[-1]))
        bot.edit_message_text('reordered - down',
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=BotKb.products_list(panel_pk=panel['panelpk'], page=prodcuts_page['page']))


    if call.data.startswith('up_'):
        BotKb.products_list(panel_pk=panel['panelpk'], up=int(call.data.split('_')[-1]))
        bot.edit_message_text('reordered - up',
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=BotKb.products_list(panel_pk=panel['panelpk'], page=prodcuts_page['page']))
    


#> ./management > product > manage-product - next-or-prev-buttons (step-1-2)
@bot.callback_query_handler(func = lambda call :  call.data.startswith('product_next_page_products_') or call.data.startswith('product_prev_page_products_'))
def handle_NextPrev_button_in_remove_product(call):

    page_number = int(call.data.split('_')[-1])
    prodcuts_page['page'] = page_number

    if call.data.startswith('product_next_page_products_'):
        bot.edit_message_text(f'which products do you want  ? \n tap  product \n\n page : {page_number}' , 
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup= BotKb.products_list(panel_pk=panel['panelpk']  ,  page = page_number)
                             )
           

    if call.data.startswith('product_prev_page_products_') :
        bot.edit_message_text(f'which products do you want ? \n tap  product \n\n page : {page_number}' , 
                              call.message.chat.id ,
                              call.message.message_id ,
                              reply_markup= BotKb.products_list(panel_pk= panel['panelpk'] ,  page = page_number)
                             )
        











product_id = {'product_pk' : 0 }
#> ./management > products > manage-product (step-1-3)
@bot.callback_query_handler(func = lambda call : call.data.startswith('detaling_product_'))
def manage_products_base_id (call) : 


    if call.data.startswith('detaling_product_') : 
        changing_product_details['enable_changing_product_deatails'] = True
        product_id['product_pk'] = 0
        product_id['product_pk'] = int(call.data.split('_')[-1])

        bot.edit_message_text('to change details tap on them ' ,
                              call.message.chat.id ,
                              call.message.message_id , 
                              reply_markup = BotKb.product_changing_details(product_id = int(call.data.split('_')[-1]))
                            )





changing_product_details = {'enable_changing_product_deatails' : False ,
                            'product_name' : False ,
                            'data-limit' : False ,
                            'expire_date' : False ,
                            'pro_cost' : False}



#> ./management > products > manage-product - changing product-name -1 (step-1-4)
@bot.callback_query_handler(func = lambda call: call.data.startswith('_product_name_'))
def change_prodcut_name_details(call) : 

    if changing_product_details['enable_changing_product_deatails'] == True :
            
            if call.data.startswith('_product_name_')  :
                changing_product_details['product_name'] = True
                bot.send_message(call.message.chat.id ,
                                'send me your new product ||| name? \n\n to cancel it : /cancel'
                                )
                
    else :
        bot.answer_callback_query(call.id , 'pls use back button and try again')




#> ./management > products > manage-product - changeing product-name -2
@bot.message_handler(func= lambda message : changing_product_details['product_name'] == True)
def get_changing_product_details_name(message):

    if changing_product_details['product_name'] == True :

        if message.text == '/cancel' :
            changing_product_details['product_name'] = False
            bot.send_message(message.chat.id ,
                             'to change details tap on them' , 
                             reply_markup = BotKb.product_changing_details(product_id = product_id['product_pk'])
                            )

        else : 

            if len(message.text) <= 128:
                 
                try : 
                    product_ = products.objects.get(id = product_id['product_pk'])
                    product_new_name = message.text
                    product_.product_name = product_new_name
                    product_.save()
                    
                    changing_product_details['product_name'] = False

                except Exception as changename_RE :
                    print(f'Error during changing product name \n\t Error-msg : {changename_RE}')
                
                bot.send_message(message.chat.id , 
                                'to change settings tap to them \n\n prodcut name changed',
                                reply_markup = BotKb.product_changing_details(product_id = product_id['product_pk'])
                                )
                

            else :
                bot.send_message(message.chat.id ,
                                 'the product name must be undre 128 character\'s \n\n TRY again')






#> ./management > product > manage-product - changing data-limit -1
@bot.callback_query_handler(func = lambda call : call.data.startswith('_data_limit_'))
def change_product_datalimit_details(call):

    if changing_product_details['enable_changing_product_deatails'] == True :

        if call.data.startswith('_data_limit_') :
            changing_product_details['data-limit'] = True
            bot.send_message(call.message.chat.id ,
                            'send me your new data limit? \n\n to cancel it: /cancel')
            
    else :
        bot.answer_callback_query(call.id , 'pls use back button and try again')





#> ./management > product > manage-product - changing data-limit -2
@bot.message_handler(func = lambda message : changing_product_details['data-limit'] == True)
def get_changing_product_datalimit_details(message):

    if changing_product_details['data-limit'] == True:

        if message.text =='/cancel':
            changing_product_details['data-limit'] = False
            bot.send_message(message.chat.id , 
                            'to change details tap on them',
                            reply_markup = BotKb.product_changing_details(product_id = product_id['product_pk'])
                            )

        else :

            if message.text.isdigit() :
                data_limit_checker = re.search(r'([0-9]{1,9}|[0-9]{1,9}\.[0-9]{0,2}}})' , message.text)

                if data_limit_checker : 

                    try : 
                        product_ = products.objects.get(id = product_id['product_pk'])
                        product_new_datalimit = data_limit_checker.group(0)
                        product_.data_limit = product_new_datalimit
                        product_.save()
                        

                        changing_product_details['data-limit'] = False

                    except Exception as datalimit_RE :
                        print(f'Error during changing product data limit \n\n Error-msg : {datalimit_RE}')

                    bot.send_message(message.chat.id ,
                                    'to change settings tap to them \n\n prodcut datalimit changed' ,
                                    reply_markup = BotKb.product_changing_details(product_id = product_id['product_pk'])
                                    )
                    
                else :

                    bot.send_message(message.chat.id ,
                                    'the input must be string andin this format : 0.00  \n\n to cancel it : /cancel' ,
                                    reply_markup = BotKb.product_changing_details(product_id = product_id['product_pk'])
                                    )  
                      
            else :
                bot.send_message(message.chat.id , 
                                'please send me digits not strings \n\n to cancel it : /cancel'
                                )
                




#> ./management > product > manage-product - changeing expire-date -1 
@bot.callback_query_handler(func = lambda call : call.data.startswith('ـexpire_date_') )
def change_product_expiredate_details(call):

    if changing_product_details['enable_changing_product_deatails'] :

        if call.data.startswith('ـexpire_date_') :
            changing_product_details['expire_date'] = True
            bot.send_message(call.message.chat.id ,
                            'send me your new expire date? \n\n to cancel it: /cancel')
            
    else :

        bot.answer_callback_query(call.id , 'pls use back button and try again')




#> ./management > product > manage-product - changeing expire-date -2
@bot.message_handler(func = lambda message : changing_product_details['expire_date'] == True)
def get_changing_product_expiredate_detalis(message):
 
    if changing_product_details['expire_date'] == True:

        if message.text =='/cancel' :

            changing_product_details['expire_date'] = False
            bot.send_message(message.chat.id , 
                            'to change details tap on them',
                            reply_markup = BotKb.product_changing_details(product_id = product_id['product_pk'])
                            )

        else :

            if message.text.isdigit() :

                try : 
                    product_ = products.objects.get(id = product_id['product_pk'])
                    product_new_expiredate = message.text
                    product_.expire_date = product_new_expiredate
                    product_.save()
                    changing_product_details['expire_date'] = False

                except Exception as expiredate_RE :
                    print(f'Error during changing product data limit \n\n Error-msg : {expiredate_RE}')

                bot.send_message(message.chat.id ,
                                'to change settings tap to them \n\n prodcut expire date changed' ,
                                reply_markup = BotKb.product_changing_details(product_id = product_id['product_pk']))
                

            else : 
                bot.send_message(message.chat.id , 
                                'please send me digits not strings \n\n to cancel ir : /cancel'
                                )                        





#> ./management > product > manage-product - changeing expire-date -1 
@bot.callback_query_handler(func = lambda call : call.data.startswith('_pro_cost_'))
def change_product_expiredate_details(call) :

    if changing_product_details['enable_changing_product_deatails'] == True :

        if call.data.startswith('_pro_cost_') :
            changing_product_details['pro_cost'] = True
            bot.send_message(call.message.chat.id ,
                            'send me your new product cost? \n\n to cancel it: /cancel'
                            )
            
    else :
        bot.answer_callback_query(call.id , 'pls use back button and try again')


#> ./management > product > manage-product - changeing expire-date -2
@bot.message_handler(func = lambda message : changing_product_details['pro_cost'] == True)
def get_changing_product_expiredate_detalis(message):
 
    if changing_product_details['pro_cost'] == True:

        if message.text =='/cancel':
            changing_product_details['pro_cost'] = False
            bot.send_message(message.chat.id , 
                            'to change details tap on them',
                            reply_markup = BotKb.product_changing_details(product_id= product_id['product_pk'])
                            )

        else :
            
            if message.text.isdigit():

                try : 
                    product_ = products.objects.get(id = product_id['product_pk'])
                    product_new_pro_cost = message.text
                    product_.pro_cost = product_new_pro_cost
                    product_.save()
                    changing_product_details['pro_cost'] = False

                except Exception as procost_RE :
                    print(f'Error during changing product pro cost \n\n Error-msg : {procost_RE}')


                bot.send_message(message.chat.id ,
                                'to change settings tap to them \n\n prodcut pro cost changed' ,
                                reply_markup = BotKb.product_changing_details(product_id = product_id['product_pk']))
                

            else : 
                bot.send_message(message.chat.id , 
                                'please send me digits not strings \n\n to cancel ir : /cancel'
                                )                        









# ------------------------- Wallet-Profile ----------------------------------------------------------------------------------------

wallet_profile_dict = {'charge_wallet': False ,'waiting_for_user_fish' : False ,
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
                wallet_profile_dict['waiting_for_user_fish'] = True
                wallet_profile_dict['charge_wallet'] = False
                bot.send_message(message.chat.id , text_ )
                users_ = users.objects.get(user_id = message.chat.id )
                payments_ = payments.objects.create(user_id = users_ , amount = message.text , payment_stauts = 'waiting' )
            else:
                bot.send_message(message.chat.id , 'لطفا مقدار عددی  وارد کنید \n\n برای لغو کردن انتقال :  /CANCEL')


    




# ./wallet-profile > charge - wallet : fish section
@bot.message_handler(func= lambda message : wallet_profile_dict['waiting_for_user_fish'] == True , content_types=['photo'])
def charge_wallet_profilewallet_fish(message):
    
    if wallet_profile_dict['waiting_for_user_fish'] == True :
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


@bot.callback_query_handler(func= lambda call : call.data)
def check_call(call):
    print(call.data)

"""

