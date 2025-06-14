import os
from datetime import datetime
import cv2
import json
from config import UPLOAD_FOLDER, HISTORY_FILE
from services.history_service import load_history, save_history
import uuid
from model_config import get_model_instance, load_model_settings
import numpy as np
import time

# 缓存模型实例和上次加载时间
_model_cache = {
    'model': None,
    'settings': None,
    'path': None,
    'last_loaded': 0
}

# 模型缓存有效期（秒）
MODEL_CACHE_TTL = 300  # 5分钟

def get_cached_model():
    """获取缓存的模型实例，如果缓存过期或模型配置变更则重新加载"""
    current_time = time.time()
    settings = load_model_settings()
    model_path = settings['model']['path']
    
    # 检查是否需要重新加载模型
    if (_model_cache['model'] is None or 
        _model_cache['path'] != model_path or
        current_time - _model_cache['last_loaded'] > MODEL_CACHE_TTL):
        
        print(f"加载模型: {model_path}")
        model, model_settings = get_model_instance()
        _model_cache['model'] = model
        _model_cache['settings'] = model_settings
        _model_cache['path'] = model_path
        _model_cache['last_loaded'] = current_time
    else:
        print("使用缓存模型")
    
    return _model_cache['model'], _model_cache['settings']

def preprocess_image(image, target_size=None):
    """预处理图像，可选调整大小以加快处理速度"""
    if target_size and (image.shape[0] > target_size[0] or image.shape[1] > target_size[1]):
        # 保持宽高比的调整大小
        h, w = image.shape[:2]
        scale = min(target_size[0] / h, target_size[1] / w)
        new_size = (int(w * scale), int(h * scale))
        image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
        print(f"调整图像大小: {image.shape}")
    
    return image

def process_image_for_detection(file, app_config):
    """处理图像检测，使用缓存模型和优化的处理流程"""
    start_time = time.time()
    
    # 从缓存获取模型，避免重复加载
    model, model_settings = get_cached_model()
    
    filename = file.filename
    upload_path = os.path.join(app_config['UPLOAD_FOLDER'], filename)
    file.save(upload_path)

    # 读取并预处理图像
    img = cv2.imread(upload_path)
    if img is None:
        return None, "图像读取失败，请检查文件格式", [], {}
    
    # 对大图像进行预处理，限制最大尺寸为1920x1080
    img = preprocess_image(img, target_size=(1080, 1920))
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 使用模型配置中的设置进行检测
    detection_settings = model_settings['detection']
    
    # 设置优化参数
    results = model(
        img, 
        save=detection_settings['save_results'], 
        conf=model_settings['model']['confidence_threshold'],
        iou=model_settings['model']['iou_threshold'],
        line_width=detection_settings['line_width'],
        show_labels=detection_settings['show_labels'],
        show_conf=detection_settings['show_conf'],
        project=app_config['UPLOAD_FOLDER'], 
        name='detect', 
        exist_ok=True,
        verbose=False  # 减少不必要的输出
    )
    detect_dir = os.path.join(app_config['UPLOAD_FOLDER'], 'detect')

    result_img_url = None
    msg = None
    yolo_results = []
    stats = {}

    result_files = sorted(
        [f for f in os.listdir(detect_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))],
        key=lambda x: os.path.getctime(os.path.join(detect_dir, x)),
        reverse=True
    )
    if result_files:
        old_path = os.path.join(detect_dir, result_files[0])
        new_filename = f'detect_{timestamp}.jpg'
        new_path = os.path.join(detect_dir, new_filename)
        os.rename(old_path, new_path)
        result_img_url = f'results/detect/{new_filename}'

        class_confidences = {}
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            cls_name = model.names[cls_id]
            conf = float(box.conf[0])
            if cls_name not in class_confidences:
                class_confidences[cls_name] = []
            class_confidences[cls_name].append(conf)

        avg_confidences = {
            cls: sum(confs) / len(confs) if confs else 0
            for cls, confs in class_confidences.items()
        }

        # 异步保存历史记录，不阻塞主流程
        def save_history_async():
            history = load_history()
            history.append({
                'id': str(uuid.uuid4()),
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'image_url': result_img_url,
                'total_objects': len(results[0].boxes),
                'main_classes': list(set([model.names[int(box.cls[0])] for box in results[0].boxes])),
                'avg_confidence': sum(avg_confidences.values()) / len(avg_confidences) if avg_confidences else 0,
                'class_confidences': avg_confidences,
                'status': 'success'
            })
            save_history(history)
        
        # 在生产环境中，这里可以使用线程池或异步任务队列
        # 但为了简单起见，我们暂时不做异步处理
        save_history_async()
    else:
        msg = "检测失败，未生成结果图片。"

    if results and len(results):
        det = results[0]
        names = det.names if hasattr(det, 'names') else model.names
        yolo_results = []
        class_count = {}
        total_confidence = 0
        total_area = 0
        for box in det.boxes:
            cls_id = int(box.cls[0])
            cls_name = names[cls_id] if names and cls_id in names else str(cls_id)
            conf = float(box.conf[0])
            xyxy = [float(x) for x in box.xyxy[0].tolist()]
            area = (xyxy[2] - xyxy[0]) * (xyxy[3] - xyxy[1])
            total_confidence += conf
            total_area += area
            yolo_results.append({
                'class_id': cls_id,
                'class_name': cls_name,
                'confidence': conf,
                'bbox': xyxy,
                'area': area
            })
            class_count[cls_name] = class_count.get(cls_name, 0) + 1

        avg_confidence = total_confidence / len(yolo_results) if yolo_results else 0
        avg_area = total_area / len(yolo_results) if yolo_results else 0
        stats = {
            'total': len(yolo_results),
            'class_count': class_count,
            'avg_confidence': avg_confidence,
            'avg_area': avg_area,
            'max_confidence': max([r['confidence'] for r in yolo_results]) if yolo_results else 0,
            'min_confidence': min([r['confidence'] for r in yolo_results]) if yolo_results else 0,
            'processing_time': round(time.time() - start_time, 2)  # 添加处理时间统计
        }

    return result_img_url, msg, yolo_results, stats 