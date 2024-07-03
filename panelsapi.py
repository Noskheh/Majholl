from mainrobot.models import v2panel , products
import requests , uuid , json , datetime


#//TODO add try/exception for api

class marzban:

    def __init__(self , panel_id:int ):
        panel_ = v2panel.objects.get(id = panel_id)
        self.panel_url = panel_.panel_url
        self.panel_username = panel_.panel_username
        self.panel_password = panel_.panel_password
        self.reality_flow = panel_.reality_flow

    def get_token_acces(self ):
        panel_url = self.panel_url + '/api/admin/token'
        req = requests.post(panel_url , data={'username':self.panel_username , 'password' :self.panel_password})

        if req.status_code == 200:
            Token = json.loads(req.content)['access_token']
            header_info = {'Authorization': f"bearer {Token}"}
            return header_info
        else:
            return False


    def add_user(self , username , data_limit , date_expire):
        #- https://marzban:port/api/user
        panel_url = self.panel_url + '/api/user'
        #موقعه خرید محصول باید اینباند ها رو لود کنیم
         #, product_id:int=None
        # products_ = products.objects.get()

        #proxies 
        current_time = datetime.datetime.now()
        expire_time = current_time + datetime.timedelta(days = date_expire)
        reality = self.reality_flow if self.reality_flow else ""
        proxy_dict ={
            "username": username,
            "proxies": {"vmess": {"id": str(uuid.uuid4())},"vless": {'flow': reality}},
            "inbounds": json.loads(self.inbounds),
            "expire": datetime.datetime.timestamp(expire_time),
            "data_limit": data_limit * 1024 * 1024 * 1024,
            "data_limit_reset_strategy": "no_reset",
            "status": "active",
            "note": "",
            "on_hold_timeout": "2023-11-03T20:30:00",
            "on_hold_expire_duration": 0
                }
        get_header = marzban.get_token_acces(self)
        add_user_request = requests.post(panel_url , json= proxy_dict , headers= get_header)
        
        if add_user_request.status_code == 200:
            return json.loads(add_user_request.content)
        else :
            return False


    def get_inbounds(self):
        panel_url = self.panel_url + '/api/inbounds'
        get_headr = marzban.get_token_acces(self)
        get_inbouns_requsts = requests.get(panel_url , headers=get_headr)
        return json.loads(get_inbouns_requsts.content)



