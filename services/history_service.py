import os
import json
import uuid # 导入 uuid 模块
from config import HISTORY_FILE, UPLOAD_FOLDER

def load_history():
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    
    # 检查并为没有ID的历史记录添加ID
    updated = False
    for record in history:
        if 'id' not in record:
            record['id'] = str(uuid.uuid4())
            updated = True
            
    if updated:
        save_history(history) # 保存更新后的历史记录
        
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
            # 找到要删除的记录，删除对应的图片文件
            image_url = record.get('image_url')
            if image_url:
                # image_url 是类似 'results/detect/detect_TIMESTAMP.jpg'
                # 需要构建完整的绝对路径
                # 从 image_url 中提取相对路径部分，例如 'results/detect/detect_TIMESTAMP.jpg'
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