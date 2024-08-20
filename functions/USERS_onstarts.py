from mainrobot.models import users , channels , botsettings
from keybuttons import BotkeyBoard as botkb
#handles welcome functions
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
def FORCE_JOIN_CHANNEL(UserId, Bot):
    Users_ = users.objects.get(user_id=UserId)
    Channels_ = channels.objects.all()
    botsettings_forcech= botsettings.objects.all()[0].forcechjoin
    state = {}
    
    for i in Channels_:
        if botsettings_forcech == 1 :
            Membership_ = Bot.get_chat_member(i.channel_url or i.channel_id, Users_.user_id).status
            state[i.channel_id] = Membership_


    # Check all membership statuses
    for membership_status in state.values():
        if membership_status == 'left' and botsettings_forcech == 1 :
            return botkb.load_channels(Bot , UserId)
    
    return True