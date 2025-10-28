import os
import logging
from flask import Flask
from config import Config
from extensions import db
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# ---------------------------
# Initialize Flask app
# ---------------------------
app = Flask(__name__)
app.config.from_object(Config)

# ---------------------------
# Ensure database exists
# ---------------------------
db_uri = app.config['SQLALCHEMY_DATABASE_URI']
db_name = db_uri.rsplit('/', 1)[-1]
engine_uri_without_db = db_uri.rsplit('/', 1)[0]

try:
    engine = create_engine(db_uri)
    conn = engine.connect()
    conn.close()
except OperationalError:
    engine = create_engine(engine_uri_without_db)
    conn = engine.connect()
    conn.execute(f"CREATE DATABASE {db_name}")
    conn.close()
    print(f"Database '{db_name}' created successfully.")

# ---------------------------
# Initialize database
# ---------------------------
db.init_app(app)

# ---------------------------
# Configure logging (all app logs go to app.log)
# ---------------------------
os.makedirs(app.config['LOG_FOLDER'], exist_ok=True)
logger = logging.getLogger()  # root logger
logger.setLevel(logging.INFO)

# Remove Flask default handlers to avoid duplicates
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# File handler
file_handler = logging.FileHandler(f"{app.config['LOG_FOLDER']}/app.log")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Optional: Console output
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# ---------------------------
# Register blueprints
# ---------------------------
from controllers.file_controller import file_bp
from controllers.auth_controller import auth_bp

# Optional: prefix auth blueprint to avoid 404 issues
app.register_blueprint(file_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')

# ---------------------------
# Create database tables if they don't exist
# ---------------------------
with app.app_context():
    db.create_all()

# ---------------------------
# Run the app
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
