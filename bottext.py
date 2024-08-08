from mainrobot.models import v2panel , products , shomarekart

#-all editable messages 


#This is message when user send (/start)
welcome_msg = 'سلام به ربات ما خوش امدید😍🫠\n  فروشگاه ما به صورت ۲۴ ساعته اماده پشتیبانی از نیاز های شماست ❤️🙏🏻\n/start'


#Force user join channel 
force_channel_join_msg=f'♨️پیش از ادامه کار با ربات لطفا در چنل های ما جوین شوید'




#buy service section 
buy_service_section_product_msg = '✏️محصولی که میخواهید را انتخاب نمایید'
buy_service_section_choosing_panel_msg = '✏️سروری را که میخواهید انتخاب نمایید'
buy_service_section_choosing_username_msg = 'سرویس مورد نظر شما انتخاب شد ✅ \n 🟡 لطفا یک نام کاربری برای اشتراک خود انتخاب نمایید . \n   🔸نام کاربری باید به صورت حروف و اعداد اینگلیسی باشد \n TO CANCEL : /cancel'



def product_info_msg(product_info  , tamdid:bool=False):
    panel_name= v2panel.objects.get(id = product_info['panel_number']).panel_name
    if tamdid is not False:
        product_info_msg = f"""
<b>╮ ✣ سرویس شما انتخاب شد ✣ ╭</b>

┐<b>👤 نام کاربری</b>: <code>{product_info['config_name']}</code>

┊─<b>🌐  نام سرور</b>:‌ <code>{panel_name}</code>
┊─<b>📎  نام محصول</b>: <code>{product_info['product_name']}</code>
┊─<b>⌛️  زمان محصول</b>: <code>{product_info['expire_date']}</code> روز 
┊─<b>🔋  حجم محصول</b>: <code>{product_info['data_limit']}</code> گیگ 
┊─<b>💸  قیمت محصول</b>: <code>{format(product_info['pro_cost'] , ',')}</code> تومان

┘ <b> در صورت تایید گزینه ( تایید محصول ) را زده و در صورت عدم تایید گزینه بازگشت را بزنید </b>

"""
        return product_info_msg

    product_info_msg = f"""
<b>╮ ✣ سرویس شما انتخاب شد ✣ ╭</b>

┐<b>👤 نام کاربری</b>: <code>{product_info['usernameforacc']} </code>

┊─<b>🌐  نام سرور</b>:‌ <code>{panel_name} </code>
┊─<b>📎  نام محصول</b>: <code>{product_info['product_name']} </code>
┊─<b>⌛️  زمان محصول</b>: <code>{product_info['expire_date']} </code> روز
┊─<b>🔋  حجم محصول</b>: <code>{product_info['data_limit']} </code> گیگ
┊─<b>💸  قیمت محصول</b>: <code>{format(product_info['pro_cost'] , ',')} </code> تومان

┘ <b> در صورت تایید گزینه ( تایید محصول ) را زده و در صورت عدم تایید گزینه بازگشت را بزنید </b>

"""
    return product_info_msg
   


paied_msg = '✅پرداخت شما با موفقیت انجام شد \n محصول در حال اماده سازی و ارسال میباشد'




def buy_service_section_product_send(link_kind , link=None , image_only=None):
    buy_service_section_product_send = f"""
┐🛍محصول شما حاضر شد
 ─🧷نوع لینک : {link_kind}
┘  لینک شما :‌ \n<code>{link}</code> 
"""
    
    if image_only is not None:
        buy_service_section_product_image_send = f"""
┐🛍محصول شما حاضر شد
 ─🧷نوع لینک :{link_kind}
""" 
        return buy_service_section_product_image_send
        
    return buy_service_section_product_send



def buy_service_section_card_to_card_msg(cost): 
    shomarekart_ = shomarekart.objects.get(bank_inmsg=1)
    bank_kard = shomarekart_.bank_card
    bank_owner = shomarekart_.ownername
    bank_name = shomarekart_.bank_name

    kard = [str(bank_kard)[i : i+4] for i in range(0 , len(str(bank_kard)) , 4)]
    buy_service_section_card_to_card_msg = f"""
╮ برای  تکمیل خرید خود و دریافت لینک اشتراک خود  ╭

    ┤ 💸مبلغ : {format(cost , ',')}
به این شماره کارت واریز کرده و سپس فیش واریزی را همین جا ارسال کنید

▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐
         
┐  💳شماره کارت :‌  {(",".join(kard))}
 ─ ✍🏻 نام صاحب کارت : {bank_owner}
┘  🏦بانک عامل : {bank_name}

▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐

 - لطفا از اسپم کردن پرهیز نمایید⚠️
┤ از ارسال رسید فیک اجتناب فرمایید ⚠️
  - هرگونه واریزی اشتباه بر عهده شخص میباشد⚠️

  TO CANCEL : /cancel
  .
            """ 
    return buy_service_section_card_to_card_msg





inovice_time_passed_msg = 'این صورت حساب باطل شده است مجدد صادر فرمایید \n تمامی صورت حساب هایی که ۳۰ دقیقه از مدت زمان انها گذشته باشند به صورت خودکار باطل خواهند شد'


def send_user_buy_request_to_admins(user_basket , user_info , panel_name , tamdid:bool = None):

    if tamdid is not None:
        send_user_buy_request_to_admins = f'''
【✣ درخواست تمدید سرویس در سیستم ثبت شده است ✣】
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

┐🧷نام  کاربری  :  {user_info.first_name } {'' if not user_info.last_name else user_info.last_name}

┊──👤: ایدی عددی : {user_info.user_id}
┊──🆔 یوزرنیم تلگرام :‌ @‌{user_info.username}
┊──💰موجودی کیف پول :‌ {format(user_info.user_wallet, ",")} تومان
┊── 💸مبلغ خرید : {user_basket['pro_cost']} تومان
┊──🔗نام محصول : {user_basket['product_name']}

┘🔖 نام سرور : {panel_name}

     ¦─ در صورت تایید گزینه تایید پرداخت ✅ را بزنید در غیر این صورت رد پرداخت ❌  را بزنید
        '''
        return send_user_buy_request_to_admins
    
    send_user_buy_request_to_admins = f'''
【✣ درخواست خرید جدید در سیستم ثبت شده است ✣】
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

┐🧷نام  کاربری  :  {user_info.first_name } {'' if not user_info.last_name else user_info.last_name}

┊──👤: ایدی عددی : {user_info.user_id}
┊──🆔 یوزرنیم تلگرام :‌ @‌{user_info.username}
┊──💰موجودی کیف پول :‌ {format(user_info.user_wallet, ",")} تومان
┊── 💸مبلغ خرید : {user_basket['pro_cost']} تومان
┊──🔗نام محصول : {user_basket['product_name']}

┘🔖 نام سرور : {panel_name}

     ¦─ در صورت تایید گزینه تایید پرداخت ✅ را بزنید در غیر این صورت رد پرداخت ❌  را بزنید
        '''
    return send_user_buy_request_to_admins    

        

        
send_success_msg_to_user= '👨🏻‍💻درخواست شما برای ادمین صادر شد در صورت تایید به اطلاع شما خواهد رسید \n  —🔸 پردازش درخواست شما ممکن است مدتی طول بکشید در این صورت از ارسال مجدد درخواست خودداری کنید❌'
