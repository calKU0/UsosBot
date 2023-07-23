from replit import Database
import json

class Operations:
    def __init__(self) -> None:
        self.db = Database(db_url="https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsImlzcyI6ImNvbm1hbiIsImtpZCI6InByb2Q6MSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb25tYW4iLCJleHAiOjE2OTAyMjM3NzUsImlhdCI6MTY5MDExMjE3NSwiZGF0YWJhc2VfaWQiOiJiY2ZiYTQwYS03ZTMxLTQ1MmEtYTBjMi03ZmE0ZTBiNDE5MjAiLCJ1c2VyIjoiS3J6eXN6dG9mS3Vyb3dzIiwic2x1ZyI6IlVzb3NCb3QifQ.gxntgwcqoL4n_hxWoFjmu6fBS_r_iE77DUgx_ZXfTa8UOBogHzsfHm9RwRLf_12pmEss8SflvhLtYOWxBqyVRw")
        
    def registered(self, user_id):
        for user in self.db["Users"]:
            if user.get("user_id") == user_id:
                return True
        return False

    def add_user(self, user_id, name, access_token, registration_date):
        max_id = max(user.get("GID", 1) for user in self.db.get("Users", []))
        new_user = {
            "GID": max_id + 1,
            "user_id": user_id, 
            "name": name,
            "access_token": str(access_token),
            "registration_date": registration_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        serialized_data = json.dumps(new_user)
        self.db["Users"].append(serialized_data)
        
    def modify_user(self, user_id, name=None, access_token=None, registration_date=None):
        for user in self.db.get("Users", []):
            user_dict = json.loads(user)
            if user_dict.get("user_id") == user_id:
                user_to_modify = user_dict
                break

        if name is not None:
            user_to_modify["name"] = name
        if access_token is not None:
            user_to_modify["access_token"] = str(access_token)
        if registration_date is not None:
            user_to_modify["registration_date"] = registration_date.strftime('%Y-%m-%d %H:%M:%S')

        serialized_user = json.dumps(user_to_modify)
        for i, user in enumerate(self.db["Users"]):
            if json.loads(user)["user_id"] == user_id:
                self.db["Users"][i] = serialized_user
                break

        return True
            