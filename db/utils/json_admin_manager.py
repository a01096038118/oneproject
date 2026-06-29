import json, os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILE = os.path.join(BASE_DIR, 'json','admins.json' )

def load_admins():
    try:
        with open(FILE, encoding='utf-8') as f:
            return json.load(f)
        
    except:
        return {}
    

def save_admins(admins):
    with open(FILE,'w', encoding='utf-8') as f:
        json.dump(admins,
                  f,
                  ensure_ascii= False,
                  indent=4
                  )