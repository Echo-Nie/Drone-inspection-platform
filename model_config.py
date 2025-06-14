import os
import yaml
from pathlib import Path

# 模型配置基础目录
MODELS_DIR = 'models'
CONFIG_DIR = 'configs'
DEFAULT_MODEL = 'uav.pt'  # 默认模型

# 确保目录存在
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

# 默认配置文件路径
DEFAULT_CONFIG_PATH = os.path.join(CONFIG_DIR, 'model_settings.yaml')

# 预定义的YOLO模型版本
YOLO_VERSIONS = {
    'yolov8': {
        'name': 'YOLOv8',
        'description': 'Latest version with improved accuracy and speed',
        'default_config': 'yolov8n.yaml',
        'supported_formats': ['.pt', '.yaml']
    },
    'yolov7': {
        'name': 'YOLOv7',
        'description': 'High performance object detection',
        'default_config': 'yolov7.yaml',
        'supported_formats': ['.pt', '.yaml']
    },
    'yolov5': {
        'name': 'YOLOv5',
        'description': 'Stable and widely used version',
        'default_config': 'yolov5s.yaml',
        'supported_formats': ['.pt', '.yaml']
    }
}

# 默认配置
DEFAULT_SETTINGS = {
    'model': {
        'path': os.path.join(MODELS_DIR, DEFAULT_MODEL),
        'version': 'yolov8',
        'confidence_threshold': 0.25,
        'iou_threshold': 0.45,
        'device': 'auto'  # 'cpu', 'cuda:0', 'auto'
    },
    'detection': {
        'save_results': True,
        'show_labels': True,
        'show_conf': True,
        'line_width': 2
    }
}

def load_model_settings():
    """加载模型配置，如果配置文件不存在则创建默认配置"""
    if os.path.exists(DEFAULT_CONFIG_PATH):
        with open(DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as f:
            try:
                settings = yaml.safe_load(f)
                # 确保配置完整，如果缺少某些配置项则使用默认值
                if 'model' not in settings:
                    settings['model'] = DEFAULT_SETTINGS['model']
                if 'detection' not in settings:
                    settings['detection'] = DEFAULT_SETTINGS['detection']
                return settings
            except Exception as e:
                print(f"Error loading model settings: {e}")
                return DEFAULT_SETTINGS
    else:
        # 创建默认配置文件
        save_model_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

def save_model_settings(settings):
    """保存模型配置到YAML文件"""
    try:
        with open(DEFAULT_CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(settings, f, default_flow_style=False, allow_unicode=True)
        return True
    except Exception as e:
        print(f"Error saving model settings: {e}")
        return False

def get_available_models():
    """获取可用的模型文件列表"""
    models = []
    
    # 扫描模型目录
    if os.path.exists(MODELS_DIR):
        for file in os.listdir(MODELS_DIR):
            file_path = os.path.join(MODELS_DIR, file)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[1].lower()
                if ext in ['.pt', '.yaml']:
                    models.append({
                        'name': file,
                        'path': file_path,
                        'format': ext[1:],  # 移除点号
                        'size': os.path.getsize(file_path) / (1024 * 1024),  # 转换为MB
                        'modified': os.path.getmtime(file_path)
                    })
    
    return sorted(models, key=lambda x: x['modified'], reverse=True)

def get_model_instance(custom_settings=None):
    """
    根据配置获取YOLO模型实例
    可以传入自定义配置覆盖默认配置
    """
    from ultralytics import YOLO
    
    # 加载配置
    settings = load_model_settings()
    
    # 如果有自定义配置，则覆盖默认配置
    if custom_settings:
        if 'model' in custom_settings:
            settings['model'].update(custom_settings['model'])
        if 'detection' in custom_settings:
            settings['detection'].update(custom_settings['detection'])
    
    model_path = settings['model']['path']
    
    # 检查模型文件是否存在
    if not os.path.exists(model_path):
        # 如果指定的模型不存在，尝试在models目录中查找
        potential_path = os.path.join(MODELS_DIR, os.path.basename(model_path))
        if os.path.exists(potential_path):
            model_path = potential_path
        else:
            # 如果还是找不到，使用默认模型
            model_path = os.path.join(MODELS_DIR, DEFAULT_MODEL)
            # 如果默认模型也不存在，抛出异常
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
    
    # 加载模型
    model = YOLO(model_path)
    
    return model, settings 