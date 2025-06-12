import os
import json
import uuid # 导入 uuid 模块
from config import HISTORY_FILE, UPLOAD_FOLDER

def load_history():
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)

    updated = False
    for record in history:
        if 'id' not in record:
            record['id'] = str(uuid.uuid4())
            updated = True
            
    if updated:
        save_history(history)
        
    return history

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def delete_history_record(record_id):
    history = load_history()
    original_len = len(history)
    updated_history = []
    deleted_file_path = None

    for record in history:
        if record.get('id') == record_id:
            image_url = record.get('image_url')
            if image_url:
                relative_path = image_url.split('/', 1)[1] if '/' in image_url else image_url
                file_to_delete = os.path.join(UPLOAD_FOLDER, relative_path)
                if os.path.exists(file_to_delete):
                    try:
                        os.remove(file_to_delete)
                        deleted_file_path = file_to_delete
                        print(f"Deleted image file: {file_to_delete}")
                    except Exception as e:
                        print(f"Error deleting image file {file_to_delete}: {e}")
                else:
                    print(f"Image file not found: {file_to_delete}")
        else:
            updated_history.append(record)

    if len(updated_history) < original_len:
        save_history(updated_history)
        return True, "记录删除成功", deleted_file_path
    else:
        return False, "未找到指定记录或删除失败", None 