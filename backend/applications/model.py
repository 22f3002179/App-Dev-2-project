from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,String,Column,ForeignKey
from datetime import datetime

db = SQLAlchemy()

class Professional(db.Model):
    __tablename__ = 'professional'
    Professional_id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(60), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(60), nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    supporting_documents = db.Column(db.String)
    role = db.Column(db.String(15), nullable=False, default='professional')
    status = db.Column(db.Boolean, nullable=False, default=False)
    MainServices_id = db.Column(db.Integer, db.ForeignKey('main_services.MainServices_id'), nullable=False)
    main_service = db.relationship('Main_Services', back_populates='professionals', lazy=True)

    def to_json(self):
        return {
            "Professional_id": self.Professional_id,
            "email_id": self.email_id,
            "full_name": self.full_name,
            "experience": self.experience,
            "address": self.address,
            "pin_code": self.pin_code,
            "supporting_documents": self.supporting_documents,
            "role": self.role,
            "status": self.status,
            "MainServices_id": self.MainServices_id,
        }

class Customer(db.Model):
    __tablename__ = 'customer'
    Customer_id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String, nullable=False, default='customer')
    booking = db.relationship('ServiceBooking', backref='customer', cascade='all, delete-orphan', lazy=True)

    def to_json(self):
        return {
            "Customer_id": self.Customer_id,
            "email_id": self.email_id,
            "full_name": self.full_name,
            "address": self.address,
            "pin_code": self.pin_code,
            "role": self.role,
        }

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String, nullable=False, default='admin')

class Service(db.Model):
    __tablename__ = 'service'
    service_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    MainServices_id = db.Column(db.Integer, db.ForeignKey('main_services.MainServices_id'), nullable=False)
    bookings = db.relationship('ServiceBooking', backref='service', cascade='all, delete-orphan', lazy=True)
    main_service = db.relationship('Main_Services', back_populates='services', lazy=True)

    def to_json(self):
        return {
            "service_id": self.service_id,
            "price": self.price,
            "description": self.description,
            "MainServices_id": self.MainServices_id,
        }

class Main_Services(db.Model):
    __tablename__ = 'main_services'
    MainServices_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    professionals = db.relationship('Professional', back_populates='main_service', cascade='all, delete-orphan', lazy=True)
    services = db.relationship('Service', back_populates='main_service', cascade='all, delete-orphan', lazy=True)

    def to_json(self):
        return {
            "MainServices_id": self.MainServices_id,
            "name": self.name,
        }

class ServiceBooking(db.Model):
    __tablename__ = 'service_booking'
    booking_id = db.Column(db.Integer, primary_key=True)
    date_of_request = db.Column(db.Date, nullable=False)
    date_of_completion = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False, default='requested') #assigned, completed
    location = db.Column(db.String, nullable=False)
    pincode = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.Professional_id'), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.Customer_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id'), nullable=False)
    

    def to_json(self):
        return {
            "booking_id": self.booking_id,
            "date_of_request": self.date_of_request.strftime('%Y-%m-%d') if self.date_of_request else None,
            "date_of_completion": self.date_of_completion if self.date_of_completion else None,
            "phone_number": self.phone_number,
            "status": self.status,
            "location": self.location,
            "pincode": self.pincode,
            "rating": self.rating,
            "professional_id": self.professional_id,
            "customer_id": self.customer_id,
            "service_id": self.service_id
        }
