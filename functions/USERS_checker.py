from mainrobot.models import users , channels


#= check user existence
def CHECK_USER_EXITENCE(UserId , UserFirstName , UserLastName , UserUserName , UserWallet):
    try: 
        User_ = users.objects.get(user_id = UserId)
        if not User_ :
            return User_ , False   
        
    except users.DoesNotExist:
        User_ = users.objects.create(first_name=UserFirstName , last_name=UserLastName , user_id=UserId , username=UserUserName ,
                                    user_wallet=UserWallet) 
        
        return User_ , True 


#= check user in channel or not
def CHECK_USER_CHANNEL(UserId , Bot):

    Users_ = users.objects.get(user_id=UserId)
    Channels_ = channels.objects.all()
    
    for i in Channels_:
        Membership_status = Bot.get_chat_member(i.channel_url or i.channel_id , Users_.user_id).status
    
    if Membership_status in ['member' , 'administrator' , 'creator'] :
            return True
    else :
            return False