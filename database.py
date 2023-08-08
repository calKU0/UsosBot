from replit import Database
import json
import keys
import oauth2 as oauth

class operations:
    def __init__(self) -> None:
        self.db = Database(db_url=keys.secrets("database"))
        print(self.db["Users"])
        
    def registered(self, user_id):
        parsed_list = [json.loads(item) if isinstance(item, str) else item for item in self.db["Users"]]
        return any(entry.get('user_id') == user_id for entry in parsed_list)

    def add_user(self, user_id, name, access_token, collage_name, endpoint, registration_date):
        max_id = max(user.get("GID", 1) for user in self.db.get("Users", []))
        new_user = {
            "GID": max_id + 1,
            "user_id": user_id, 
            "name": name,
            "access_token": str(access_token),
            "college_name": str(collage_name),
            "endpoint": str(endpoint),
            "registration_date": registration_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        serialized_data = json.dumps(new_user)
        self.db["Users"].append(serialized_data)
        
    '''def new_database(self):
        self.db["Users"] = [{
           "GID": 1,
           "user_id": 1,
           "name": "test",
           "access_token": 1234,
           "college_name": "test",
           "endpoint": "test",
           "registration_date":124
        }]'''

    def modify_user(self, user_id, name = None, access_token = None, collage_name = None, endpoint = None, registration_date = None):
        parsed_list = [json.loads(item) if isinstance(item, str) else item for item in self.db["Users"]]
        for entry in parsed_list:
            if 'user_id' in entry and entry['user_id'] == user_id:
                entry['name'] = name
                entry['access_token'] = access_token
                entry['collage_name'] = collage_name
                entry['endpoint'] = endpoint
                entry['registration_date'] = registration_date.strftime('%Y-%m-%d %H:%M:%S')
                break
    
    def select(self, user_id, key):
        parsed_list = [json.loads(item) if isinstance(item, str) else item for item in self.db["Users"]]
        for entry in parsed_list:
            if "user_id" in entry and entry["user_id"] == user_id:
                if key != "access_token":
                    return entry[f"{key}"]
                else:
                    token_parts = entry["access_token"].split('&')
                    for part in token_parts:
                        if part.startswith('oauth_token='):
                            oauth_token = part[len('oauth_token='):]
                        elif part.startswith('oauth_token_secret='):
                            oauth_token_secret = part[len('oauth_token_secret='):]
                    return oauth_token, oauth_token_secret
        return None
            
    def consumer(self):
        return oauth.Consumer(keys.secrets("consumer_key"), keys.secrets("CONSUMER_SECRET"))
    
    
            