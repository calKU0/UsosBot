import json
    
def secrets(name):
    with open ("config.json") as config:
        secrets = json.load(config)
        return secrets[name.upper()]
        



    