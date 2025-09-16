from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config['UPLOAD_FOLDER'] = '/app/uploads'
    app.config['OUTPUT_FOLDER'] = '/app/outputs'
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
    from .routes import bp
    app.register_blueprint(bp)
    return app
