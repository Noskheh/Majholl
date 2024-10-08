from django.db import models
from django.utils.timezone import now





class users(models.Model):
    first_name = models.CharField(max_length=256, null=True)
    last_name = models.CharField(max_length=256, null=True)
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=256, null=True)
    user_wallet = models.DecimalField(max_digits=18, decimal_places=2)
    # / -1
    block_reason = models.CharField(max_length=126, blank=True, null=True)
    block_status = models.BooleanField(default=0)
    # / -2
    phone_number = models.CharField(max_length=54, blank=True, null=True)

    class Meta:
        db_table = 'v2_users'





class admins(models.Model):
    user_id = models.BigIntegerField()
    admin_name = models.CharField(max_length=128 , null=True , blank=True)
    is_admin = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    password = models.CharField(max_length=128 , null=True , blank=True)
    acc_panels = models.BooleanField(default=False)
    acc_products = models.BooleanField(default=False)
    acc_botmanagment = models.BooleanField(default=False)
    acc_admins = models.BooleanField(default=False)
    acc_users = models.BooleanField(default=False)
    acc_staticts = models.BooleanField(default=False)

    def __str__(self):
        return f'User {self.user_id}: Admin={self.is_admin}, Owner={self.is_owner}'


    class Meta:
        db_table = 'v2_admins'




class v2panel(models.Model):
    panel_status = models.SmallIntegerField(default=1 , null=False)
    panel_name = models.CharField(max_length = 256 , blank = False)
    panel_url = models.CharField(max_length= 256 , blank = False)
    panel_username = models.CharField(max_length=256 , null=False)
    panel_password = models.CharField(max_length=256 , null= False)
    panel_id_str = models.CharField(max_length=36 , null= True , blank=True)
    reality_flow = models.CharField(max_length=256, null=True)
    capcity_mode = models.PositiveSmallIntegerField(default= 2 , null=False)
    all_capcity = models.BigIntegerField(default= 0 , blank= True , null= True)
    sold_capcity = models.BigIntegerField(default= 0 ,blank= True , null= True)
    panel_sale_mode = models.PositiveSmallIntegerField(default= 1 , null=False)
    send_links_mode = models.PositiveSmallIntegerField(default=0 , null=False)
    send_qrcode_mode = models.PositiveSmallIntegerField(default= 0 , null=False)
        
    def __str__(self):
        return f'panel name :{self.panel_name }  panel url : {self.panel_url}'
    

    class Meta:
        db_table = 'v2_v2panel'




class products(models.Model):
    product_status = models.SmallIntegerField(default=1 , null=False)
    product_name = models.CharField(max_length=128)
    data_limit = models.DecimalField(max_digits=12 , decimal_places=2 )
    expire_date = models.SmallIntegerField()
    pro_cost = models.BigIntegerField()
    panel_id = models.SmallIntegerField(null=True , blank=True)
    categori_id = models.SmallIntegerField(null=True, blank=True)
    pro_id_str = models.CharField(max_length=36 , null=True , blank=True)
    sort_id = models.SmallIntegerField(null=True , blank=True)
    inbounds_selected = models.JSONField(default=None , blank=True , null= True)
    class Meta :
        db_table = 'v2_products'




class inovices(models.Model):

    paid_mode_choices = [
                        ('wlt' , 'wallet') , 
                        ('kbk' , 'kart-be-kart'),
                        ('arz' , 'arz-digital')]

    user_id = models.ForeignKey(to = users , to_field='user_id' , on_delete= models.DO_NOTHING)
    user_username = models.CharField(max_length = 56 , null = True , blank = True)
    panel_name = models.CharField(max_length = 56 )
    product_name = models.CharField(max_length = 56)
    data_limit = models.DecimalField(max_digits = 12 , decimal_places = 2 )
    expire_date = models.SmallIntegerField()
    pro_cost = models.BigIntegerField()
    gift_code = models.CharField(max_length = 56 , blank= True , null = True)
    discount = models.BigIntegerField(default = 0 , blank = True , null = True)
    created_date = models.DateTimeField(auto_now_add=True )
    paid_status = models.PositiveBigIntegerField(default = 0)
    paid_mode = models.CharField(max_length = 3 , choices = paid_mode_choices)
    
    # / -1
    config_name = models.CharField(max_length= 56 , blank= True , null= True)
    kind_pay = models.CharField(max_length=12 , blank=True , null=True)
    
    class Meta:
        db_table = 'v2_inovices'

    


class payments(models.Model):
    user_id = models.ForeignKey( to = users , to_field='user_id' , on_delete= models.DO_NOTHING)
    amount = models.BigIntegerField()
    decline_reason = models.CharField(max_length= 256 , null=True , blank= True)
    payment_status = models.CharField(max_length = 56 , null=True , blank=True)
    inovice_id = models.ForeignKey(to = inovices , on_delete= models.DO_NOTHING ,null=True , blank= True)
    payment_time = models.DateTimeField(auto_now_add=True)

    class Meta :
        db_table = 'v2_payments'





class subscriptions(models.Model):
    user_id = models.ForeignKey(to=users , to_field='user_id' , on_delete=models.DO_NOTHING)
    user_subscription = models.CharField(max_length=56)
    product_id = models.ForeignKey(to=products, blank=True, null=True, on_delete=models.DO_NOTHING)
    panel_id = models.ForeignKey(to=v2panel , blank=True, null=True, on_delete= models.DO_NOTHING)
    date_created= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'v2_subscriptions'















# -------------- > Bot-Settings < -------------- 

class botsettings(models.Model):
    #- 1
    wallet_pay = models.SmallIntegerField(default=0 , null=False)
    kartbkart_pay = models.SmallIntegerField(default= 0 , null=False)
    moneyusrtousr = models.SmallIntegerField(default=0 , null=False)
    forcechjoin = models.SmallIntegerField(default=0 , null=False)
    #- 2
    irnumber = models.SmallIntegerField(default=0 , null=False)
    #- 3
    newusers_notf = models.SmallIntegerField(default=0 , null=False)
    walletcharge_notf = models.SmallIntegerField(default=0 , null=False)
    moneyusrtousr_notf = models.SmallIntegerField(default=0 , null=False)
    buyservice_notf = models.SmallIntegerField(default=0 , null=False)
    tamdidservice_notf = models.SmallIntegerField(default=0 , null=False)

    class Meta:
        db_table = 'v2_botsettings'



class shomarekart(models.Model):
    bank_name = models.CharField(max_length=56 , null=True , blank= True)
    ownername = models.CharField(max_length=124 , null= True , blank=True)
    bank_card = models.BigIntegerField(null=True , blank=True)
    bank_status = models.SmallIntegerField(default= 1 , null=False)
    bank_inmsg = models.SmallIntegerField(default=0 , null=False)
    class Meta:
        db_table = 'v2_shomarekart'




class channels(models.Model):

    ch_usage_choices = [('logc' , 'logs_channel') ,
                        ('fjch' , 'force_join_channel')]
    
    channel_name = models.CharField(max_length=56)
    channel_url = models.CharField(max_length=256 , blank=True , null=True)
    channel_id = models.BigIntegerField(blank=True , null=True)
    ch_status = models.SmallIntegerField(default=0 , null=False)
    ch_usage = models.CharField(max_length=4 , choices=ch_usage_choices ,blank=True , null=True)
    class Meta:    
        db_table = 'v2_channels'
