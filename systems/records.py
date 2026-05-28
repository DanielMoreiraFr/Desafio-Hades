import json
import os

FILE = os.path.join(os.path.dirname(__file__), "..", 'records.json')

def get_records_path() -> str:
    return os.path.abspath(FILE)

def load_records() -> list[dict]:
    try:
        with open(get_records_path(), encoding='utf-8') as loaded_file:
            return json.load(loaded_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def save_record(nickname: str, rooms: int) -> None:
    records = load_records()
    records.append({'nickname': nickname, 'rooms': rooms})
    records.sort(key=lambda r: r['rooms'], reverse= True)
    with open(get_records_path(), 'w', encoding='utf-8') as file:
        json.dump(records, file, ensure_ascii= False, indent= 2)