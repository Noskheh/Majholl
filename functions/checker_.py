from mainrobot.models import v2panel , inovices , users
from datetime import datetime , timedelta


def check_capcity(panel_id = int):
    try : 
            panels_ = v2panel.objects.get(id = panel_id)
        
            if panels_.all_capcity > 0 :
                panels_.all_capcity -= 1
                panels_.sold_capcity += 1

                if panels_.all_capcity == 0:
                    panels_.capcity_mode = 0
                
                panels_.save()
    
    except Exception as error:
        print(f'An error occurred while checking capacity: {error}')
   
    


def check_time_passed(inovice_id : int):

    inovices_ = inovices.objects.get(id = inovice_id)
    created_date = str(inovices_.created_date)
    created_datetime = datetime.strptime(created_date ,  "%Y-%m-%d %H:%M:%S.%f")
    created_date_timstamp = created_datetime.timestamp()
    current_time = datetime.now().timestamp()
    check_30_min_pass = current_time - created_date_timstamp

    if check_30_min_pass >= 1800:
         return 'time_passed'
    else :
         return 'have-time'




def check_user_in_channel(userid , Bot):

    users_ = users.objects.get(user_id = userid)

    membership_status = Bot.get_chat_member('@vtwoNet' , users_.user_id).status
    
    if membership_status in ['member' , 'administrator' , 'creator'] :
            return True
    else :
            return False



