from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required, get_jwt
from applications.model import db, Professional, Customer, Admin, Service, Main_Services, ServiceBooking
from flask import request
import re
from flask_caching import Cache

cache = Cache()
class ProfessionalAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=30)
    def get(self):
        current_user = get_jwt_identity()
        role = get_jwt().get('role')

        if role not in ['admin', 'professional']:
            return {'message': 'You do not have permission'}, 403

        email_id = request.args.get('email_id')  # Retrieve email from request parameters

        if email_id:
            professional = Professional.query.filter(Professional.email_id.ilike(email_id)).first()
            if not professional:
                return {'error': 'No professional data found for this email.'}, 404

            professional_data = {
                'Professional_id': professional.Professional_id,
                'email_id': professional.email_id,
                'full_name': professional.full_name,
                'experience': professional.experience,
                'address': professional.address,
                'pin_code': professional.pin_code,
                'supporting_documents': professional.supporting_documents,
                'role': professional.role,
                'status': professional.status,
                'MainServices_id': professional.MainServices_id
            }
            return {'professional': professional_data}

        professionals = Professional.query.all()
        professional_list = [
            {
                'Professional_id': professional.Professional_id,
                'email_id': professional.email_id,
                'full_name': professional.full_name,
                'experience': professional.experience,
                'address': professional.address,
                'pin_code': professional.pin_code,
                'supporting_documents': professional.supporting_documents,
                'role': professional.role,
                'status': professional.status,
                'MainServices_id': professional.MainServices_id
            }
            for professional in professionals
        ]

        return {'professionals': professional_list}

    @jwt_required()  
    def delete(self, professional_id):
        current_user = get_jwt_identity()
        role = get_jwt().get('role')

        if role != 'admin':
            return {'message': 'You do not have permission'}, 403

        professional = Professional.query.get(professional_id)
        if not professional:
            return {'message': 'Professional not found.'}, 404      

        db.session.delete(professional)
        db.session.commit()
        return {'message': 'Professional deleted successfully.'}, 200


    @jwt_required()  
    def put(self, professional_id):
        current_user = get_jwt_identity()
        role = get_jwt().get('role')

        if role != 'professional':
            return {'message': 'You do not have permission'}, 403
        
        professional = Professional.query.get(professional_id)
        if not professional:
            return {'message': 'Professional not found.'}, 404
        
        data = request.json
        

        if 'full_name' in data:
            professional.full_name = data['full_name']
        if 'experience' in data:
            professional.experience = data['experience']
        if 'address' in data:
            professional.address = data['address']
        if 'pin_code' in data:
            professional.pin_code = data['pin_code']
        if 'supporting_documents' in data:
            professional.supporting_documents = data['supporting_documents']
        
        db.session.commit()

        return {
            'message': 'Professional information updated successfully.',
            'professional': {
                'Professional_id': professional.Professional_id,
                'email_id': professional.email_id,
                'full_name': professional.full_name,
                'experience': professional.experience,
                'address': professional.address,
                'pin_code': professional.pin_code,
                'supporting_documents': professional.supporting_documents,
                'role': professional.role,
                'status': professional.status,
                'MainServices_id': professional.MainServices_id
            }
        }, 200

class CustomerAPI(Resource):

    @jwt_required() 
    @cache.cached(timeout=30)
    def get(self):
        customers = Customer.query.all()
        current_user = get_jwt_identity()
        role = get_jwt().get('role')

        if role not in ['admin', 'customer']:
            return {'message': 'You do not have permission'}, 403

        customer_list = []
        for customer in customers:
            customer_list.append({
                'Customer_id': customer.Customer_id,
                'email_id': customer.email_id,
                'full_name': customer.full_name,
                'address': customer.address,
                'pin_code': customer.pin_code,
                'role': customer.role
            })
        return {'customers': customer_list}, 200

    @jwt_required()  
    def delete(self, customer_id):
        current_user = get_jwt_identity()
        role = get_jwt().get('role')

        if role != 'admin':
            return {'message': 'You do not have permission'}, 403

        customer = Customer.query.get(customer_id)
        if not customer:
            return {'message': 'Customer not found.'}, 404

        db.session.delete(customer)
        db.session.commit()
        return {'message': 'Customer deleted successfully.'}, 200

    @jwt_required()  
    def put(self, customer_id):
        current_user = get_jwt_identity()
        role = get_jwt().get('role')

        if role != 'customer':
            return {'message': 'You do not have permission'}, 403

        customer = Customer.query.get(customer_id)
        if not customer:
            return {'message': 'Customer not found.'}, 404

        data = request.json

        if 'full_name' in data:
            customer.full_name = data['full_name']
        if 'address' in data:
            customer.address = data['address']
        if 'pin_code' in data:
            customer.pin_code = data['pin_code']

        db.session.commit()

        return {
            'message': 'Customer information updated successfully.',
            'customer': {
                'Customer_id': customer.Customer_id,
                'email_id': customer.email_id,
                'full_name': customer.full_name,
                'address': customer.address,
                'pin_code': customer.pin_code,
                'role': customer.role
            }
        }, 200