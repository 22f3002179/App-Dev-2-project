from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required,get_jwt
from applications.model import db,Professional,Customer,Admin,Service,Main_Services,ServiceBooking
from flask import request,current_app as app


class adminserviceAPI(Resource):
    def get(self):
        services = Service.query.all()
        return {
            'services': [
                {
                    'service_id': service.service_id,
                    'service_name': service.main_service.name if service.main_service else None,
                    'price': service.price,
                    'description': service.description,
                    'MainServices_id': service.MainServices_id,
                } 
                for service in services
            ]
        }, 200

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        role = get_jwt().get('role')
        if role != 'admin':
            return {'message': 'You do not have permission'}, 403
        
        data = request.json
        if not data.get('price'):
         return {'message': 'Bad request! Price is required.'}, 400
        elif not data.get('description'):
         return {'message': 'Bad request! Description is required.'}, 400
        elif not data.get('id'):
         return {'message': 'Bad request! Name is required.'}, 400
        try:
          price = float(data.get('price'))
          if price <= 0:
            return {'message': 'Price must be a positive number.'}, 400
        except ValueError:
          return {'message': 'Invalid price format. Price must be a number.'}, 400
        new_Service = Service(
           MainServices_id=data.get('id'),
           description=data.get('description').strip(),
           price=price)
        db.session.add(new_Service)
        db.session.commit()
        return {'message': 'Category created successfully.'}, 201


    @jwt_required()
    def put(self, service_id):
        current_user = get_jwt_identity()
        role = get_jwt().get('role')
        if role != 'admin':
            return {'message': 'You do not have permission'}, 403  
        data = request.json
        if not data.get('price') and not data.get('description'):
            return {'message': 'Bad request! At least one field (price or description) is required.'}, 400        
        service = Service.query.get(service_id)
        if not service:
            return {'message': 'Service not found.'}, 404   
        if 'price' in data:
            service.price = data['price']
        if 'description' in data:
            service.description = data['description'].strip()   
        db.session.commit()    
        return {'message': 'Service updated successfully.'}, 200

    @jwt_required()
    def delete(self, service_id):
        current_user = get_jwt_identity()
        role = get_jwt().get('role')
        if role != 'admin':
            return {'message': 'You do not have permission'}, 403
        service = Service.query.get(service_id)
        if not service:
            return {'message': 'Service not found.'}, 404       
        db.session.delete(service)
        db.session.commit()      
        return {'message': 'Service deleted successfully.'}, 200

