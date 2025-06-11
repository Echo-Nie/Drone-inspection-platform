import os
from flask import Flask
from config import UPLOAD_FOLDER
from routes.main_routes import main_bp
from routes.history_routes import history_bp
from routes.statistics_routes import statistics_bp
from routes.visualization_routes import visualization_bp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'detect'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'history'), exist_ok=True)

app.register_blueprint(main_bp)
app.register_blueprint(history_bp)
app.register_blueprint(statistics_bp)
app.register_blueprint(visualization_bp)

if __name__ == '__main__':
    app.run(debug=True)