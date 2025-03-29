from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required,get_jwt
from applications.model import db, Professional,Customer,Admin,Service,Main_Services,ServiceBooking
from flask import request



class MainServiceAPI(Resource):
    def get(self):
     services = Main_Services.query.all()
     service_list = [{"MainServices_id": service.MainServices_id, "name": service.name} for service in services]
     return {"services": service_list}, 200
    # Add Service (Only Admin)
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        role = get_jwt().get('role')
        if role != 'admin':
            return {'message': 'You do not have permission to add services.'}, 403
        
        name = request.json.get('name')
        if not name:
            return {'message': 'Service name is required.'}, 400
        
        new_service = Main_Services(name=name)
        db.session.add(new_service)
        db.session.commit()
        
        return {'message': f'Service {name} added successfully.'}, 201
    
    # Delete Service (Only Admin)
    @jwt_required()
    def delete(self, MainServices_id ):
        current_user = get_jwt_identity()
        role = get_jwt().get('role')
        if role != 'admin':
            return {'message': 'You do not have permission.'}, 403
        
        service_to_delete = Main_Services.query.get(MainServices_id)
        if not service_to_delete:
            return {'message': 'Service not found.'}, 404
        
        db.session.delete(service_to_delete)
        db.session.commit()
        
        return {'message': 'Service deleted successfully.'}, 200
    