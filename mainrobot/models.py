from django.db import models
from django.utils.timezone import now





class users(models.Model):
    first_name = models.CharField(max_length=256 , null=True)
    last_name = models.CharField(max_length=256 , null=True)
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=256 , null=True)
    user_wallet = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = 'TeleBot_users'



class channels(models.Model):
    channel_name = models.CharField(max_length=56)
    channel_url = models.CharField(max_length=256 , blank=True , null=True)
    channel_id = models.BigIntegerField(blank=True , null=True)

    class Meta:    
        db_table = 'TeleBot_channels'


class admins(models.Model):
    user_id = models.BigIntegerField()
    is_admin = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return f'User {self.user_id}: Admin={self.is_admin}, Owner={self.is_owner}'

    class Meta:
        db_table = 'TeleBot_admins'




class v2panel(models.Model):

    panel_name = models.CharField(max_length = 256 , blank = False)
    panel_url = models.CharField(max_length= 256 , blank = False)
    panel_username = models.CharField(max_length=256 , null=False)
    panel_password = models.CharField(max_length=256 , null= False)
    panel_id_str = models.CharField(max_length=36 , null= True , blank=True)
    reality_flow = models.CharField(max_length=256, null=True)
    panel_status = models.SmallIntegerField(default=1 , null=False)

    #-1 added 
    capcity_mode = models.PositiveSmallIntegerField(default= 2 , null=False)
    sold_capcity = models.BigIntegerField(default= 0 ,blank= True , null= True)
    panel_sale_mode = models.PositiveSmallIntegerField(default= 1 , null=False)
    send_links_mode = models.PositiveSmallIntegerField(default=0 , null=False)
    send_qrcode_mode = models.PositiveSmallIntegerField(default= 0 , null=False)
    inbounds_selected = models.JSONField(default=None , blank=True , null= True)

    #-2 changed
    all_capcity = models.BigIntegerField(default= 0 , blank= True , null= True)
    
    def __str__(self):
        return f'panel name :{self.panel_name }  panel url : {self.panel_url}'
    

    class Meta:
        db_table = 'TeleBot_v2panel'




class products(models.Model):
    #- change product_name max lenght
    product_name = models.CharField(max_length=128)
    data_limit = models.DecimalField(max_digits=12 , decimal_places=2 )
    expire_date = models.SmallIntegerField()
    pro_cost = models.BigIntegerField()
    panel_id = models.SmallIntegerField(null=True , blank=True)
    categori_id = models.SmallIntegerField(null=True, blank=True)
    pro_id_str = models.CharField(max_length=36 , null=True , blank=True)
    sort_id = models.SmallIntegerField(null=True , blank=True)

    class Meta :
        db_table = 'TeleBot_products'




class inovices(models.Model):

    paid_mode_choices = [
        ('wlt' , 'wallet') , 
        ('kbk' , 'kart-be-kart'),
        ('arz' , 'arz-digital')
    ]

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
    
    # later added
    config_name = models.CharField(max_length= 56 , blank= True , null= True)
    class Meta:
        db_table = 'TeleBot_inovices'

    


class payments(models.Model):
    user_id = models.ForeignKey( to = users , to_field='user_id' , on_delete= models.DO_NOTHING)
    amount = models.BigIntegerField()
    decline_reason = models.CharField(max_length= 256 , null=True , blank= True)
    payment_stauts = models.CharField(max_length = 56 , null=True , blank=True)
    inovice_id = models.ForeignKey(to = inovices , on_delete= models.DO_NOTHING ,null=True , blank= True)
    payment_time = models.DateTimeField(auto_now_add=True)

    class Meta :
        db_table = 'TeleBot_payments'