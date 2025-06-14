import os
import json
import uuid
import cv2
from config import HISTORY_FILE, UPLOAD_FOLDER
from model_config import get_model_instance

# 历史记录缓存
_history_cache = None
_history_cache_dirty = False

def load_history():
    """加载历史记录，使用缓存减少IO操作"""
    global _history_cache, _history_cache_dirty
    
    # 如果缓存有效且未修改，直接返回缓存
    if _history_cache is not None and not _history_cache_dirty:
        return _history_cache.copy()
    
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except Exception as e:
            print(f"加载历史记录出错: {e}")
            history = []

    updated = False
    for record in history:
        if 'id' not in record:
            record['id'] = str(uuid.uuid4())
            updated = True
            
    if updated:
        save_history(history)
    
    # 更新缓存
    _history_cache = history.copy()
    _history_cache_dirty = False
        
    return history

def save_history(history):
    """保存历史记录，更新缓存状态"""
    global _history_cache, _history_cache_dirty
    
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        
        # 更新缓存
        _history_cache = history.copy()
        _history_cache_dirty = False
        return True
    except Exception as e:
        print(f"保存历史记录出错: {e}")
        _history_cache_dirty = True
        return False

def get_history_details(record_id):
    # 每次获取详细信息时获取最新的模型实例和设置
    model, model_settings = get_model_instance()
    
    history = load_history()
    for record in history:
        if record.get('id') == record_id:
            # 读取原始图片
            image_path = os.path.join(UPLOAD_FOLDER, record['image_url'].split('/', 1)[1])
            if os.path.exists(image_path):
                img = cv2.imread(image_path)
                if img is not None:
                    # 使用模型配置中的设置进行检测
                    detection_settings = model_settings['detection']
                    results = model(
                        img,
                        conf=model_settings['model']['confidence_threshold'],
                        iou=model_settings['model']['iou_threshold'],
                        verbose=False
                    )
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