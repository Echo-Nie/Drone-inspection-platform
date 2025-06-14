import os
from datetime import datetime
import cv2
import json
from ultralytics import YOLO
from config import UPLOAD_FOLDER, HISTORY_FILE
from services.history_service import load_history, save_history
import uuid

model = YOLO('models/uav.pt')

def process_image_for_detection(file, app_config):
    filename = file.filename
    upload_path = os.path.join(app_config['UPLOAD_FOLDER'], filename)
    file.save(upload_path)

    img = cv2.imread(upload_path)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results = model(img, save=True, project=app_config['UPLOAD_FOLDER'], name='detect', exist_ok=True)
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
            'min_confidence': min([r['confidence'] for r in yolo_results]) if yolo_results else 0
        }

    return result_img_url, msg, yolo_results, stats 