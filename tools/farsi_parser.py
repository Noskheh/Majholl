farsi_list = ['ا' , 'ب' , 'پ' , 'ت' , 'ث' , 'ج' , 'چ' , 'ح' , 'خ' , 'د', '‌ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ه' , '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '۰' ,'ی' ]
#//TODO 
# حرف ذ را رد میکند 

def parse_farsi(txt : str ):
    txt_list = []
    for i in txt :
        txt_list.append(i)
    
    for txt_parse in txt_list:
        if txt_parse in farsi_list:  
            print('yes') 
            return True
        
    return False


