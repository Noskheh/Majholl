from mainrobot.models import v2panel , products 
from keybuttons import BotkeyBoard as BotKb
import random , string , json , re
#this is functions that managing producs




#-Adding panel to Database
def add_product_database(call , BOT , product_dict , inbouds_dict):
    product_id_STRgenerated = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4))
    products_obejcts = [i.id for i in products.objects.all()] 
            
    try:
        product_=products.objects.create(product_name=product_dict['Product_Name'] , data_limit=product_dict['Data_Limit'] ,
                                        expire_date=product_dict['Expire_Date'] , pro_cost=product_dict['Product_Cost'] ,
                                        panel_id=product_dict['Panel_Id'] , pro_id_str=product_id_STRgenerated ,
                                        sort_id=max(products_obejcts)+1 if products_obejcts else 1 , inbounds_selected= json.dumps(inbouds_dict , indent=1))
        product_dict.update({key : '' for key in product_dict})
        Text_2='✅پنل با موفقیت به دیتابیس اضافه شد'
        BOT.edit_message_text(Text_2 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.product_management_menu_in_admin_side())
                
    except Exception as product_creation:
        print(f'Error during creating product \n\t Error-msg : {product_creation}')
        Text_1='❌یک مشکلی در هنگام اضافه کردن محصول به وجود امد\n مجدد امتحان کنید'
        BOT.send_message(call.message.chat.id , Text_1)         




#-Deleting panel from Database
def remove_product_database(call ,  BOT , product_id , panel_id_dict):
    product_to_remove=products.objects.get(id = product_id)  
    pro_name=product_to_remove.product_name        
    try:
        product_to_remove.delete()
    except Exception as remove_product:
        print(f'Error during removing product \n Error_msg : {remove_product}')
        Text_1=f'هنگام حذف کردن محصول از دیتابیس مشکلی بوجود امد \n{remove_product}'
        BOT.send_message(call.message.chat.id , Text_1 ,reply_markup=BotKb.product_managemet_remove_products(panel_pk=panel_id_dict['Panel_Id']))
    else:
        Text_2=f'محصول با موفقیت از دیتابیس پاک شد ✅\n\n  نام محصول حذف شده  : {pro_name}'
        BOT.edit_message_text(Text_2 ,call.message.chat.id ,call.message.message_id , reply_markup=BotKb.product_managemet_remove_products(panel_pk=panel_id_dict['Panel_Id']))
            






#-Managing product from Database
#- product_STATUS 
def change_product_status(call , BOT , product_id):
    try :
        product_ = products.objects.get(id = product_id)
        product_status = int
        if product_.product_status ==1:
            product_status = 0
        else :
            product_status = 1 
        product_.product_status=product_status
        product_.save() 
        show_status = '🟢فعال ' if product_status ==1 else "🔴 غیر فعال"
        Text_1=f'وضعیت محصول تغییر کرد \n وضعیت فعلی محصول : {show_status}'
        BOT.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=BotKb.product_changing_details(product_id))
    except Exception as change_product_status:
        print(f'Error during changing product status \n\n Error-msg : {change_product_status}')
    


#- product_NAME
def change_product_name(message , BOT , product_dict , product_id):
    if product_dict['Product_Name'] == True and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        product_dict['Product_Name'] = False
        Text_1='🖋برای تغییر تنظیمات  محصول بر روی آن کلیک کنید'
        BOT.send_message(message.chat.id , Text_1 , reply_markup=BotKb.product_changing_details(product_id=product_id['Product_Id']))
    else: 
        if len(message.text) <= 64: 
            try: 
                product_ = products.objects.get(id = product_id['Product_Id'])
                product_new_name = message.text
                product_.product_name = product_new_name
                product_.save()
                product_dict['Product_Name'] = False
            except Exception as change_prodcuct_name :
                print(f'Error during changing product name \n\t Error-msg : {change_prodcuct_name}')
            Text_2='🖋برای تغییر تنظیمات  محصول بر روی آن کلیک کنید\n نام محصول تغییر کرد'
            BOT.send_message(message.chat.id , Text_2 , reply_markup =BotKb.product_changing_details(product_id =product_id['Product_Id']))
        else :
            Text_3='اسم محصول نباید بیشتر از ۶۴ حرف یا کرکتر باشد \n مجدد امتحان نمایید'
            BOT.send_message(message.chat.id , Text_3)





