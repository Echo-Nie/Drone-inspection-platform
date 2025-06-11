from flask import Blueprint, render_template, request, jsonify
from services.history_service import load_history
from services.statistics_service import get_statistics_data

statistics_bp = Blueprint('statistics', __name__)

@statistics_bp.route('/statistics')
def statistics():
    classes = list(set([item for record in load_history() for item in record.get('main_classes', [])]))
    return render_template('statistics.html', classes=classes)

@statistics_bp.route('/api/statistics', methods=['POST'])
def api_statistics():
    response_data = get_statistics_data(request.get_json())
    return jsonify(response_data) 