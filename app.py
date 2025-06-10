import os
from datetime import datetime
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import cv2
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/results'
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'detect'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'history'), exist_ok=True)

# 加载模型
model = YOLO('yolov9c.pt')

# 历史记录文件路径
HISTORY_FILE = 'detection_history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    result_img_url = None
    msg = None
    yolo_results = []
    stats = {}
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].filename == '':
            msg = "请上传一张图片！"
        else:
            file = request.files['file']
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)

            # 目标检测
            img = cv2.imread(upload_path)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            results = model(img, save=True, project=app.config['UPLOAD_FOLDER'], name='detect', exist_ok=True)
            detect_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'detect')
            
            # 重命名最新的检测结果文件
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
                
                # 保存到历史记录
                history = load_history()
                history.append({
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'image_url': result_img_url,
                    'total_objects': len(results[0].boxes),
                    'main_classes': list(set([model.names[int(box.cls[0])] for box in results[0].boxes]))
                })
                save_history(history)
            else:
                msg = "检测失败，未生成结果图片。"

            # YOLO详细结果
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
                
                # 计算更多统计信息
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

    return render_template('index.html', result_img_url=result_img_url, msg=msg, yolo_results=yolo_results, stats=stats)

@app.route('/history')
def history():
    history_records = load_history()
    return render_template('history.html', history_records=history_records)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)