from flask import Blueprint, render_template, request, current_app, jsonify
from services.detection_service import process_image_for_detection
from model_config import get_model_instance, get_available_models, load_model_settings, save_model_settings
import os
from werkzeug.utils import secure_filename
from model_config import MODELS_DIR
import time

main_bp = Blueprint('main', __name__)

@main_bp.route('/index', methods=['GET', 'POST'])
def index():
    start_time = time.time()
    result_img_url = None
    msg = None
    yolo_results = []
    stats = {}
    
    # 获取可用模型和当前模型设置
    available_models = get_available_models()
    model_settings = load_model_settings()
    current_model_path = model_settings['model']['path']
    
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].filename == '':
            msg = "请上传一张图片！"
        else:
            # 获取选择的模型和置信度
            model_name = request.form.get('model_name')
            confidence = request.form.get('confidence')
            
            # 如果选择了模型，更新模型设置
            if model_name:
                for model in available_models:
                    if model['name'] == model_name:
                        model_settings['model']['path'] = model['path']
                        current_model_path = model['path']
                        save_model_settings(model_settings)
                        break
            
            # 如果设置了置信度，更新模型设置
            if confidence:
                try:
                    conf_value = float(confidence)
                    if 0 <= conf_value <= 1:
                        model_settings['model']['confidence_threshold'] = conf_value
                        save_model_settings(model_settings)
                except ValueError:
                    pass
            
            file = request.files['file']
            result_img_url, msg, yolo_results, stats = process_image_for_detection(file, current_app.config)
            
            # 如果处理时间未包含在stats中，添加路由处理时间
            if 'processing_time' not in stats:
                stats['processing_time'] = round(time.time() - start_time, 2)

    return render_template(
        'index.html', 
        result_img_url=result_img_url, 
        msg=msg, 
        yolo_results=yolo_results, 
        stats=stats,
        available_models=available_models,
        current_model_path=current_model_path,
        model_settings=model_settings
    )

@main_bp.route('/update_model_settings', methods=['POST'])
def update_model_settings():
    """更新模型设置的API"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': '无效的请求数据'})
        
        # 获取当前设置
        settings = load_model_settings()
        
        # 更新模型路径
        model_name = data.get('model_name')
        if model_name:
            available_models = get_available_models()
            for model in available_models:
                if model['name'] == model_name:
                    settings['model']['path'] = model['path']
                    break
        
        # 更新置信度阈值
        confidence_threshold = data.get('confidence_threshold')
        if confidence_threshold is not None:
            try:
                settings['model']['confidence_threshold'] = float(confidence_threshold)
            except ValueError:
                pass
        
        # 更新IOU阈值
        iou_threshold = data.get('iou_threshold')
        if iou_threshold is not None:
            try:
                settings['model']['iou_threshold'] = float(iou_threshold)
            except ValueError:
                pass
        
        # 更新设备
        device = data.get('device')
        if device:
            settings['model']['device'] = device
        
        # 更新线宽
        line_width = data.get('line_width')
        if line_width is not None:
            try:
                settings['detection']['line_width'] = int(line_width)
            except ValueError:
                pass
        
        # 更新检测选项
        save_results = data.get('save_results')
        if save_results is not None:
            settings['detection']['save_results'] = bool(save_results)
        
        show_labels = data.get('show_labels')
        if show_labels is not None:
            settings['detection']['show_labels'] = bool(show_labels)
        
        show_conf = data.get('show_conf')
        if show_conf is not None:
            settings['detection']['show_conf'] = bool(show_conf)
        
        # 保存设置
        save_model_settings(settings)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@main_bp.route('/upload_model', methods=['POST'])
def upload_model():
    """上传模型的API"""
    try:
        if 'model_file' not in request.files:
            return jsonify({'success': False, 'message': '没有找到文件'})
        
        file = request.files['model_file']
        if file.filename == '':
            return jsonify({'success': False, 'message': '没有选择文件'})
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(MODELS_DIR, filename)
            
            # 保存文件
            file.save(file_path)
            
            return jsonify({'success': True})
        
        return jsonify({'success': False, 'message': '上传失败'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@main_bp.route('/about')
def about():
    return render_template('about.html') 