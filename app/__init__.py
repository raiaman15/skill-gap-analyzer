from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__, 
                template_folder='../templates', 
                static_folder='../static')
    
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models so migration script detects them
    from app import models

    # Register Blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.employee import bp as employee_bp
    app.register_blueprint(employee_bp)

    from app.manager import bp as manager_bp
    app.register_blueprint(manager_bp)

    from app.delivery_lead import bp as delivery_lead_bp
    app.register_blueprint(delivery_lead_bp)

    from app.delivery_head import bp as delivery_head_bp
    app.register_blueprint(delivery_head_bp)

    from app.group_delivery_lead import bp as group_delivery_lead_bp
    app.register_blueprint(group_delivery_lead_bp)

    # Register Error Handlers
    register_error_handlers(app)

    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
