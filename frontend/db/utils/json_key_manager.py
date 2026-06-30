import json, os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILE = os.path.join(BASE_DIR, 'json','keys.json' )

def load_admins_key():
    try:
        with open(FILE, encoding='utf-8') as f:
            return json.load(f)
        
    except:
        return {}
    

def save_admins_key(keys):
    with open(FILE,'w', encoding='utf-8') as f:
        json.dump(keys,
                  f,
                  ensure_ascii= False,
                  indent=4
                  )