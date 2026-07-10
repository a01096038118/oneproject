import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILE = os.path.join(BASE_DIR, 'json', "critical_errors.json")

def load_errors():
    try:
        with open(FILE, encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}
    
def save_errors(critical_errors):
    
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(
            critical_errors,
            f,
            ensure_ascii= False,
            indent=4
        )