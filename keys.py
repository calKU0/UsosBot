import json
import oauth2 as oauth
from datetime import datetime

class authorization:      
    def consumer():
        return oauth.Consumer(oauth.secrets("consumer_key"), oauth.secrets("CONSUMER_SECRET"))
    
    def access_token(user, access_token):
        pass
        #operacja na bazie, aby znaleźć access token dla usera
        #Edit: Prawdopodobnie wywali circular refernce excepion więc ogarnąć inny sposób albo wyjebać tą funkcję
          
    def secrets(name):
        with open ("config.json") as config:
            secrets = json.load(config)
            return secrets[name.upper()]
        



    