from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required,get_jwt
from applications.model import db,Professional,Customer,Admin,Service,Main_Services,ServiceBooking
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
import re
from applications.task import data_export

class LoginAPI(Resource):
    def post(self):
        data = request.json
        
        if not (data.get('email_id') and data.get('password') and data.get('role')):
            return {"message": "Both email & password fields are required."}, 400
        
        user = None
        role =  data.get('role')

        if data.get('role') == 'professional':
            user = Professional.query.filter_by(email_id=data.get('email_id')).first()
            role = "professional" 
            if user:
             token = create_access_token(identity=user.email_id, additional_claims={'role': user.role})
            else:
                return {"message": "User not found."}, 404

        if data.get('role') == 'customer':
            user = Customer.query.filter_by(email_id=data.get('email_id')).first()
            role = "customer" 
            if user:
             token = create_access_token(identity=user.email_id, additional_claims={'role': user.role})
            else:
                return {"message": "User not found."}, 404

        if data.get('role') == 'admin':
            user = Admin.query.filter_by(email_id=data.get('email_id')).first()
            role = "admin" 
            if user:
             token = create_access_token(identity=user.email_id, additional_claims={'role': user.role})
            else:
                return {"message": "User not found."}, 404

        # If user is not found in any table
        if not user:
            return {"message": "User not found."}, 404

        # Check if password is correct
        
        if not check_password_hash(user.password, data.get('password')):
            return {"message": "Incorrect password."}, 400
        

        if user.role=='professional' and user.status==False:
            return{'message':'Your account is pending approval'},400
        
        return {
            "message": "User logged in successfully",
            "token": token,
            "email_id": user.email_id,
            "role": user.role
        }, 200
    
    @jwt_required()
    def patch(self, Professional_id):
        current_user = get_jwt_identity()
        role = get_jwt().get('role')
        if role != 'admin':
            return {'message': 'You do not have permission'}, 403

        professional = Professional.query.filter_by(Professional_id=Professional_id).first()

        if not professional:
            return {'message': 'Professional not found.'}, 404
        data = request.json
        professional.status = data['status']
        db.session.commit()
        return {'message': 'Professional approved/blocked successfully.'}, 200


class CustomerSignupAPI(Resource):
    def post(self):
        data = request.json

        if not (data.get('full_name') and data.get('email') and data.get('password') and data.get('address') and data.get('pin_code')):
            return {"message": "Bad request! All data fields are required."}, 400

        if Customer.query.filter_by(email_id=data.get('email')).first():
            return {"message": "Email already exists."}, 400
        
        full_name = data.get('full_name').strip()
        address = data.get('address').strip()
        pin_code = data.get('pin_code').strip()

        if len(full_name) == 60 or not full_name.replace(" ", "").isalpha():
            return {"message": "Full name must be text only and less than 60 characters."}, 400

        if not pin_code.isdigit() or len(pin_code) != 6:
            return {"message": "Pin code must be exactly 6 digits."}, 400

        if not pin_code.isdigit():
            return {"message": "Pin code must be numerical only."}, 400
        
        if data.get('password'):
            password = data.get('password').strip()
            hashed_password = generate_password_hash(password)

        new_customer = Customer(
            full_name=data.get('full_name').strip(),
            email_id=data.get('email').strip(),
            password=hashed_password,
            address=data.get('address').strip(),
            pin_code=data.get('pin_code'),
            role='customer'
        )

        db.session.add(new_customer)
        db.session.commit()

        return {"message": "Customer signed up successfully."}, 201

class ProfessionalSignupAPI(Resource):
    def post(self):
        data = request.json

        if not (data.get('full_name') and data.get('email') and data.get('password') and data.get('experience') and data.get('address') and data.get('pin_code') and data.get('service_id')):
            return {"message": "Bad request! All data fields are required."}, 400

        if Professional.query.filter_by(email_id=data.get('email')).first():
            return {"message": "Email already exists."}, 400
        
        full_name = data.get('full_name').strip()
        if len(full_name) > 60 or not all(c.isalpha() or c.isspace() for c in full_name):
            return {"message": "Full name must be alphabetic and less than or equal to 60 characters."}, 400
        
        experience = data.get('experience')
        if not experience.isdigit() or int(experience) >= 80:
            return {"message": "Experience must be a number less than 80."}, 400
        
        pin_code = data.get('pin_code').strip()
        if not pin_code.isdigit() or len(pin_code) != 6:
            return {"message": "Pin code must be exactly 6 digits."}, 400
        
        supporting_documents = data.get('supporting_documents').strip()
        if not re.match(r'^https?://', supporting_documents):
            return {"message": "Supporting documents must be a valid URL."}, 400
        
        if data.get('password'):
            password = data.get('password').strip()
            hashed_password = generate_password_hash(password)

        new_professional = Professional(
            full_name=data.get('full_name').strip(),
            email_id=data.get('email').strip(),
            password=hashed_password,
            experience=data.get('experience'),
            address=data.get('address').strip(),
            pin_code=data.get('pin_code'),
            supporting_documents=data.get('supporting_documents'),
            role='professional',
            status=False,
            MainServices_id=data.get('service_id')
        )

        db.session.add(new_professional)
        db.session.commit()

        return {"message": "Professional signed up successfully."}, 201

class ExportDataAPI(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            role = get_jwt().get('role')

            if role != 'admin':
                return {'message': 'You do not have permission.'}, 403


            professionals = Professional.query.all()
            for professional in professionals:
                all_completed_bookings = []
                main_service_id = professional.MainServices_id
                services = Service.query.filter_by(MainServices_id=main_service_id).all()
                service_ids = [service.service_id for service in services]
                completed_bookings = ServiceBooking.query.filter_by(status='completed').filter(ServiceBooking.service_id.in_(service_ids)).all()
                for booking in completed_bookings:
                    booking_data = {
                        "booking_id": booking.booking_id,
                        "date_of_request": booking.date_of_request.strftime('%Y-%m-%d') if booking.date_of_request else None,
                        "date_of_completion": booking.date_of_completion,
                        "phone_number": booking.phone_number,
                        "location": booking.location,
                        "pincode": booking.pincode,
                        "rating": booking.rating,
                        "service_id": booking.service_id,
                        "status": booking.status,
                        "customer_id": booking.customer_id
                    }
                    all_completed_bookings.append(booking_data)
                data_export(all_completed_bookings, professional.email_id)

            return {'message': "Your data export task has been initiated. Please check your inbox."}, 200

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500


    
 