#- Product_data-limit
def change_product_datalimt(message , BOT , product_dict , product_id):
    if product_dict['Data_Limit']==True and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        product_dict['Data_Limit'] = False
        Text_1='🖋برای تغییر تنظیمات  محصول بر روی آن کلیک کنید'
        BOT.send_message(message.chat.id , Text_1 , reply_markup=BotKb.product_changing_details(product_id=product_id['Product_Id']))
    else:
        if message.text.isdigit():
            data_limit_checker=re.search(r'([0-9]{1,9}|[0-9]{1,9}\.[0-9]{0,3})' , message.text)
            if data_limit_checker: 
                try: 
                    product_=products.objects.get(id = product_id['Product_Id'])
                    product_new_datalimit = data_limit_checker.group(0)
                    product_.data_limit = product_new_datalimit
                    product_.save()        
                    product_dict['Data_Limit'] = False
                except Exception as change_data_limit :
                    print(f'Error during changing product data limit \n\n Error-msg : {change_data_limit}')
                Text_2='🖋برای تغییر تنظیمات هر محصول بر روی آن کلیک کنید\n حجم محصول تغییر کرد'
                BOT.send_message(message.chat.id , Text_2 ,reply_markup=BotKb.product_changing_details(product_id=product_id['Product_Id']))   
            else :
                Text_3='فرمت ارسالی اشتباه میباشد مقادیر اعشاری را امتحان کنید \n مانند : 10.0 یا 20.00\n\nTO CANCEL : /CANCEL'
                BOT.send_message(message.chat.id ,Text_3 , reply_markup = BotKb.product_changing_details(product_id = product_id['Product_Id']))       
        else :
            Text_3='مقدار ورود باید به صورت عدد باشد \n\nTO CANCEL : /CANCEL'
            BOT.send_message(message.chat.id , Text_3)






#- prdouct_expire-date
def change_prdocut_expiredate(message , BOT , product_dict , product_id):
    if product_dict['Expire_Date']==True and (message.text=='/cancel' or message.text=='/cancel'.upper()):
            product_dict['Expire_Date'] = False
            Text_1='🖋برای تغییر تنظیمات  محصول بر روی آن کلیک کنید'
            BOT.send_message(message.chat.id , Text_1 , reply_markup =BotKb.product_changing_details(product_id =product_id['Product_Id']))
    else :
        if message.text.isdigit() :
            try : 
                product_ = products.objects.get(id = product_id['Product_Id'])
                product_new_expiredate = message.text
                product_.expire_date = product_new_expiredate
                product_.save()
                product_dict['Expire_Date'] = False
            except Exception as change_expire_date :
                    print(f'Error during changing product data limit \n\n Error-msg : {change_expire_date}')
            Text_2='🖋برای تغییر تنظیمات  محصول بر روی آن کلیک کنید\n دوره محصول تغییر کرد'
            BOT.send_message(message.chat.id , Text_2 , reply_markup=BotKb.product_changing_details(product_id=product_id['Product_Id']))
        else : 
            Text_3='مقدار ورود باید به صورت عدد باشد \n\nTO CANCEL : /CANCEL'
            BOT.send_message(message.chat.id , Text_3)                        
    



#- prodcut_cost
def change_product_cost(message , BOT , product_dict , product_id):
    if product_dict['Product_Cost']==True and (message.text=='/cancel' or message.text=='/cancel'.upper()):
        product_dict['Product_Cost'] = False
        Text_1='🖋برای تغییر تنظیمات هر محصول بر روی آن کلیک کنید'
        BOT.send_message(message.chat.id , Text_1 , reply_markup=BotKb.product_changing_details(product_id=product_id['Product_Id']))
    else :  
        if message.text.isdigit():
            try : 
                product_ = products.objects.get(id = product_id['Product_Id'])
                product_new_pro_cost = message.text
                product_.pro_cost = product_new_pro_cost
                product_.save()
                product_dict['Product_Cost'] = False
            except Exception as change_product_cost :
                print(f'Error during changing product pro cost \n\n Error-msg : {change_product_cost}')
            Text_2='🖋برای تغییر تنظیمات هر محصول بر روی آن کلیک کنید\n دوره محصول تغییر کرد'
            BOT.send_message(message.chat.id , Text_2 , reply_markup = BotKb.product_changing_details(product_id = product_id['Product_Id']))
        else : 
            Text_3='مقدار ورود باید به صورت عدد باشد \n\nTO CANCEL : /CANCEL'
            BOT.send_message(message.chat.id , Text_3)                        



#- product_inbound 
def change_product_inbound(call , BOT , inbounds):
    if  (inbounds['inbounds'] is not None and call.data in inbounds['inbounds']):
        inbounds_list=inbounds['inbounds']
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
        for i in inbounds['inbounds']:
            if  '✅' in i:
                inbounds_checkmark.append(i.strip('✅'))
            Text_1=f"لیست اینباند های انتخابی:\n\n {inbounds_checkmark}"
        keyboard = BotKb.change_inbounds(inbounds_list) 
        BOT.edit_message_text(Text_1 , call.message.chat.id , call.message.message_id , reply_markup=keyboard)


