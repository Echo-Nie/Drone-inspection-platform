from flask import Blueprint, render_template, url_for, redirect, jsonify, request
import os
from config import UPLOAD_FOLDER, HISTORY_FILE
from services.history_service import load_history

history_bp = Blueprint('history', __name__)

@history_bp.route('/history')
def history():
    history_records = load_history()
    return render_template('history.html', history_records=history_records)

@history_bp.route('/clear_history', methods=['POST'])
def clear_history():
    detect_dir = os.path.join(UPLOAD_FOLDER, 'detect')
    if os.path.exists(detect_dir):
        for f in os.listdir(detect_dir):
            file_path = os.path.join(detect_dir, f)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    
    return redirect(url_for('history.history')) 