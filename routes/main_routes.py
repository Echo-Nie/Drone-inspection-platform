from flask import Blueprint, render_template, request, current_app
from services.detection_service import process_image_for_detection

main_bp = Blueprint('main', __name__)

@main_bp.route('/index', methods=['GET', 'POST'])
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
            result_img_url, msg, yolo_results, stats = process_image_for_detection(file, current_app.config)

    return render_template('index.html', result_img_url=result_img_url, msg=msg, yolo_results=yolo_results, stats=stats)

@main_bp.route('/about')
def about():
    return render_template('about.html') 