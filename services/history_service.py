import os
import json
import uuid
import cv2
from ultralytics import YOLO
from config import HISTORY_FILE, UPLOAD_FOLDER

model = YOLO('models/uav.pt')

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

def get_history_details(record_id):
    history = load_history()
    for record in history:
        if record.get('id') == record_id:
            # 读取原始图片
            image_path = os.path.join(UPLOAD_FOLDER, record['image_url'].split('/', 1)[1])
            if os.path.exists(image_path):
                img = cv2.imread(image_path)
                if img is not None:
                    # 重新运行检测
                    results = model(img)
                    if results and len(results):
                        det = results[0]
                        names = det.names if hasattr(det, 'names') else model.names
                        detections = []
                        for box in det.boxes:
                            cls_id = int(box.cls[0])
                            cls_name = names[cls_id] if names and cls_id in names else str(cls_id)
                            conf = float(box.conf[0])
                            xyxy = [float(x) for x in box.xyxy[0].tolist()]
                            detections.append({
                                'class_id': cls_id,
                                'class_name': cls_name,
                                'confidence': conf,
                                'bbox': xyxy
                            })
                        
                        # 返回详细信息
                        return {
                            'id': record['id'],
                            'date': record['date'],
                            'image_url': record['image_url'],
                            'total_objects': record['total_objects'],
                            'avg_confidence': record['avg_confidence'],
                            'class_confidences': record['class_confidences'],
                            'detections': detections
                        }
    return None

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