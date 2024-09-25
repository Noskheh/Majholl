import datetime , jdatetime , panelsapi
from mainrobot.models import users ,subscriptions , payments , inovices
from django.db.models import Count 

def user_detaild (user_id):
    user_ = users.objects
    subscriptions_ = subscriptions.objects
    payments_ = payments.objects

    try : 
        user = user_.get(user_id = user_id)
                    
        number_subscription = subscriptions_.filter(user_id = user.user_id).aggregate(Count('id'))['id__count']
                        

        last_datetime = payments_.filter(payment_status = 'accepted' , user_id  = user.user_id).order_by('payment_time').values('payment_time').last()['payment_time']
        turn_lastdate_time_to_timestamp = datetime.datetime.timestamp(last_datetime)
        ir_datetime = jdatetime.datetime.fromtimestamp(turn_lastdate_time_to_timestamp).strftime('%H:%M:%S - %Y/%m/%d')
                        
        last_payment = payments_.filter(payment_status = 'accepted' , user_id = user.user_id).order_by('payment_time').values('amount').last()['amount']
                        
        amount_transaction = payments_.filter(payment_status = 'accepted' , user_id = user.user_id).aggregate(Count('id'))['id__count']
                        
        Text_1 = f"""
    ✤ اطلاعات کاربر با ایدی عددی 

– #️⃣ایدی عددی : <code>{user.user_id} </code>
– 👤نام کاربری :‌ {user.first_name} {user.last_name}
– 🌀یوزر نیم : @{user.username}

  • 👝موجودی کیف پول  : {format(int(user.user_wallet) , ',')} تومان
  • 📌تعداد اشتراک ها : {str(number_subscription) +" عدد" if number_subscription else '❕اشتراکی وجود ندارد'}
  • 📅تاریخ آخرین خرید‌‌ : {ir_datetime if ir_datetime else 'هنوز خریدی انجام نشده است'}
  • 💲مبلغ آخرین خرید : {str(format(last_payment,',')) + " تومان" if last_payment else '❕تراکنشی وجود ندارد '} 
  • تعداد تراکنش ها  : {str(amount_transaction) + " عدد" if amount_transaction else 'هیچ تراکنشی وجود ندارد'} 
  ↲ اشتراک ها :‌

"""
        return Text_1
    except Exception as error_user_detaild:
        print(f'Error while finding user_sub \n error-msg : {error_user_detaild}')






def config_details(SHOW_USER_INFO , call=None , message=None):
        call_ = call if call is not  None else message

        info = SHOW_USER_INFO[call_.from_user.id]

        subscriptions_ = subscriptions.objects
        payments_ = payments.objects
        inovices_ = inovices.objects

        
        try :     
            user_sub = subscriptions_.get(user_subscription = info['config_name'])

            product_info = user_sub.product_id.product_name if user_sub.product_id is not None else 'اطلاعاتی از این محصول در دسترسی نیست'
            
            panel_info = user_sub.panel_id.panel_name if user_sub.panel_id is not None else 'اطلاعاتی از پنل متصل شده وجود ندارد'
           
            payment_amount = payments_.get(inovice_id = inovices_.filter(config_name = str(info['config_name']) , user_id = info['user_id']).last().pk ).amount if inovices_.filter(config_name = str(info['config_name']) , user_id = info['user_id']).last().pk else 'اطلاعاتی در دسترسی نمیباشد'

            last_time_online = info['sub_request']['online_at'] if info['sub_request']['online_at'] is not None else 'None'
            if last_time_online != 'None':
                last_time_online_timestamp = datetime.datetime.strptime(last_time_online.split('.')[0], '%Y-%m-%dT%H:%M:%S')
                last_time_online_jeo = jdatetime.datetime.fromgregorian(datetime=last_time_online_timestamp).strftime('%H:%M:%S - %Y/%m/%d')
            else :
                last_time_online_jeo = 'هنوز متصل نشده'
            
            
            datetime_remaining = info['sub_request']['expire'] if info['sub_request']['expire'] is not None else 'None' 
            if datetime_remaining !='None':
                datetime_remaining= datetime.datetime.fromtimestamp(datetime_remaining)
                datetime_now = datetime.datetime.now()
                remianing_datetime = (datetime_remaining - datetime_now ).days
            else: 
                remianing_datetime = 'این اشتراک لایف تایم میباشد' 

            used_traffic = round(info['sub_request']['used_traffic'] / (1024 * 1024 * 1024) , 2) if info['sub_request']['used_traffic'] is not None else 'حجمی مصرف نشده'

            all_data_limit = info['sub_request']['data_limit'] / (1024 * 1024 * 1024) if info['sub_request']['data_limit']  is not None else 'ٔNone'
            if all_data_limit == 'ٔNone':
                all_data_limit = 'حجم اشتراک نامحدود میباشد'

            if info['sub_request']['data_limit']  is not None :

                all_expire_date = jdatetime.datetime.fromtimestamp(info['sub_request']['expire'])
            else :
                all_expire_date = 'این اشتراک لایف تایم میباشد'

            Text_2 = f"""
شما در حال مشاهده اشتراک <code>{ info['config_name']}</code> هستید

– #️⃣ایدی عددی خریدار : <code>{info['user_id']}</code>

● 🛍نام محصول : {product_info}
● 🎛پنل متصل شده : {panel_info}
● 💰مبلغ پرداختی : {format(payment_amount , ',')} تومان
● 📆آخرین اتصال : {str(last_time_online_jeo)}
● 🧮زمان باقی مانده : {remianing_datetime} روز
● 📅 زمان کلی : {str(all_expire_date)}
● ⌛️حجم مصرف شده : {str(used_traffic)} Gb
● 🔋 حجم کلی :‌ {str(all_data_limit)} Gb
.
"""         
            return Text_2
        except Exception as finding_user_sub:
            print(f'Error while finding user_sub \n error-msg : {finding_user_sub}')


