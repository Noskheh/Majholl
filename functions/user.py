from mainrobot.models import users 




#= check user existence
def CHECK_USER_EXITENCE(UserId , UserFirstName , UserLastName , UserUserName , UserWallet):

    try: 
        User_ = users.objects.get(user_id = UserId)
        if not User_ :
            return User_ , False   
        
    except users.DoesNotExist:
        User_ = users.objects.create(first_name = UserFirstName ,
                                    last_name = UserLastName,
                                    user_id = UserId ,
                                    username = UserUserName ,
                                    user_wallet = UserWallet) 
        return User_ , True 
