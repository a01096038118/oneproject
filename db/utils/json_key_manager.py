import json, os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILE = os.path.join(BASE_DIR, 'json','keys.json' )

def load_admin_keys():
    try:
        with open(FILE, encoding='utf-8') as f:
            return json.load(f)
        
    except:
        return {}
    

def save_admin_keys(keys):
    with open(FILE,'w', encoding='utf-8') as f:
        json.dump(keys,
                  f,
                  ensure_ascii= False,
                  indent=4
                  )