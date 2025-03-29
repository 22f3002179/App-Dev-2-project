from flask import Flask, request
from flask_restful import Api
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from applications.adminservice import adminserviceAPI
from applications.auth_api import ProfessionalSignupAPI, CustomerSignupAPI, LoginAPI,ExportDataAPI
from applications.booking import bookingAPI
from applications.Mainservice import MainServiceAPI 
from applications.model import db,Professional,Customer,Admin,Service,Main_Services,ServiceBooking
from applications.user import ProfessionalAPI,CustomerAPI,cache
from applications.worker import celery
from applications.task import *
from werkzeug.security import generate_password_hash, check_password_hash
from celery import Celery


base_dir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "database.sqlite3")
app.config["SECRET_KEY"] = "AppdevProject-secret"
app.config["JWT_SECRET_KEY"] = "AppdevProject-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = "redis://localhost:6379"
app.config['CACHE_DEFAULT_TIMEOUT'] = 300


celery.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/1',
    timezone='Asia/Kolkata'
)
# Initialize extensions
db.init_app(app)
cache.init_app(app)
api = Api(app)
jwt = JWTManager(app)
celery.conf.update(app.config)
app.app_context().push()
from flask_cors import CORS

CORS(app, origins=["http://localhost:5173"])


def add_admin():
    admin = Admin.query.filter_by(email_id='abc@gmail.com', role='admin').first()
    if not admin:
        new_admin = Admin(
            username='Admin',
            email_id='abc@gmail.com',
            password=generate_password_hash('abc'),
            role='admin'
        )
        db.session.add(new_admin)
        db.session.commit()
        return "Admin added."
    
    return "Admin already exists."

api.add_resource(adminserviceAPI, '/api/adminservice','/api/adminservice/<int:service_id>',methods=['POST','GET','PUT','DELETE'] )
api.add_resource(ProfessionalSignupAPI, '/api/professionalSignup','/api/professionalSignup/<int:professional_id>', methods=['POST','GET','PUT','DELETE'])
api.add_resource(CustomerSignupAPI, '/api/CustomerSignup')
api.add_resource(LoginAPI, '/api/Login','/api/Login/<int:Professional_id>', methods=['POST', 'PATCH'])
api.add_resource(bookingAPI, '/api/booking','/api/booking/<int:booking_id>')
api.add_resource(MainServiceAPI, '/api/MainService','/api/MainService/<int:MainServices_id>',methods=['GET', 'POST', 'DELETE'])
api.add_resource(ProfessionalAPI, '/api/Professional','/api/Professional/<int:professional_id>',methods=['GET', 'POST', 'DELETE','PUT'])
api.add_resource(CustomerAPI, '/api/Customer','/api/Customer/<int:customer_id>',methods=['GET', 'POST', 'DELETE','PUT'])
api.add_resource(ExportDataAPI, '/api/exportData')



if __name__=='__main__':
    db.create_all()
    add_admin()
    app.run(debug=True)