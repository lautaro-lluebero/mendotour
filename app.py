from flask import Flask, jsonify , render_template, request 
from models.db import db
from config.config import DATABASE_CONNECTION_URI
from routes.routes_users import routes_users as users
from routes.routes_auth import routes_auth as auth
from routes.routes_main import routes_main as main
from routes.routes_reportes import routes_reportes as reportes
from routes.routes_opiniones import routes_opiniones as opiniones

# Initialize Flask app
app = Flask(__name__)

# Register blueprints
app.register_blueprint(users)
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(reportes)
app.register_blueprint(opiniones)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secretkey'
db.init_app(app)

# Create database tables
with app.app_context():
    #db.drop_all()
    db.create_all()

# Simple route to test the app

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

@app.route('/')
def home():
    return render_template('home.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
